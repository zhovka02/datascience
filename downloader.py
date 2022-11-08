import bundestag
import json

min_year = 2006
max_year = 2023


# Läd alle Plenarprotokolle herunter und speichert es in Textdateien
def mass_download():
    gen = generate_day_ranges()
    for from_date, to_date in gen:
        print(f"Downloading {from_date}..{to_date}")
        save_documents_to_file(from_date, to_date)


# Läd die Plenarprotokolle einer Datums-Range und speichert sie in eine Textdatei
def save_documents_to_file(from_date, to_date):
    data = bundestag.request_date_range(from_date, to_date)
    save_data(from_date, data)


# Speichert einen JSON in einer Textdatei
def save_data(name, data):
    f = open(name + ".txt", "x")
    f.write(json.dumps(data, sort_keys=True, indent=4))
    f.close()


# Generiert Ranges von Tagen. Der Generator gibt pro Eintrag jeweils zwei Strings im Format "YYYY-MM-DD" zurück
def generate_day_ranges():
    for year in range(min_year, max_year):
        for month in range(1, 13):
            fromYear = year
            toYear = year
            fromMonth = month
            toMonth = month + 1
            if toMonth > 12:
                toYear = toYear + 1
                toMonth = 1
            for day in range(2, 27):
                yield f"{format(fromYear)}-{format(fromMonth)}-{format(day)}", f"{format(fromYear)}-{format(fromMonth)}-{format(day)}"
            yield f"{format(fromYear)}-{format(fromMonth)}-28", f"{format(toYear)}-{format(toMonth)}-01"


# Formatiert eine Zahl, sodass sie immer zwei Stellen lang ist
def format(number):
    return '{:0>2}'.format(number)
