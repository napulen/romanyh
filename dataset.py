from urllib.request import urlretrieve
from zipfile import ZipFile


def downloadAndExtract(listFile="dataset.txt"):
    """Downloads and extracts all RomanText files in When-in-Rome.

    The script gets the latest master branch of the When-in-Rome repository,
    extracts all the RomanText files into a local folder, and generates
    a file `dataset.txt` with a global path to every file it extracted.

    The name of the listFile generated can be optionally provided.
    """
    wheninromeURL = (
        "https://github.com/MarkGotham/When-in-Rome/archive/master.zip"
    )

    # Gets the zipped repo in a temporary file
    tmpZipFile, httpResponse = urlretrieve(wheninromeURL)
    # TODO: Maybe handle any issues based on httpResponse
    repo = ZipFile(tmpZipFile)
    directory = []
    for f in repo.namelist():
        if "analysis" in f and "feedback_on" not in f and f.endswith("txt"):
            localFileName = repo.extract(f)
            directory.append(localFileName)
    with open("dataset.txt", "w") as fout:
        fout.write("\n".join(directory))


if __name__ == "__main__":
    downloadAndExtract()
