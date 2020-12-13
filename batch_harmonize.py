import voicing
import dataset
import os
import re


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
    datasetListFile = "dataset.txt"
    outputFolder = "harmonic_reductions"
    if os.path.isfile(datasetListFile):
        with open(datasetListFile) as fd:
            datasetFiles = fd.read().split("\n")
    else:
        datasetFiles = dataset.downloadAndExtract()
    for f in datasetFiles:
        try:
            s = voicing.harmonizeFile(f)
        except:
            s = None
            pass
        if s:
            if not os.path.exists(outputFolder):
                os.makedirs(outputFolder)
            localFileName = os.path.join(outputFolder, get_valid_filename(f))
            try:
                s.write(fmt="musicxml", fp=localFileName)
                print(f)
            except:
                print(f + "\t\tFAILED TO WRITE MUSICXML")
                pass
        else:
            print(f + "\t\tFAILED")
