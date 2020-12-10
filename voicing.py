import copy
import argparse
import itertools
from fractions import Fraction
from functools import lru_cache
from enum import IntEnum

from music21.layout import StaffGroup
from music21.converter import parse
from music21.note import Note
from music21.pitch import Pitch
from music21.chord import Chord
from music21.roman import RomanNumeral
from music21.key import Key
from music21.meter import TimeSignature
from music21.clef import BassClef, TrebleClef
from music21.instrument import Piano
from music21.stream import Part, Score, Voice
from music21.interval import Interval

from unconventional_chords import unconventional_chords


class PartEnum(IntEnum):
    SOPRANO = 3
    ALTO = 2
    TENOR = 1
    BASS = 0


class IntervalV(IntEnum):
    ALTO_SOPRANO = 5
    TENOR_SOPRANO = 4
    TENOR_ALTO = 3
    BASS_SOPRANO = 2
    BASS_ALTO = 1
    BASS_TENOR = 0


class Cost(IntEnum):
    FORBIDDEN = 64
    VERYBAD = 8
    BAD = 4
    MAYBEBAD = 2
    NOTIDEAL = 1


class Rule(IntEnum):
    # progression-related arules
    IDENTICAL_VOICING = 1
    ALLVOICES_SAME_DIRECTION = 2
    MELODIC_INTERVAL_FORBIDDEN = 3
    MELODIC_INTERVAL_BEYONDOCTAVE = 4
    MELODIC_INTERVAL_BEYONDFIFTH = 5
    MELODIC_INTERVAL_BEYONDTHIRD = 6
    MELODIC_INTERVAL_BEYONDSECOND = 7
    UNISON_BY_LEAP = 8
    PARALLEL_FIFTH = 9
    PARALLEL_OCTAVE = 10
    HIDDEN_FIFTH = 11
    HIDDEN_OCTAVE = 12
    VOICE_CROSSING = 13
    SEVENTH_UNPREPARED = 14
    SEVENTH_UNRESOLVED = 15
    LEADINGTONE_UNRESOLVED = 16
    # voicing-related rules
    VERTICAL_NOT_DOUBLINGROOT = 17
    VERTICAL_SEVENTH_MISSINGNOTE = 18


_ruleCostMapping = {
    # progression rules
    Rule.IDENTICAL_VOICING: Cost.VERYBAD,
    Rule.ALLVOICES_SAME_DIRECTION: Cost.FORBIDDEN,
    Rule.MELODIC_INTERVAL_FORBIDDEN: Cost.FORBIDDEN,
    Rule.MELODIC_INTERVAL_BEYONDOCTAVE: Cost.VERYBAD,
    Rule.MELODIC_INTERVAL_BEYONDFIFTH: Cost.BAD,
    Rule.MELODIC_INTERVAL_BEYONDTHIRD: Cost.MAYBEBAD,
    Rule.MELODIC_INTERVAL_BEYONDSECOND: Cost.NOTIDEAL,
    Rule.UNISON_BY_LEAP: Cost.VERYBAD,
    Rule.PARALLEL_FIFTH: Cost.FORBIDDEN,
    Rule.PARALLEL_OCTAVE: Cost.FORBIDDEN,
    Rule.HIDDEN_FIFTH: Cost.FORBIDDEN,
    Rule.HIDDEN_OCTAVE: Cost.FORBIDDEN,
    Rule.VOICE_CROSSING: Cost.BAD,
    Rule.SEVENTH_UNPREPARED: Cost.BAD,
    Rule.SEVENTH_UNRESOLVED: Cost.VERYBAD,
    Rule.LEADINGTONE_UNRESOLVED: Cost.VERYBAD,
    # voicing rules
    Rule.VERTICAL_NOT_DOUBLINGROOT: Cost.NOTIDEAL,
    Rule.VERTICAL_SEVENTH_MISSINGNOTE: Cost.MAYBEBAD,
}


def applyRule(rule):
    return _ruleCostMapping[rule]


