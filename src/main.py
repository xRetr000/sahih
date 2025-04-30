#!/home/ubuntu/hadith_checker/venv/bin/python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import re # Import regex for cleaning
from urllib.parse import quote # For URL encoding search query

# Corrected Flask initialization (using single quotes, no backslashes)
app = Flask(__name__, template_folder='templates', static_folder='static')

DORAR_API_URL = "https://dorar.net/dorar_api.json"

# --- Dorar API Integration --- 
def parse_dorar_response(html_content):
    """Parses the HTML response from Dorar API to extract Hadith details."""
    soup = BeautifulSoup(html_content, 'html.parser')
    hadiths = []
    hadith_elements = soup.find_all('div', class_='hadith')
    info_elements = soup.find_all('div', class_='hadith-info')

    # Ensure we have matching numbers of hadith texts and info blocks
    num_results = min(len(hadith_elements), len(info_elements))

    for i in range(num_results):
        hadith_div = hadith_elements[i]
        info_div = info_elements[i]

        # Extract Hadith text, removing the search key span and extra spaces
        hadith_text = ''
        for content in hadith_div.contents:
            if content.name == 'span' and 'search-keys' in content.get('class', []):
                hadith_text += content.get_text(strip=True)
            elif isinstance(content, str):
                hadith_text += content
        # Corrected regex to replace multiple whitespace characters with a single space
        hadith_text = re.sub(r'\s+', ' ', hadith_text.strip()) 
        # Remove leading number like "1 - "
        hadith_text = re.sub(r'^\d+\s*-\s*', '', hadith_text).strip()

        # Extract metadata
        metadata = {}
        spans = info_div.find_all('span', class_='info-subtitle')
        for span in spans:
            key_ar = span.get_text(strip=True).replace(":", '')
            value = 'N/A'
            # Try to find the value in the next non-empty text node or non-subtitle span
            current_sibling = span.next_sibling
            while current_sibling:
                if isinstance(current_sibling, str) and current_sibling.strip():
                    value = current_sibling.strip()
                    break
                elif current_sibling.name == 'span' and not current_sibling.has_attr('class'):
                     value = current_sibling.get_text(strip=True)
                     break
                elif current_sibling.name == 'span' and 'info-subtitle' in current_sibling.get('class', []):
                    # Reached the next subtitle, stop looking for value for the current key
                    break 
                current_sibling = current_sibling.next_sibling
            
            # Map Arabic keys to English keys for consistency
            key_map = {
                "الراوي": "narrator",
                "المحدث": "scholar",
                "المصدر": "source",
                "الصفحة أو الرقم": "reference",
                "خلاصة حكم المحدث": "grade"
            }
            key_en = key_map.get(key_ar, key_ar) # Use original key if not mapped
            metadata[key_en] = value

        if hadith_text:
            hadiths.append({
                "text": hadith_text,
                "narrator": metadata.get('narrator', 'N/A'),
                "scholar": metadata.get('scholar', 'N/A'),
                "source": metadata.get('source', 'N/A'),
                "reference": metadata.get('reference', 'N/A'),
                "grade": metadata.get('grade', 'N/A')
            })
            
    # Check for "المزيد" link to indicate more results might be available on the site
    more_results_available = soup.find('a', string='المزيد') is not None

    return hadiths, more_results_available

def fetch_from_dorar(query):
    """Fetches search results from Dorar API for a given query."""
    try:
        encoded_query = quote(query)
        response = requests.get(f"{DORAR_API_URL}?skey={encoded_query}", timeout=15) # Increased timeout
        response.raise_for_status() # Raise an exception for bad status codes
        # The actual content is inside the 'ahadith.result' field of the JSON
        data = response.json()
        html_content = data.get('ahadith', {}).get('result', '')
        if not html_content:
             print(f"No HTML content found in Dorar response for query: {query}") # Debugging
             return [], False # Return empty list if no result HTML
        return parse_dorar_response(html_content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Dorar API: {e}")
        return None, False # Indicate error
    except json.JSONDecodeError as e:
        print(f"Error decoding Dorar API JSON response: {e}")
        return None, False # Indicate error
    except Exception as e:
        # Log the specific parsing error and the HTML content that caused it
        print(f"Error parsing Dorar API response: {e}")
        # print(f"Problematic HTML content:\n{html_content[:500]}...") # Optionally log part of the HTML
        return None, False # Indicate error

# --- Routes --- 
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

# Route for serving localization files
@app.route('/locales/<lang>.json')
def get_locale(lang):
    return send_from_directory(os.path.join(app.static_folder, 'locales'), f'{lang}.json')

@app.route('/suggest', methods=['GET'])
def suggest_hadith():
    """Provides Hadith suggestions based on partial input query using Dorar API."""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 5, type=int)

    if not query or len(query) < 3: # Only suggest if query is reasonably long
        return jsonify([])

    hadiths, _ = fetch_from_dorar(query)

    if hadiths is None: # Handle API error
        return jsonify({"error": "Failed to fetch suggestions from Dorar API"}), 500
        
    # Return only the text of the first few hadiths as suggestions
    suggestions = [h['text'] for h in hadiths[:limit]]
    return jsonify(suggestions)


@app.route('/check', methods=['POST'])
def check_hadith():
    """Receives Hadith text, searches using Dorar API, and returns the best match details."""
    data = request.get_json()
    input_text = data.get('text', '')

    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    hadiths, more_results = fetch_from_dorar(input_text)

    if hadiths is None: # Handle API error
        return jsonify({"error": "Failed to fetch results from Dorar API"}), 500

    if not hadiths:
        return jsonify({'found': False})
    else:
        # Return the first result from Dorar as the primary match
        # The API search itself acts as the matching logic
        first_match = hadiths[0]
        return jsonify({
            'found': True,
            'hadith_text': first_match['text'],
            'narrator': first_match['narrator'],
            'scholar': first_match['scholar'],
            'source': first_match['source'],
            'reference': first_match['reference'],
            'grade': first_match['grade'],
            'more_results_available': more_results # Indicate if Dorar has more results
            # Similarity score is not directly applicable here as Dorar does the matching
        })

if __name__ == '__main__':
    # Listen on all interfaces, essential for deployment/exposure
    app.run(host='0.0.0.0', port=5000, debug=False)

