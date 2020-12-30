import romanyh
import dataset
import os
import re
import sys


# Taken from django
def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        tonic = None
    else:
        tonic = sys.argv[1]
    datasetListFile = "dataset.txt"
    outputFolder = "harmonic_reductions"
    if os.path.isfile(datasetListFile):
        with open(datasetListFile) as fd:
            datasetFiles = fd.read().split("\n")
    else:
        datasetFiles = dataset.downloadAndExtract()
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    for f in datasetFiles:
        for closePosition in [True, False]:
            try:
                s = romanyh.harmonize(f, closePosition, tonic)
            except:
                s = None
                pass
            if s:
                filename, extension = os.path.splitext(f)
                localFileName = "{}_{}{}.musicxml".format(
                    filename.split("Corpus")[1],
                    tonic if tonic else "originalkey",
                    "_closeposition" if closePosition else "",
                )
                localPath = os.path.join(
                    outputFolder, get_valid_filename(localFileName)
                )
                try:
                    s.write(fmt="musicxml", fp=localPath)
                    print(f)
                except:
                    print(f + "\t\tFAILED TO WRITE MUSICXML")
                    pass
            else:
                print(f + "\t\tFAILED")
