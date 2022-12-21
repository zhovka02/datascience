import json
import os
from time import strptime


class Protocol:
    def __init__(self, identifier, datum, bemerkung, titel, text):
        self.identifier = identifier
        self.datum = datum
        self.bemerkung = bemerkung
        self.titel = titel
        self.text = text

    def get_month(self):
        return Month(self.datum.tm_year, self.datum.tm_mon)

    def __str__(self):
        return f"{self.titel} ({self.identifier})"


class Month:
    def __init__(self, year, month):
        self.year = year
        self.month = month


# Extrahiert alle Protokolle
def all_protocols():
    for data in all_protocol_data():
        for protocol in extract_protocols(data):
            yield protocol


# Extrahiert Protokolle aus einem heruntergeladenen JSON-Dokument
def extract_protocols(str_data):
    data = json.loads(str_data)
    for document in data["documents"]:
        if "text" in document:
            datum = strptime(document["datum"], "%Y-%m-%d")
            yield Protocol(document["dokumentnummer"], datum, "", document["titel"], document["text"])


# Liest alle heruntergeladenen Dateien ein
def all_protocol_data():
    directory = "data"
    for path in os.listdir(directory):
        file = open(directory + "/" + path)
        text = file.read()
        yield text
        file.close()
