# Import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(
        prog = 'CircleGraph CSV Creator',
        description = "Tool to create a circular graph from provided output.csv in the 'wordcloud' format",
        add_help = True
    )

parser.add_argument("-i", "--inputFile", help="Provide a .csv file with the words and frequencies")
parser.add_argument("-o", "--outputFile", help="Provide name and path for the image to be exported")
parser.add_argument("-d", "--description", help="Enter a description for the graph")
parser.add_argument("-l", "--limit", help="Enter value which limits the maximum of words")
parser.add_argument("-t", "--title", help="Enter a title for the graph")
parser.add_argument("-p", "--print", help="Print graph on screen")
args = parser.parse_args()

inputFile = args.inputFile
if inputFile is None:
    inputFile = "outputWC.csv"
outputFile = args.outputFile
if outputFile is None:
    outputFile = "circleExport.png"
description = args.description
if description is None:
    description = ""
limit = args.limit
if limit is None:
    limit = 30
title = args.title
if title is None:
    title = "CircleBar Graph"
printOnScreen = args.print

def get_dict_from_csv_with_limit(csv_file, limit):
    data = pd.read_csv(csv_file, header=0, names=['Word', 'Count'])
    return data.head(limit)


def make_circular_plot(data, title, description):
    plt.figure(figsize=(11, 10))
    ax = plt.subplot(111, polar=True)
    # remove grid
    plt.axis('off')
    plt.title(title, loc='left', fontsize=48)
    plt.figtext(.02, .02, description, horizontalalignment='left')
    plt.tight_layout(pad=0)

    # Set the coordinates limits
    upperLimit = data['Count'].max()
    lowerLimit = data['Count'].min()

    # Let's compute heights: they are a conversion of each item value in those new coordinates
    # In our example, 0 in the dataset will be converted to the lowerLimit (10)
    # The maximum will be converted to the upperLimit (100)
    slope = (upperLimit - lowerLimit) / upperLimit
    heights = slope * data.Count + lowerLimit

    # Compute the width of each bar. In total we have 2*Pi = 360°
    width = 2 * np.pi / len(data.index)

    # Compute the angle each bar is centered on:
    indexes = list(range(1, len(data.index) + 1))
    angles = [element * width for element in indexes]
    angles

    # Draw bars
    bars = ax.bar(
        x=angles,
        height=heights,
        width=width,
        bottom=lowerLimit,
        linewidth=2,
        edgecolor="white",
        label="Test"
    )

    # little space between the bar and the label
    labelPadding = 4

    # Add labels
    for bar, angle, height, label in zip(bars, angles, heights, data["Word"]):

        # Labels are rotated. Rotation must be specified in degrees :(
        rotation = np.rad2deg(angle)

        # Flip some labels upside down
        alignment = ""
        if angle >= np.pi / 2 and angle < 3 * np.pi / 2:
            alignment = "right"
            rotation = rotation + 180
        else:
            alignment = "left"

        # Finally add the labels
        ax.text(
            x=angle,
            y=lowerLimit + bar.get_height() + labelPadding,
            s=label,
            ha=alignment,
            va='center',
            rotation=rotation,
            rotation_mode="anchor")
    #ax.bar_label(bars, padding=10)
    if printOnScreen:
        plt.show()
    plt.savefig(outputFile, format="png", dpi=300)


def main():
    data = get_dict_from_csv_with_limit(inputFile, limit)
    make_circular_plot(data, title, description)


if __name__ == '__main__':
    main()
