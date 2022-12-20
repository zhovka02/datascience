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

def makeWordcloudImage(text, printOnScreen, outputFile):

    directory = os.getcwd()
    reichstagsMask = np.array(Image.open(path.join(directory, "reichstagsMaskeBlack.jpg")))

    wc = WordCloud(background_color="white", max_words=500, mask=reichstagsMask, contour_width=0.1, contour_color='steelblue')
    # generate word cloud
    wc.generate_from_frequencies(text)

    if printOnScreen:
        # show
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    #save in file
    wc.to_file(outputFile)
    #wordcloud_svg = wc.to_svg(embed_font=True, embed_image=True, optimize_embedded_font=True)
    #f = open("export.svg", "w+")
    #f.write(wordcloud_svg)
    #f.close()

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
    args = parser.parse_args()

    inputFile = args.inputFile
    outputFile = args.outputFile
    printScreen = args.print

    #if inputfile command is empty take output.csv in project root
    if inputFile is None:
        inputFile = 'output2006.csv'

    # if outputfile command is empty take export.png in project root
    if outputFile is None:
        outputFile = "export.png"

    words = getWords(inputFile)

    unsortedDict = {}
    for a in words:
        unsortedDict[remove_umlaut(a)] = words[a]
        unsortedDict[remove_umlaut(a)] = int(unsortedDict[remove_umlaut(a)])

    sortedDict = {}
    for w in sorted(unsortedDict, key=unsortedDict.get, reverse=True):
        sortedDict[w] = unsortedDict[w]

    wordcloud = makeWordcloudImage(sortedDict, printScreen, outputFile)





