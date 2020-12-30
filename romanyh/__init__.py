import copy

from music21.converter import parse, parseData

from .notation import normalizeRomanNumerals
from .voicing import solveProgression
from .voicing import generateHarmonization
from .voicing import decorateScore
from .transposition import transposeRomanText


def harmonizations(inputFile, closePosition=False, tonic=None):
    if tonic:
        transposedRntxt = transposeRomanText(inputFile, tonic)
        romantext = parseData(transposedRntxt, format="rntext")
    else:
        romantext = parse(inputFile, format="rntxt")
    romanNumerals = normalizeRomanNumerals(romantext)
    costTable = solveProgression(romanNumerals, closePosition)
    for progression, cost in generateHarmonization(costTable):
        romantextcopy = copy.deepcopy(romantext)
        score = decorateScore(romantextcopy, progression)
        yield score
    return


def harmonize(inputFile, closePosition=False, tonic=None):
    return next(harmonizations(inputFile, closePosition, tonic))
