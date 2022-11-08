import downloader
import bundestag

currentFunctionUsed = None


class Protocols:
    def __init__(self, identifier, datum, bemerkung, titel, text):
        self.identifier = identifier
        self.datum = datum
        self.bemerkung = bemerkung
        self.titel = titel
        self.text = text

    def __str__(self):
        return f"{self.titel} ({self.identifier})"


def extract_documents(data):
    protocols = []
    for document in data["documents"]:
        protocols.append(Protocols(document["dokumentnummer"], document["datum"], "", document["titel"], document["text"]))
    return protocols


if __name__ == '__main__':
    downloader.mass_download()