voice_ranges = {
    PartEnum.SOPRANO: (Pitch("C4"), Pitch("G5")),
    PartEnum.ALTO: (Pitch("G3"), Pitch("D5")),
    PartEnum.TENOR: (Pitch("C3"), Pitch("G4")),
    PartEnum.BASS: (Pitch("E2"), Pitch("C4")),
}


verticalHorizontalMapping = {
    IntervalV.ALTO_SOPRANO: (PartEnum.SOPRANO, PartEnum.ALTO),
    IntervalV.TENOR_SOPRANO: (PartEnum.TENOR, PartEnum.SOPRANO),
    IntervalV.TENOR_ALTO: (PartEnum.TENOR, PartEnum.ALTO),
    IntervalV.BASS_SOPRANO: (PartEnum.BASS, PartEnum.SOPRANO),
    IntervalV.BASS_ALTO: (PartEnum.BASS, PartEnum.ALTO),
    IntervalV.BASS_TENOR: (PartEnum.BASS, PartEnum.TENOR),
}


perfectUnison = Interval("P1")

cachedGetChordFromPitches = []
cachedGetKeyFromString = []
cachedGetPitchFromString = []
cachedGetLeadingTone = []
cachedGetVerticalIntervalsFromPitches = []
cachedGetInterval = []
cachedIsTriad = []
cachedVoiceChord = []
cachedProgressionCost = []
cachedChordCost = []


@lru_cache(maxsize=None)
def getChordFromPitches(pitches):
    cachedGetChordFromPitches.append(pitches)
    return Chord(pitches)


@lru_cache(maxsize=None)
def getKeyFromString(key):
    cachedGetKeyFromString.append(key)
    return Key(key)


@lru_cache(maxsize=None)
def getPitchFromString(p):
    cachedGetPitchFromString.append(p)
    return Pitch(p)


@lru_cache(maxsize=None)
def getLeadingTone(key):
    cachedGetLeadingTone.append(key)
    return getKeyFromString(key).getLeadingTone()


@lru_cache(maxsize=None)
def getVerticalIntervalsFromPitches(pitches):
    cachedGetVerticalIntervalsFromPitches.append(pitches)
    return [
        getInterval(pitches[i], pitches[j])
        for i in range(3)
        for j in range(i + 1, 4)
    ]


@lru_cache(maxsize=None)
def getInterval(p1, p2):
    cachedGetInterval.append((p1, p2))
    pitch1 = getPitchFromString(p1)
    pitch2 = getPitchFromString(p2)
    return Interval(noteStart=pitch1, noteEnd=pitch2)


@lru_cache(maxsize=None)
def isTriad(pitches):
    cachedIsTriad.append(pitches)
    return getChordFromPitches(pitches).isTriad()


def _voice(part, voicingSoFar, remainingNotes):
    if not remainingNotes:
        # Time to break the recursion
        pitches = tuple(voicingSoFar)
        intervals = [getInterval(pitches[i], pitches[i + 1]) for i in range(3)]
        if (
            intervals.count(perfectUnison) <= 1
            and 1 <= intervals[1].generic.directed <= 8
            and 1 <= intervals[2].generic.directed <= 8
            # and 1 <= tenorSoprano.generic.directed <= 8
        ):
            yield pitches
        return
    # Keep recursing
    minPitch, maxPitch = voice_ranges[part]
    if voicingSoFar:
        minPitch = max(minPitch, getPitchFromString(voicingSoFar[-1]))
    octaveStart = minPitch.octave
    octaveEnd = maxPitch.octave
    for noteName in sorted(set(remainingNotes)):
        newRemaining = remainingNotes.copy()
        newRemaining.remove(noteName)
        for octave in range(octaveStart, octaveEnd + 1):
            pitchName = f"{noteName}{octave}"
            pitch = getPitchFromString(pitchName)
            if minPitch <= pitch <= maxPitch:
                yield from _voice(
                    part + 1,
                    voicingSoFar + [pitchName],
                    newRemaining,
                )


