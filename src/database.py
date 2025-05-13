# Mock Hadith Database

# This list contains tuples: (hadith_text, source, number)
hadiths = [
    (
        "Actions are judged by intentions. So whoever emigrated for worldly benefits or for a woman to marry, his emigration was for what he emigrated for.",
        "Sahih al-Bukhari",
        "1"
    ),
    (
        "Religion is very easy and whoever overburdens himself in his religion will not be able to continue in that way. So you should not be extremists, but try to be near to perfection and receive the good tidings that you will be rewarded; and gain strength by worshipping in the mornings, the afternoons, and during the last hours of the nights.",
        "Sahih al-Bukhari",
        "39"
    ),
    (
        "None of you will have faith till he wishes for his (Muslim) brother what he likes for himself.",
        "Sahih al-Bukhari",
        "13"
    ),
    (
        "The seeking of knowledge is obligatory for every Muslim.",
        "Sunan Ibn Majah", # Note: While requested Bukhari/Muslim, adding variety for testing might be useful, or stick strictly? Sticking to request for now.
        "224" # Placeholder, will replace with actual Bukhari/Muslim hadith
    ),
     (
        "God does not look at your forms and possessions but He looks at your hearts and your deeds.",
        "Sahih Muslim",
        "2564c"
    ),
    (
        "The best among you are those who have the best manners and character.",
        "Sahih al-Bukhari",
        "3559"
    ),
    (
        "A man walking along a path felt very thirsty. Reaching a well he descended into it, drank his fill and came up. Then he saw a dog with its tongue hanging out, trying to lick up mud to quench its thirst. The man saw that the dog was feeling the same thirst as he had felt so he went down into the well again and filled his shoe with water and gave the dog a drink. God forgave his sins for this action.' The Prophet was asked: 'Messenger of God, are we rewarded for kindness towards animals?' He said: 'There is a reward for kindness to every living thing.'",
        "Sahih al-Bukhari",
        "2363"
    ),
    (
        "He who eats his fill while his neighbor goes without food is not a believer.",
        "Al-Adab Al-Mufrad (Bukhari)", # Technically Bukhari's collection, acceptable?
        "112" # Placeholder, will replace with actual Bukhari/Muslim hadith
    ),
    (
        "Wealth is not in having many possessions. Rather, true wealth is the richness of the soul.",
        "Sahih Muslim",
        "1051a"
    ),
    (
        "Do not wish to be like anyone except in two cases. The first is a person whom Allah has given wealth and he spends it righteously. The second is the one whom Allah has given wisdom and he acts according to it and teaches it to others.",
        "Sahih al-Bukhari",
        "73"
    ),
    (
        "The believer's shade on the Day of Resurrection will be his charity.",
        "Tirmidhi", # Placeholder, will replace with actual Bukhari/Muslim hadith
        "604" # Placeholder
    ),
    # Replacing placeholders with actual Bukhari/Muslim Hadiths
    # Replacing Hadith 4 (Ibn Majah)
    (
        "Whoever follows a path in the pursuit of knowledge, Allah will make a path to Paradise easy for him.",
        "Sahih Muslim",
        "2699"
    ),
    # Replacing Hadith 8 (Al-Adab Al-Mufrad)
    (
        "Modesty is part of faith.",
        "Sahih al-Bukhari",
        "24"
    ),
    # Replacing Hadith 11 (Tirmidhi)
    (
        "Take benefit of five before five: Your youth before your old age, your health before your sickness, your wealth before your poverty, your free time before you are preoccupied, and your life before your death.",
        "Mustadrak Hakim", # Still not Bukhari/Muslim, finding suitable short ones.
        "7846" # Placeholder
    ),
    # Adding more Bukhari/Muslim
    (
        "Control your tongue, let your house be enough for you, and weep for your sins.",
        "Jami` at-Tirmidhi", # Still not Bukhari/Muslim, will find better ones.
        "2406" # Placeholder
    ),
    # Final attempt to get 10+ Bukhari/Muslim
    (
        "The strong man is not the good wrestler; the strong man is only the one who controls himself when he is angry.",
        "Sahih al-Bukhari",
        "6114"
    ),
    (
        "Whosoever relieves a believer's distress of the distressful aspects of this world, Allah will rescue him from a difficulty of the difficulties of the Hereafter.",
        "Sahih Muslim",
        "2699"
    ),
    (
        "Visit the sick, feed the hungry, and free the captive.",
        "Sahih al-Bukhari",
        "5649"
    )
]

# Cleaned list with only Bukhari and Muslim, ensuring at least 10
hadiths_clean = [
    ("Actions are judged by intentions. So whoever emigrated for worldly benefits or for a woman to marry, his emigration was for what he emigrated for.", "Sahih al-Bukhari", "1"),
    ("Religion is very easy and whoever overburdens himself in his religion will not be able to continue in that way. So you should not be extremists, but try to be near to perfection and receive the good tidings that you will be rewarded; and gain strength by worshipping in the mornings, the afternoons, and during the last hours of the nights.", "Sahih al-Bukhari", "39"),
    ("None of you will have faith till he wishes for his (Muslim) brother what he likes for himself.", "Sahih al-Bukhari", "13"),
    ("God does not look at your forms and possessions but He looks at your hearts and your deeds.", "Sahih Muslim", "2564c"),
    ("The best among you are those who have the best manners and character.", "Sahih al-Bukhari", "3559"),
    ("A man walking along a path felt very thirsty. Reaching a well he descended into it, drank his fill and came up. Then he saw a dog with its tongue hanging out, trying to lick up mud to quench its thirst. The man saw that the dog was feeling the same thirst as he had felt so he went down into the well again and filled his shoe with water and gave the dog a drink. God forgave his sins for this action.' The Prophet was asked: 'Messenger of God, are we rewarded for kindness towards animals?' He said: 'There is a reward for kindness to every living thing.'", "Sahih al-Bukhari", "2363"),
    ("Wealth is not in having many possessions. Rather, true wealth is the richness of the soul.", "Sahih Muslim", "1051a"),
    ("Do not wish to be like anyone except in two cases. The first is a person whom Allah has given wealth and he spends it righteously. The second is the one whom Allah has given wisdom and he acts according to it and teaches it to others.", "Sahih al-Bukhari", "73"),
    ("Whoever follows a path in the pursuit of knowledge, Allah will make a path to Paradise easy for him.", "Sahih Muslim", "2699"),
    ("Modesty is part of faith.", "Sahih al-Bukhari", "24"),
    ("The strong man is not the good wrestler; the strong man is only the one who controls himself when he is angry.", "Sahih al-Bukhari", "6114"),
    ("Whosoever relieves a believer's distress of the distressful aspects of this world, Allah will rescue him from a difficulty of the difficulties of the Hereafter.", "Sahih Muslim", "2699"), # Note: Same number as another Muslim hadith, source might have variations.
    ("Visit the sick, feed the hungry, and free the captive.", "Sahih al-Bukhari", "5649")
]

def get_hadiths():
    """Returns the list of Hadiths."""
    # Convert list of tuples to list of dictionaries for easier processing
    hadith_data = [] 
    for text, source, number in hadiths_clean:
        hadith_data.append({
            "text": text,
            "source": source,
            "number": number
        })
    return hadith_data

if __name__ == '__main__':
    # Example usage: Print the hadiths when the script is run directly
    all_hadiths = get_hadiths()
    print(f"Loaded {len(all_hadiths)} Hadiths:")
    for i, hadith in enumerate(all_hadiths):
        print(f"{i+1}. {hadith['source']} {hadith['number']}: {hadith['text'][:50]}...")

