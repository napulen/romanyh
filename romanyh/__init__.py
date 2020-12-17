import copy

from music21.converter import parse

from .notation import normalizeRomanNumerals
from .voicing import solveProgression
from .voicing import generateHarmonization
from .voicing import decorateScore


def harmonize(inputFile):
    romantext = parse(inputFile, format="rntext")
    romanNumerals = normalizeRomanNumerals(romantext)
    costTable = solveProgression(romanNumerals)
    progression, cost = next(generateHarmonization(costTable))
    score = decorateScore(romantext, progression)
    return score


def harmonizations(inputFile):
    romantext = parse(inputFile, format="rntext")
    romanNumerals = normalizeRomanNumerals(romantext)
    costTable = solveProgression(romanNumerals)
    for progression, cost in generateHarmonization(costTable):
        romantextcopy = copy.deepcopy(romantext)
        score = decorateScore(romantextcopy, progression)
        yield score
    return