def _voiceChord(pitches):
    chord = getChordFromPitches(pitches)
    pitchNames = list(chord.pitchNames)
    if isTriad(frozenset(pitchNames)):
        if chord.inversion() != 2:
            doublings = [
                pitchNames + [chord.root().name],
                pitchNames + [chord.fifth.name],
                pitchNames + [chord.third.name],
                pitchNames[:2] + [chord.root().name] * 2,
            ]
        elif chord.inversion() == 2:
            doublings = [
                pitchNames + [chord.root().name],
                pitchNames + [chord.fifth.name],
            ]
    elif chord.isSeventh():
        doublings = [pitchNames]
        # TODO: Alternative doublings
    for doubling in doublings:
        minBassPitch, maxBassPitch = voice_ranges[PartEnum.BASS]
        octaveStart = minBassPitch.octave
        octaveEnd = maxBassPitch.octave
        for octave in range(octaveStart, octaveEnd + 1):
            bassPitchName = doubling[PartEnum.BASS] + str(octave)
            bassPitch = getPitchFromString(bassPitchName)
            if minBassPitch <= bassPitch <= maxBassPitch:
                yield from _voice(
                    PartEnum.TENOR, [bassPitchName], doubling[1:]
                )


@lru_cache(maxsize=None)
def voiceChord(pitches):
    cachedVoiceChord.append(pitches)
    return [v for v in _voiceChord(pitches)]


