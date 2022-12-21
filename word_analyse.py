import re

import protocol
from nltk.stem.snowball import SnowballStemmer


min_count = 3000


def analyse_word_counts():
    # make word counts
    word_counts = {}
    for month, word in get_all_words_by_month():
        month_id = f"{month.year}-{month.month}"
        if word in word_counts:
            month_counts = word_counts.get(word)
            if month_id in month_counts:
                month_counts[month_id] = month_counts[month_id] + 1
            else:
                month_counts[month_id] = 1
        else:
            word_counts[word] = {month_id: 1}

    print(f"Found {len(word_counts)} words")

    # Total Line
    print("Finding total number of words per month")
    per_month = {}
    for word in word_counts:
        month_counts = word_counts[word]
        for month_id in month_counts:
            if month_id in per_month:
                per_month[month_id] = per_month[month_id] + month_counts[month_id]
            else:
                per_month[month_id] = month_counts[month_id]
    word_counts["TOTAL"] = per_month

    # Wörter, die nicht oft genug gesagt wurden RAUS
    print("Finding removable words")
    words_to_be_removed = []
    for word in word_counts:
        month_counts = word_counts[word]
        word_sum = 0
        for month_id in month_counts:
            month_count = month_counts[month_id]
            word_sum = word_sum + month_count
        if word_sum < min_count:
            words_to_be_removed.append(word)

    print(f"Removing {len(words_to_be_removed)} words")
    for word in words_to_be_removed:
        del word_counts[word]

    print(f"Now we have only {len(word_counts)} words")

    # write result to output file
    print("Writing them to a file")
    output = open("output.csv", "w+")

    # write header
    output.write("word")
    for month_id in get_all_month_ids():
        output.write(",")
        output.write(month_id)
    output.write("\n")

    # write values
    for word in word_counts:
        month_counts = word_counts[word]
        output.write(word)
        for month_id in get_all_month_ids():
            output.write(",")
            if month_id in month_counts:
                output.write(str(month_counts[month_id]))
            else:
                output.write("0")
        output.write("\n")

    output.close()

    print("Finished :)")


def get_all_month_ids():
    for year in range(2006, 2023):
        for month in range(1, 13):
            yield f"{year}-{month}"


def get_all_words_by_month():
    excluded = get_excluded_words()
    stemmer = SnowballStemmer("german")
    index = 0
    for doc in protocol.all_protocols():
        if "Deutschen Bundestages" in doc.titel:  # alle, Dokumente ausschließen, die nicht vom Bundestag kommen
            month = doc.get_month()
            processed = preprocess_text(doc.titel, doc.text)
            index = index + 1
            print(f"i={index} processing {doc.titel}")
            for word in processed.split(" "):
                word = word.lower()
                if len(word) >= 2 and word not in excluded:  # mindestens 3 Buchstaben und nicht ausgeschlossen
                    word = stemmer.stem(word) # Wort auf den Wortstamm zurückführen
                    yield month, word


def get_excluded_words():
    f = open("excluded.txt")
    excluded = f.read().split("\n")
    f.close()
    return excluded


def preprocess_text(title, text):
    if "Beginn:" not in text or "(Schluss" not in text:
        print(f"Didnt find start or end in document {title}")
        return ""
    start_idx = text.index("Beginn:")
    end_idx = text.index("(Schluss")
    text = text[start_idx:end_idx]
    text = text.replace("-\n", "")  # Gebrochene Wörter zusammensetzen
    text = text.replace("\n", " ")  # Zeilenumbrüche eliminieren
    text = re.sub("\\([^)]*\\)", "", text)  # alle Ausdrücke in Klammern entfernen z.B. (Beifall von der SPD)
    text = re.sub("Deutscher Bundestag . \\d+ ?\\. Wahlperiode . \\d+ ?\\. Sitzung ?\\. Berlin, "
                  "\\w+, den \\d+ ?\\. \\w+ \\d\\d\\d\\d", "", text)  # Kopfzeilen eliminieren
    text = re.sub("[^a-zA-ZöäüÖÄÜß\\- ]", "", text)  # Sonderzeichen eliminieren

    return text
