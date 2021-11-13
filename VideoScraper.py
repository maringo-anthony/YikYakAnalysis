# Anthony Maringo Alm4cu
import cv2  # for capturing videos
import pytesseract
import os
from datetime import datetime
import glob
import re
from difflib import SequenceMatcher


def frameScreenshots(video_file_name):
    """
    Convert video into frame by frame screenshots

    :param video_file_name: Name of the file to process
    """

    print("Extracting screenshots...")

    vidcap = cv2.VideoCapture(video_file_name)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        count += 1


def screenshotsToText():
    """
    Parse all *.jpgs in the current directory for yaks
    :return: Set of all unique yaks found from screenshots
    """
    yaks = set()

    for screenshot in glob.glob("*.jpg"):
        print("processing", screenshot, "...")

        image_text = pytesseract.image_to_string(screenshot)
        parsed_yaks = parseTextToYaks(image_text)
        yaks.update(parsed_yaks)
        os.remove(screenshot)

    return yaks


def writeYaksToFile(yaks):
    """
    Output set of yaks to file with the current date and time as filename

    :param yaks: Set of individual yaks
    """
    time = datetime.now().strftime("-%m-%d-%H-%M-%S")
    fileName = "yak-text" + time + ".txt"
    with open(fileName, 'w') as out_file:
        for yak in yaks:
            out_file.write(yak + "\n")
    print("Data written to", fileName)


def parseTextToYaks(yakText):
    """
    Clean up raw yik yak text to individual yaks

    :param yakText: Raw text from reading screenshot
    :return: Set of individual yaks as strings
    """
    ret = set()

    yakText = yakText.replace("\n", " ")  # Get rid of weird spacing
    yakText = yakText.strip().split("Report")  # split each yak

    for yak in yakText:  # remove buttons text
        formattedYak = re.sub(r'(\s\d?)*\d+[mh].*', '', yak).strip()
        if formattedYak != "":
            ret.add(formattedYak)

    return ret


def removeLikelyMistakes(yaks):
    """
    Remove likely duplicate yaks from the set due to error in OCR
    :param yaks: Set of yak strings
    :return: Set of yak strings with likely duplicates removed
    """

    list_yaks = list(yaks)
    yaks_to_remove = set()

    # Find yaks with high similarity to others in the set
    for i in range(len(list_yaks)):
        for j in range(i + 1, len(list_yaks)):
            if SequenceMatcher(None, list_yaks[i], list_yaks[j]).ratio() >= .8:
                yaks_to_remove.add(list_yaks[j])

    # Remove them from the set
    for yak in yaks_to_remove:
        yaks.remove(yak)

    return yaks


VIDEO_FILE_NAME = "RPReplay_Final1636681059.MP4"

frameScreenshots(VIDEO_FILE_NAME)
yaks = screenshotsToText()
refined_yaks = removeLikelyMistakes(yaks)
writeYaksToFile(refined_yaks)
