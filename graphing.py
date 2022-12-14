import pandas
import plotly.graph_objects as go
import plotly.io as pio
from dateutil.parser import parse


def __process_table_for_word(word):
    word_row = __get_row_for_word_from_csv(word)
    years = word_row.index.tolist()
    counts = word_row.values.tolist()
    return years, counts


def __process_table_for_word_in_pcm(word):
    word_row = __get_row_for_word_from_csv(word)
    total_row = __get_row_for_word_from_csv("TOTAL")
    years = []
    counts = []
    for year, count in word_row.items():
        years.append(year)
        if count == 0:
            counts.append(0)
        else:
            counts.append((count / total_row[year]) * 100000)
    return years, counts


def __process_table_for_word_with_range_in_pcm(word, start, end):
    word_row = __get_row_for_word_from_csv(word)
    total_row = __get_row_for_word_from_csv("TOTAL")
    start_date = __date_parser(start)
    end_date = __date_parser(end)
    years = []
    counts = []
    for year, count in word_row.items():
        parsed_year = __date_parser(year)
        if start_date <= parsed_year <= end_date:
            years.append(year)
            if count == 0:
                counts.append(0)
            else:
                counts.append((count / total_row[year]) * 100000)
    return years, counts


def __process_table_for_word_with_range(word, start, end):
    word_row = __get_row_for_word_from_csv(word)
    start_date = __date_parser(start)
    end_date = __date_parser(end)
    years = []
    counts = []
    for year, count in word_row.items():
        parsed_year = __date_parser(year)
        if start_date <= parsed_year <= end_date:
            years.append(year)
            counts.append(count)
    return years, counts


def __get_graph_xy(title, x, y, words):
    fig = go.Figure()
    for i in range(len(x)):
        fig.add_trace(go.Scatter(x=x[i], y=y[i], name=words[i]))
    fig.update_layout(title_text=title)
    fig.update_layout(xaxis_title="Zeitpunkt", yaxis_title="Anzahl")
    pio.write_html(fig, file='./graphs/' + title + '.html', auto_open=True)


def __get_row_for_word_from_csv(word):
    result = pandas.read_csv("output-3.csv")
    result.set_index("word", inplace=True)
    return result.loc[word]


def __date_parser(date):
    return parse(date + '-01')


def __get_graph_for_words(words, start, end, function):
    x = []
    y = []
    title = ""
    for word in words:
        if start is None and end is None:
            years, counts = function(word)
        else:
            years, counts = function(word, start, end)
        x.append(years)
        y.append(counts)
        title += word + " "
    title = title[:len(title) - 1]
    if start is None and end is None:
        title = title
    else:
        title = title + " von " + start + " bis " + end
    __get_graph_xy(title, x, y, words)


# creates a graph for the word based on all available data
def get_graph_for_word(word):
    get_graph_for_words([word])


# creates a graph for the list of words based on all available data
def get_graph_for_words(words):
    __get_graph_for_words(words, None, None, __process_table_for_word)


# creates a graph for the word based on the data for the years between start and end
def get_graph_for_word_and_years_range(word, start, end):
    get_graph_for_words_and_years_range([word], start, end)


# creates a graph for the list of words based on the data for the years between start and end
def get_graph_for_words_and_years_range(words, start, end):
    __get_graph_for_words(words, start, end, __process_table_for_word_with_range)


# creates a graph for the word based on all available data using pcm (per cent mile)
# as the unit of measure for the vertical quantity axis
def get_graph_for_word_in_pcm(word):
    get_graph_for_words_in_pcm([word])


# creates a graph for the list of words based on all available data using pcm (per cent mile)
# as the unit of measure for the vertical quantity axis
def get_graph_for_words_in_pcm(words):
    __get_graph_for_words(words, None, None, __process_table_for_word)


# creates a graph for the word based on the data for the years between start and end using pcm (per cent mile)
# as the unit of measure for the vertical quantity axis
def get_graph_for_word_and_years_range_in_pcm(word, start, end):
    get_graph_for_words_and_years_range_in_pcm([word], start, end)


# creates a graph for the list of words based on the data for the years between start and end using pcm (per cent mile)
# as the unit of measure for the vertical quantity axis
def get_graph_for_words_and_years_range_in_pcm(words, start, end):
    __get_graph_for_words(words, start, end, __process_table_for_word_with_range_in_pcm)
