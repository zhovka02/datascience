import csv
from os import path
import os
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import multidict as multidict
import argparse

def remove_umlaut(string):
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string


def getWords(csvInputFile):
    with open(csvInputFile, newline='') as csvfile:
        words = dict(filter(None, csv.reader(csvfile)))
        tempList = list(words.items())
        return words

def getFrequencyDictForText(simpleDict):
    fullTermsDict = multidict.MultiDict()
    for key in simpleDict:
        fullTermsDict.add(key, simpleDict[key])
    return fullTermsDict

def getPLTExportPath(outputFile, format):
    split_tup = os.path.splitext(outputFile)
    return "".join(split_tup[0]) + "_PLT_Export" + format

def makeWordcloudImage(text, printOnScreen, outputFile, printName):

    directory = os.getcwd()
    reichstagsMask = np.array(Image.open(path.join(directory, "reichstagsMaskeBlack.jpg")))

    wc = WordCloud(background_color="white",
                   max_words=500,
                   mask=reichstagsMask,
                   contour_width=0.1,
                   contour_color='steelblue',
                   repeat=False,
                   relative_scaling=0.5,
                   scale=1
                   )
    # generate word cloud
    wc.generate_from_frequencies(text)

    plt.figure(figsize=(20, 10))
    plt.imshow(wc)
    plt.tight_layout(pad=0)
    plt.axis("off")
    plt.title(printName, fontsize=60)
    #save in file
    wc.to_file(outputFile)
    secondOutputFile = getPLTExportPath(outputFile, ".png")
    plt.savefig(secondOutputFile, format="png", dpi=300)

    if printOnScreen:
        plt.show()

    return wc


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='WordCloud Creator',
        description="Tool to create a wordcloud for most said words in provided input File",
        add_help= True
    )
    parser.add_argument("-i", "--inputFile", help="Provide a .csv file with the words")
    parser.add_argument("-o", "--outputFile", help="Provide name and path for the export image")
    parser.add_argument("-p", "--print", help="Print image on screen", action='store_true')
    parser.add_argument("-n", "--name", help="Name for wordcloud print")
    args = parser.parse_args()

    inputFile = args.inputFile
    outputFile = args.outputFile
    printScreen = args.print
    printName = args.name

    #if inputfile command is empty take output.csv in project root
    if inputFile is None:
        inputFile = 'output2006.csv'

    # if outputfile command is empty take export.png in project root
    if outputFile is None:
        outputFile = "export.png"

    if printName is None:
        printName = "Wordcloud Bundestag"

    words = getWords(inputFile)

    unsortedDict = {}
    for a in words:
        unsortedDict[remove_umlaut(a)] = words[a]
        unsortedDict[remove_umlaut(a)] = int(unsortedDict[remove_umlaut(a)])

    sortedDict = {}
    for w in sorted(unsortedDict, key=unsortedDict.get, reverse=True):
        sortedDict[w] = unsortedDict[w]

    wordcloud = makeWordcloudImage(sortedDict, printScreen, outputFile, printName)





