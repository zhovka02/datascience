import plotly.graph_objects as go
import plotly.io as pio
import pandas

from dateutil.parser import parse


# makes a graph for one word based on all data stored in output.csv
def get_graph_for_word(word):
    word_row = get_row_for_word_from_csv(word)
    years = word_row.index.tolist()
    counts = word_row.values.tolist()
    get_graph_xy(word, years, counts)


# makes a graph for one word based on the data for a certain period of months, which are stored in output.csv
def get_graph_for_word_and_years_range(word, start, end):
    word_row = get_row_for_word_from_csv(word)
    start_date = date_parser(start)
    end_date = date_parser(end)
    years = []
    counts = []
    for year, count in word_row.items():
        parsed_year = date_parser(year)
        if start_date <= parsed_year <= end_date:
            years.append(year)
            counts.append(count)
    get_graph_xy(word + " from " + start + " to " + end, years, counts)


# makes a graph for one word based on all data
# which are stored in output.csv taking into account the total number of words
def get_graph_for_word_divided_by_total_count(word):
    word_row = get_row_for_word_from_csv(word)
    total_row = get_row_for_word_from_csv("TOTAL")
    years = []
    counts = []
    for year, count in word_row.items():
        years.append(year)
        print(float(total_row[year]))
        if count == 0:
            counts.append(0)
        else:
            counts.append((count / total_row[year]))
    get_graph_xy(word, years, counts)


# makes a graph for one word based on the data for a certain period of months,
# which are stored in output.csv taking into account the total number of words
def get_graph_for_word_and_years_range_divided_by_total_count(word, start, end):
    word_row = get_row_for_word_from_csv(word)
    total_row = get_row_for_word_from_csv("TOTAL")
    start_date = date_parser(start)
    end_date = date_parser(end)
    years = []
    counts = []
    for year, count in word_row.items():
        parsed_year = date_parser(year)
        if start_date <= parsed_year <= end_date:
            years.append(year)
            print(float(total_row[year]))
            if count == 0:
                counts.append(0)
            else:
                counts.append((count / total_row[year]))
    get_graph_xy(word + " from " + start + " to " + end, years, counts)


def get_graph_xy(title, x, y):
    fig = go.Figure(go.Scatter(x=x, y=y))
    fig.update_layout(title_text=title)
    pio.write_html(fig, file='./graphs/' + title + '.html', auto_open=True)


def get_row_for_word_from_csv(word):
    result = pandas.read_csv("output.csv")
    result.set_index("word", inplace=True)
    return result.loc[word]


def date_parser(date):
    return parse(date + '-01')