@lru_cache(maxsize=None)
def progressionCost(key, pitches1, pitches2):
    """An alternative algorithm for computing the cost"""
    cachedProgressionCost.append((key, pitches1, pitches2))
    chord1 = getChordFromPitches(pitches1)
    chord2 = getChordFromPitches(pitches2)
    horizontalIntervals = [
        getInterval(pitches1[i], pitches2[i]) for i in range(4)
    ]
    verticalIntervals1 = getVerticalIntervalsFromPitches(pitches1)
    verticalIntervals2 = getVerticalIntervalsFromPitches(pitches2)

    cost = 0
    # No duplicate chords
    if pitches1 == pitches2:
        cost += applyRule(Rule.IDENTICAL_VOICING)

    # All voices in the same direction
    if (
        horizontalIntervals[PartEnum.BASS].direction
        == horizontalIntervals[PartEnum.TENOR].direction
        == horizontalIntervals[PartEnum.ALTO].direction
        == horizontalIntervals[PartEnum.SOPRANO].direction
    ):
        cost += applyRule(Rule.ALLVOICES_SAME_DIRECTION)

    # Melodic intervals for individual voices
    for n1n2 in horizontalIntervals:
        if (
            n1n2.simpleName == "A2"
            or n1n2.simpleName == "A4"
            or n1n2.simpleName == "D5"
            or n1n2.simpleName == "m7"
            or n1n2.simpleName == "M7"
        ):
            cost += applyRule(Rule.MELODIC_INTERVAL_FORBIDDEN)
        elif abs(n1n2.semitones) > 12:
            cost += applyRule(Rule.MELODIC_INTERVAL_BEYONDOCTAVE)
        elif abs(n1n2.semitones) > 7:
            cost += applyRule(Rule.MELODIC_INTERVAL_BEYONDFIFTH)
        elif abs(n1n2.semitones) > 4:
            cost += applyRule(Rule.MELODIC_INTERVAL_BEYONDTHIRD)
        elif abs(n1n2.semitones) > 2:
            cost += applyRule(Rule.MELODIC_INTERVAL_BEYONDSECOND)

    # Parallel motion and unisons
    for i in range(6):
        i1j1, i2j2 = verticalIntervals1[i], verticalIntervals2[i]
        hLowerIndex, hUpperIndex = verticalHorizontalMapping[i]
        hLower = horizontalIntervals[hLowerIndex]
        hUpper = horizontalIntervals[hUpperIndex]
        # Unison arrival
        if i2j2.name == "P1":
            if hLower.generic.directed != 2 and hUpper.generic.directed != -2:
                cost += applyRule(Rule.UNISON_BY_LEAP)
        # Oblique motion is fine
        elif hLower.name == "P1" or hUpper.name == "P1":
            continue
        # Parallel fifths
        if i1j1.generic.mod7 == 5 and i2j2.generic.mod7 == 5:
            cost += applyRule(Rule.PARALLEL_FIFTH)
        # Parallel octave/unison
        elif i1j1.generic.mod7 == 1 and i2j2.generic.mod7 == 1:
            cost += applyRule(Rule.PARALLEL_OCTAVE)

    # Hidden octaves/fifths in extreme voices
    if (
        verticalIntervals2[IntervalV.BASS_SOPRANO].generic.mod7 == 5
        and horizontalIntervals[PartEnum.BASS].direction
        == horizontalIntervals[PartEnum.SOPRANO].direction
    ):
        cost += applyRule(Rule.HIDDEN_FIFTH)

    if (
        verticalIntervals2[IntervalV.BASS_SOPRANO].generic.mod7 == 1
        and horizontalIntervals[PartEnum.BASS].direction
        == horizontalIntervals[PartEnum.SOPRANO].direction
    ):
        cost += applyRule(Rule.HIDDEN_OCTAVE)

    # Voice crossing
    for i in range(3):
        if (
            horizontalIntervals[i].noteEnd
            > horizontalIntervals[i + 1].noteStart
            or horizontalIntervals[i + 1].noteEnd
            < horizontalIntervals[i].noteStart
        ):
            cost += applyRule(Rule.VOICE_CROSSING)

    # Sevenths preparation
    if chord2.seventh:
        seventhIndex = chord2.pitches.index(chord2.seventh)
        if (
            horizontalIntervals[seventhIndex].generic.directed != 1
            and horizontalIntervals[seventhIndex].generic.undirected != 2
        ):
            cost += applyRule(Rule.SEVENTH_UNPREPARED)

    # Sevenths resolution
    if chord1.seventh:
        seventhIndex = chord1.pitches.index(chord1.seventh)
        if (
            horizontalIntervals[seventhIndex].generic.directed != 1
            and horizontalIntervals[seventhIndex].generic.directed != -2
        ):
            cost += applyRule(Rule.SEVENTH_UNRESOLVED)

    # Leading tone resolution
    k = getKeyFromString(key)
    leadingTone = getLeadingTone(key).name
    root1 = chord1.root().name
    root2 = chord2.root().name
    if root1 == k.pitchFromDegree(5).name or root1 == leadingTone:
        if root2 == k.pitchFromDegree(1).name or root2 == k.pitchFromDegree(6):
            if leadingTone in chord1.pitchNames:
                leadingToneIndex = chord1.pitchNames.index(leadingTone)
                if (
                    horizontalIntervals[leadingToneIndex].name != "m2"
                    and horizontalIntervals[leadingToneIndex].name != "M-3"
                ):
                    cost += applyRule(Rule.LEADINGTONE_UNRESOLVED)

    return cost


@lru_cache(maxsize=None)
def chordCost(pitches):
    """Computes elements of cost that only pertain to a single chord."""
    cachedChordCost.append(pitches)
    chord = getChordFromPitches(pitches)
    cost = 0
    if isTriad(frozenset(chord.pitchNames)):
        if chord.inversion() < 2:
            # In root postion and first inversion, double the root
            if chord.pitchNames.count(chord.root().name) <= 1:
                cost += applyRule(Rule.VERTICAL_NOT_DOUBLINGROOT)
    elif chord.isSeventh():
        # In seventh chords, prefer to play all the notes
        if set(chord.pitchNames) != 4:
            cost += applyRule(Rule.VERTICAL_SEVENTH_MISSINGNOTE)
    return cost


