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

app = Flask(__name__, template_folder=
            "templates", static_folder="static")

DORAR_API_URL = "https://dorar.net/dorar_api.json"

# --- Dorar API Integration --- 
def parse_dorar_response(html_content):
    """Parses the HTML response from Dorar API to extract Hadith details."""
    soup = BeautifulSoup(html_content, "html.parser")
    hadiths = []
    hadith_elements = soup.find_all("div", class_="hadith")
    info_elements = soup.find_all("div", class_="hadith-info")

    num_results = min(len(hadith_elements), len(info_elements))

    for i in range(num_results):
        hadith_div = hadith_elements[i]
        info_div = info_elements[i]

        hadith_text = ""
        for content_part in hadith_div.contents:
            if content_part.name == "span" and "search-keys" in content_part.get("class", []):
                hadith_text += content_part.get_text(strip=True)
            elif isinstance(content_part, str):
                hadith_text += content_part
        hadith_text = re.sub(r"\s+", " ", hadith_text.strip())
        hadith_text = re.sub(r"^\d+\s*-\s*", "", hadith_text).strip()

        metadata = {}
        spans = info_div.find_all("span", class_="info-subtitle")
        for span in spans:
            key_ar = span.get_text(strip=True).replace(":", "")
            value = "N/A"
            current_sibling = span.next_sibling
            while current_sibling:
                if isinstance(current_sibling, str) and current_sibling.strip():
                    value = current_sibling.strip()
                    break
                elif current_sibling.name == "span" and not current_sibling.has_attr("class"):
                     value = current_sibling.get_text(strip=True)
                     break
                elif current_sibling.name == "span" and "info-subtitle" in current_sibling.get("class", []):
                    break 
                current_sibling = current_sibling.next_sibling
            
            key_map = {
                "الراوي": "narrator",
                "المحدث": "scholar",
                "المصدر": "source",
                "الصفحة أو الرقم": "reference",
                "خلاصة حكم المحدث": "grade"
            }
            key_en = key_map.get(key_ar, key_ar)
            metadata[key_en] = value

        if hadith_text:
            hadiths.append({
                "text": hadith_text,
                "narrator": metadata.get("narrator", "N/A"),
                "scholar": metadata.get("scholar", "N/A"),
                "source": metadata.get("source", "N/A"),
                "reference": metadata.get("reference", "N/A"),
                "grade": metadata.get("grade", "N/A")
            })
            
    more_results_available = soup.find("a", string="المزيد") is not None
    return hadiths, more_results_available

def fetch_from_dorar(query):
    try:
        encoded_query = quote(query)
        response = requests.get(f"{DORAR_API_URL}?skey={encoded_query}&st=a&pclass=1", timeout=15)
        response.raise_for_status()
        data = response.json()
        html_content = data.get("ahadith", {}).get("result", "")
        if not html_content:
             print(f"No HTML content found in Dorar response for query: {query}")
             return [], False
        return parse_dorar_response(html_content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Dorar API: {e}")
        return None, False
    except json.JSONDecodeError as e:
        print(f"Error decoding Dorar API JSON response: {e}")
        return None, False
    except Exception as e:
        print(f"Error parsing Dorar API response: {e}")
        return None, False

# --- Routes --- 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hadith-ranking-explanation")
def hadith_ranking_explanation():
    return render_template("hadith_ranking.html")

@app.route("/locales/<lang>.json")
def get_locale(lang):
    return send_from_directory(os.path.join(app.static_folder, "locales"), f"{lang}.json")

@app.route("/suggest", methods=["GET"])
def suggest_hadith():
    query = request.args.get("q", "")
    limit = request.args.get("limit", 5, type=int)
    if not query or len(query) < 3:
        return jsonify([])
    hadiths, _ = fetch_from_dorar(query)
    if hadiths is None:
        return jsonify({"error": "Failed to fetch suggestions from Dorar API"}), 500
    suggestions = [h["text"] for h in hadiths[:limit]]
    return jsonify(suggestions)

@app.route("/check", methods=["POST"])
def check_hadith():
    data = request.get_json()
    input_text = data.get("text", "")
    if not input_text:
        return jsonify({"error": "No text provided"}), 400
    hadiths, more_results = fetch_from_dorar(input_text)
    if hadiths is None:
        return jsonify({"error": "Failed to fetch results from Dorar API"}), 500
    if not hadiths:
        return jsonify({"found": False, "hadiths": []})
    else:
        def get_grade_sort_value(grade_text):
            if not grade_text or grade_text == "N/A":
                return 8 # Unspecified or N/A last

            # Prioritize more specific and stronger grades first
            if "صحيح لغيره" in grade_text: return 0
            if "رجاله رجال الصحيح" in grade_text: return 0
            if "إسناده صحيح" in grade_text: return 0
            if "صحيح" in grade_text and "ليس بصحيح" not in grade_text and "غير صحيح" not in grade_text: return 0
            
            if "حسن لغيره" in grade_text: return 1
            if "إسناده حسن" in grade_text: return 1
            if "رجاله ثقات" in grade_text: return 1 # Often implies Hasan or Sahih, place with Hasan
            if "حسن" in grade_text and "ليس بحسن" not in grade_text and "غير حسن" not in grade_text: return 1

            # Weak categories, ordered from "less weak" to "very weak/fabricated"
            # Important: Check for more severe forms of weakness before general "ضعيف"
            if "موضوع" in grade_text: return 6      # Mawdu (Fabricated) - worst
            if "باطل" in grade_text: return 5       # Batil (False)
            if "لا يصح" in grade_text: return 5     # La Yasihh (Not Authentic)
            if "لا أصل له" in grade_text: return 5 # La Asla Lahu (No Basis)
            if "منكر" in grade_text: return 4       # Munkar
            if "ضعيف جدا" in grade_text: return 3 # Daif Jiddan (Very Weak)
            
            # General Daif (should be checked after more specific weak terms)
            if "ضعيف" in grade_text: return 2 # General Daif
            
            return 7 # Other grades not specifically categorized, place before N/A

        sorted_hadiths = sorted(hadiths, key=lambda h: get_grade_sort_value(h.get("grade", "N/A")))
        
        return jsonify({
            "found": True,
            "hadiths": sorted_hadiths, 
            "more_results_available": more_results
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

