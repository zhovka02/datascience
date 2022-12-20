import argparse
import csv
import pandas as pd
from bundesDate import Date

parser = argparse.ArgumentParser(
        prog = 'WordCloud CSV Creator',
        description = "Tool to modify raw output.csv to wordcloud.csv",
        add_help = True
    )

parser.add_argument("-i", "--inputFile", help="Provide a .csv file with the words")
parser.add_argument("-o", "--outputFile", help="Provide name and path for the modified .csv")
parser.add_argument("-s", "--startTime", help="Enter start Time (Column Name from output.csv)")
parser.add_argument("-e", "--endTime", help="Enter end Time (Column Name from output.csv)")
args = parser.parse_args()

inputFile = args.inputFile
if inputFile is None:
    inputFile = "output_raw.csv"
outputFile = args.outputFile
if outputFile is None:
    outputFile = "outputWC.csv"
startTime = args.startTime
if startTime is None:
    startTime = "2006-1"
endTime = args.endTime
if endTime is None:
    endTime = "2022-12"


def get_dict_from_csv(csv_file):
    data = pd.read_csv(csv_file)
    return data


def trim_dict_to_time_span(csv_file, start, end, add):
    data = get_dict_from_csv(csv_file)
    dateRange = get_time_list(start, end)
    dateRange.append("word")
    trimmedData = data[dateRange]
    trimmedData = trimmedData[:-1] #remove last row with total
    if add:
        return add_dict_to_one(trimmedData)
    return trimmedData[{"word", "result"}]


def add_dict_to_one(trimmedData):
    trimmedData["result"] = trimmedData.sum(axis=1, numeric_only=True)
    return trimmedData[["word", "result"]]


def get_time_list(start, end):
    dates = []
    start = string_to_date(start)
    end = string_to_date(end)
    while start <= end:
        dates.append(start.to_string())
        start.count_month_up()
    return dates


def string_to_date(string):
    return Date(int(string.split("-")[0]), int(string.split("-")[1]))


def main():
    dict = trim_dict_to_time_span(inputFile, startTime, endTime, True)
    dict.sort_values(by="result")
    dict.to_csv(outputFile, index=False, header=False)


if __name__ == '__main__':
    main()



