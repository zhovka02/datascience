import requests

api_url = "https://search.dip.bundestag.de/api/v1"
api_key = "GmEPb1B.bfqJLIhcGAsH9fTJevTglhFpCoZyAAAdhp"


# Läd ein Plenarprotokoll nach ID herunter
def request_resource(resource_id):
    url = "{}/plenarprotokoll/{}?apikey={}"
    print(url.format(api_url, resource_id, api_key))
    response = requests.get(url.format(api_url, resource_id, api_key))
    return response.json()


# Läd ein Plenarprotokoll nach Datumsrange herunter. Datumsformat "YYYY-MM-DD"
def request_date_range(start, end):
    url = "{}/plenarprotokoll-text?f.datum.start={}&f.datum.end={}&apikey={}"
    formatted = url.format(api_url, start, end, api_key)
    print(formatted)
    response = requests.get(formatted)
    return response.json()