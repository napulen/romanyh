from urllib.request import urlretrieve
from zipfile import ZipFile
import os

from transposition import transposeRomanText


def downloadAndExtract(listFile=None):
    """Downloads and extracts all RomanText files in When-in-Rome.

    The script gets the latest master branch of the When-in-Rome repository,
    extracts all the RomanText files into a local folder, and returns
    a list with a global path to every file it extracted.

    If `listFile` is provided, the list of files is also written in disk,
    in the location provided by listFile.
    """
    wheninromeURL = (
        "https://github.com/MarkGotham/When-in-Rome/archive/master.zip"
    )

    # Gets the zipped repo in a temporary file
    tmpZipFile, httpResponse = urlretrieve(wheninromeURL)
    # TODO: Maybe handle any issues based on httpResponse
    repo = ZipFile(tmpZipFile)
    directory = []
    for f in sorted(repo.namelist()):
        if "analysis" in f and "feedback_on" not in f and f.endswith("txt"):
            localFileName = repo.extract(f)
            directory.append(localFileName)
    if listFile:
        with open(listFile, "w") as fout:
            fout.write("\n".join(directory))
    return directory


def transposeAll(keys=[]):
    """Transposes every file in the dataset to other keys.

    If keys is not provided, the files will be transposed
    to 12 different keys in the same mode.
    """
    if not os.path.exists("dataset.txt"):
        downloadAndExtract(listFile="dataset.txt")
    with open("dataset.txt") as fd:
        files = fd.read().split("\n")
    if not keys:
        keys = [
            "C",
            "C#",
            "D",
            "Eb",
            "E",
            "F",
            "F#",
            "G",
            "Ab",
            "A",
            "Bb",
            "B",
        ]
    for f in files:
        for k in keys:
            transposed = transposeRomanText(f, k)
            transposedFileName = f.replace(".txt", f"_{k}.txt")
            with open(transposedFileName, "w") as fout:
                fout.write(transposed)


if __name__ == "__main__":
    downloadAndExtract(listFile="dataset.txt")