def voiceProgression(romanNumerals):
    """Voices a chord progression in a specified key using DP.

    Follows eighteenth-century voice leading procedures, as guided by the cost
    function defined in the `chordCost` and `progressionCost` functions.
    Returns a list of four-pitch chords, corresponding to successive Roman
    numerals in the chord progression.
    """
    keys = [rn.secondaryRomanNumeralKey or rn.key for rn in romanNumerals]

    dp = [{} for _ in romanNumerals]
    for i, numeral in enumerate(romanNumerals):
        pitches = tuple([p.nameWithOctave for p in numeral.pitches])
        voicings = voiceChord(pitches)
        if i == 0:
            for v in voicings:
                dp[0][v] = (chordCost(v), None)
        else:
            for v in voicings:
                best = (float("inf"), None)
                for pv_pitches, (pcost, _) in dp[i - 1].items():
                    pvkey = keys[i - 1].tonicPitchNameWithCase
                    ccost = pcost + progressionCost(pvkey, pv_pitches, v)
                    if ccost < best[0]:
                        best = (ccost, pv_pitches)
                dp[i][v] = (best[0] + chordCost(v), best[1])

    cur, (totalCost, _) = min(dp[-1].items(), key=lambda p: p[1][0])
    ret = []
    for i in reversed(range(len(romanNumerals))):
        ret.append(Chord(cur))
        cur = dp[i][cur][1]
    return list(reversed(ret)), totalCost


def decorateScore(romantext):  # Previously generateScore
    """Decorate an annotated chorale into piano form.

    Receives a romantext stream that has been properly voiced by the
    dynamic programming algorithm, replacing the 1-part layout with a
    2-part grand staff piano layout in SA-TB form.
    """
    romanNumerals = romantext.recurse().getElementsByClass("RomanNumeral")
    score = romantext.template(fillWithRests=False)
    trebleStaff = score.parts[0]
    bassStaff = copy.deepcopy(trebleStaff)
    trebleStaff[0].insert(0, TrebleClef())
    bassStaff[0].insert(0, BassClef())
    for rn in romanNumerals:
        b, t, a, s = copy.deepcopy(rn.notes)
        b.duration = t.duration = a.duration = s.duration = rn.duration
        b.lyric = rn.lyric
        trebleStaff.measure(rn.measureNumber).insert(rn.offset, s)
        trebleStaff.measure(rn.measureNumber).insert(rn.offset, a)
        bassStaff.measure(rn.measureNumber).insert(rn.offset, t)
        bassStaff.measure(rn.measureNumber).insert(rn.offset, b)
    staffGroup = StaffGroup(
        [trebleStaff, bassStaff], name="Harmonic reduction", symbol="brace"
    )
    score.insert(0, bassStaff)
    score.insert(0, staffGroup)
    for measure in score.recurse().getElementsByClass("Measure"):
        measure.makeVoices(inPlace=True)
    return score


def voiceLeader(romantext):  # Previously generateChorale
    """Produces stylistic voice leading for a given stream of RomanNumerals.

    The input is a stream, parsed from an input RomanText file.
    The chords, time signature and key are all extracted from there.
    """
    romanNumerals = list(
        romantext.recurse().getElementsByClass("RomanNumeral")
    )
    for rn in romanNumerals:
        keyFigure = (rn.key.mode, rn.figure)
        if keyFigure in unconventional_chords:
            rn.figure = unconventional_chords[keyFigure]
    voicings, score = voiceProgression(romanNumerals)
    for idx, romanNumeral in enumerate(romanNumerals):
        romanNumeral.notes = voicings[idx].notes
    score = decorateScore(romantext)
    return score


def main():
    parser = argparse.ArgumentParser(
        description="Generates four-part harmony with idiomatic "
        "voice-leading procedures and dynamic programming."
    )
    parser.add_argument(
        "input",
        type=str,
        nargs="?",
        default="example.rntxt",
        help="A RomanText input file with the chord progression",
    )
    args = parser.parse_args()
    s = parse(args.input, format="rntext")
    voiceLeader(s).show()


if __name__ == "__main__":
    main()
