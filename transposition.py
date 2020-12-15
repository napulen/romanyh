import music21
from music21.interval import Interval
from music21.pitch import Pitch
from music21.key import Key
import re
import sys


keysPerPitchClass = {
    0: {"major": "C", "minor": "c"},
    1: {"major": "Db", "minor": "c#"},
    2: {"major": "D", "minor": "d"},
    3: {"major": "Eb", "minor": "eb"},
    4: {"major": "E", "minor": "e"},
    5: {"major": "F", "minor": "f"},
    6: {"major": "F#", "minor": "f#"},
    7: {"major": "G", "minor": "g"},
    8: {"major": "Ab", "minor": "ab"},
    9: {"major": "A", "minor": "a"},
    10: {"major": "Bb", "minor": "bb"},
    11: {"major": "B", "minor": "b"},
}


def findKeysInRomanTextString(rntxt):
    """Get all the keys in a RomanText string.

    Receive a string with valid RomanText content.
    Output a list of all the key changes that happen
    throughout the content.
    """
    return re.findall(r" ([a-gA-G][#b]?): ", rntxt)


def transposeKeys(keys, newTonic):
    """Transpose a list of keys relative to a new tonic."""
    referenceKey = Key(keys[0])
    newTonicKey = Key(newTonic, mode=referenceKey.mode)
    intervalDiff = Interval(referenceKey.tonic, newTonicKey.tonic)
    transposedKeys = [newTonicKey.tonicPitchNameWithCase]
    for k in keys[1:]:
        localKey = Key(k)
        newLocalTonic = localKey.tonic.transpose(intervalDiff)
        newLocalKey = Key(newLocalTonic, mode=localKey.mode)
        if abs(newLocalKey.sharps) >= 7:
            newLocalKey = Key(
                newLocalTonic.getEnharmonic(), mode=localKey.mode
            )
        transposedKeys.append(newLocalKey.tonicPitchNameWithCase)
    transposedKeys = [k.replace("-", "b") for k in transposedKeys]
    return transposedKeys


def transposeRomanText(f, newTonic="C"):
    """Transposes a RomanText file into a different key.

    The transposition is performed in the following way:
    - The first key in the file is taken as the reference key
    - An interval between the reference key and new tonic is computed
    - Every transposed key respects that interval, unless it becomes
      or exceeds a key signature with 7 sharps or 7 flats
    - In that case, the enharmonic spelling is preferred

    The mode of the original key is always respected. That is,
    attempting to transpose an annotation in the key of C Major
    with a newTonic of `a` will result in a transposition to
    A Major. Change of mode is not trivial and it is not addressed
    in this code.
    """
    with open(f) as fd:
        rntxt = fd.read()
    keys = findKeysInRomanTextString(rntxt)
    transposedKeys = transposeKeys(keys, transPitchClass)
    keysString = [f" {k}: " for k in keys]
    transposedKeysString = [f" {k}: " for k in transposedKeys]
    for original, transposed in zip(keysString, transposedKeysString):
        rntxt = rntxt.replace(original, transposed, 1)
    return rntxt


if __name__ == "__main__":
    inputFile = sys.argv[1]
    pc = int(sys.argv[2])
    transposedRntxt = transposeRomanText(inputFile, pc)
    print(transposedRntxt)
