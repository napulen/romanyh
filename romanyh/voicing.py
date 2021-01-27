import copy
from functools import lru_cache

from music21.layout import StaffGroup
from music21.note import Note
from music21.pitch import Pitch
from music21.chord import Chord
from music21.key import Key
from music21.clef import BassClef, TrebleClef
from music21.interval import Interval

from .enums import PartEnum, Cost, Rule, IntervalV

_ruleCostMapping = {
    # progression rules
    Rule.IDENTICAL_VOICING: Cost.VERYBAD,
    Rule.ALLVOICES_SAME_DIRECTION: Cost.VERYBAD,
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
    Rule.SUPERTONIC_UNRESOLVED: Cost.VERYBAD,
    # voicing rules
    Rule.VERTICAL_NOT_DOUBLINGROOT: Cost.NOTIDEAL,
    Rule.VERTICAL_SEVENTH_MISSINGNOTE: Cost.MAYBEBAD,
    Rule.VERTICAL_INCOMPLETE_TRIAD: Cost.MAYBEBAD,
}


def applyRule(rule):
    """Given a rule enum, provide the cost of breaking that rule."""
    print(rule)
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
    """Cached method. Calls music21.chord.Chord()."""
    cachedGetChordFromPitches.append(pitches)
    return Chord(pitches)


@lru_cache(maxsize=None)
def getKeyFromString(key):
    """Cached method. Calls music21.key.Key()."""
    cachedGetKeyFromString.append(key)
    return Key(key)


@lru_cache(maxsize=None)
def getPitchFromString(p):
    """Cached method. Calls music21.pitch.Pitch()."""
    cachedGetPitchFromString.append(p)
    return Pitch(p)


@lru_cache(maxsize=None)
def getLeadingTone(key):
    """Cached method. Calls music21.key.Key.getLeadingTone()."""
    cachedGetLeadingTone.append(key)
    return getKeyFromString(key).getLeadingTone()


@lru_cache(maxsize=None)
def getVerticalIntervalsFromPitches(pitches):
    """Cached method. Returns 6 vertical intervals: BT, BA, BS, TA, TS, AS."""
    cachedGetVerticalIntervalsFromPitches.append(pitches)
    return [
        getInterval(pitches[i], pitches[j])
        for i in range(3)
        for j in range(i + 1, 4)
    ]


@lru_cache(maxsize=None)
def getInterval(p1, p2):
    """Cached method. Calls music21.interval.Interval()."""
    cachedGetInterval.append((p1, p2))
    pitch1 = getPitchFromString(p1)
    pitch2 = getPitchFromString(p2)
    return Interval(noteStart=pitch1, noteEnd=pitch2)


@lru_cache(maxsize=None)
def isTriad(pitches):
    """Cached method. Calls music21.chord.Chord.isTriad()."""
    cachedIsTriad.append(pitches)
    return getChordFromPitches(pitches).isTriad()


def _voice(
    part, voicingSoFar, remainingNotes, closePosition=False, allowedUnisons=0
):
    if not remainingNotes:
        # Time to break the recursion
        pitches = tuple(voicingSoFar)
        intervals = [getInterval(pitches[i], pitches[i + 1]) for i in range(3)]
        if not closePosition:
            if (
                intervals.count(perfectUnison) <= allowedUnisons
                and 1 <= intervals[1].generic.directed <= 8
                and 1 <= intervals[2].generic.directed <= 8
            ):
                yield pitches
            return
        else:
            tenorSoprano = getInterval(pitches[1], pitches[3])
            if (
                intervals.count(perfectUnison) <= allowedUnisons
                and 1 <= tenorSoprano.generic.directed <= 8
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
                    closePosition,
                    allowedUnisons,
                )


def _voiceChord(pitches, closePosition=False, allowedUnisons=0):
    chord = getChordFromPitches(pitches)
    pitchNames = list(chord.pitchNames)
    doublings = []
    if isTriad(frozenset(pitchNames)):
        if chord.inversion() != 2:
            doublings = [
                pitchNames + [chord.root().name],
                pitchNames + [chord.fifth.name],
                pitchNames + [chord.third.name],
                pitchNames[:2] + [chord.root().name] * 2,
                [chord.root().name] * 2 + [chord.fifth.name] * 2,
                [chord.root().name] * 3 + [chord.fifth.name],
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
                    PartEnum.TENOR,
                    [bassPitchName],
                    doubling[1:],
                    closePosition,
                    allowedUnisons,
                )


@lru_cache(maxsize=None)
def voiceChord(pitches, closePosition=False, allowedUnisons=0):
    """Cached method. Return the possible voicings for a tuple of pitches."""
    cachedVoiceChord.append(pitches)
    return [v for v in _voiceChord(pitches, closePosition, allowedUnisons)]


@lru_cache(maxsize=None)
def progressionCost(key, pitches1, pitches2):
    """Computes the cost of two successive chords.

    The cost is computed based on voice-leading rules.
    The rules have been implemented from David Huron's
    'Voice Leading: The Science Behind the Musical Art.'

    The rules have been implemented according to the
    descriptions in Chapter 2, with the following exceptions:

    1. Compass rule: E2 instead of F2 on the lower end of the range.
    3. Chord spacing rule: Huron's description implemented as
       "Open position" form. Additionally, "Close position"
       form is implemented, with one octave between the tenor and soprano
       (easy to play on the piano: bass on the left hand and three upper
       voices on the right hand).
    4. By default, unisons are not allowed.
       An option for allowing them is made available. If allowed,
       unisons must they arrive from a third in contrary motion
       and depart to a third in contrary motion.
    5-8. Implemented as follows:
       - Oblique and stepwise melodic motion preferred
       - If not oblique or stepwise, melodic motion by third is preferred
       - If not third, melodic motion by fourth or fifth are preferred
       - If not fourth or fifth, melodic motion by octave is preferred
       - All other melodic motions forbidden (i.e., seventh and beyond octave)
    12. Omitted. Lighter version (rule 11) is implemented.
    13. Applied in octaves and fifths to bass and soprano only.
    14. Not implemented but enforced by rule 11.
        Doubling of chromatic pitches not implemented due to complexity.
    15. Not implemented.
    16. Implementing as described results in forbidding augmented unisons,
        which are necessary for passages with chromatic melodic lines.
        Augmented 4ths, diminished 5ths, and augmented 2nds are forbidden.
    """
    print(pitches1, pitches2)
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
    elif (
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
        elif hLower.direction == 0 or hUpper.direction == 0:
            continue
        # Parallel fifths
        if i1j1.generic.mod7 == 5 and i2j2.generic.mod7 == 5:
            cost += applyRule(Rule.PARALLEL_FIFTH)
        # Parallel octave/unison
        elif i1j1.generic.mod7 == 1 and i2j2.generic.mod7 == 1:
            cost += applyRule(Rule.PARALLEL_OCTAVE)
        if (
            i2j2.generic.mod7 == 5
            and hLower.direction.name == hUpper.direction.name == "ASCENDING"
        ):
            cost += applyRule(Rule.HIDDEN_FIFTH)
        elif (
            i2j2.generic.mod7 == 1
            and hLower.direction.name == hUpper.direction.name == "ASCENDING"
        ):
            cost += applyRule(Rule.HIDDEN_OCTAVE)

    # # Hidden octaves/fifths in extreme voices
    # if (
    #     verticalIntervals2[IntervalV.BASS_SOPRANO].generic.mod7 == 5
    #     and horizontalIntervals[PartEnum.BASS] != perfectUnison
    #     and horizontalIntervals[PartEnum.SOPRANO] != perfectUnison
    #     and horizontalIntervals[PartEnum.BASS].direction
    #     == horizontalIntervals[PartEnum.SOPRANO].direction
    # ):
    #     cost += applyRule(Rule.HIDDEN_FIFTH)

    # if (
    #     verticalIntervals2[IntervalV.BASS_SOPRANO].generic.mod7 == 1
    #     and horizontalIntervals[PartEnum.BASS] != perfectUnison
    #     and horizontalIntervals[PartEnum.SOPRANO] != perfectUnison
    #     and horizontalIntervals[PartEnum.BASS].direction
    #     == horizontalIntervals[PartEnum.SOPRANO].direction
    # ):
    #     cost += applyRule(Rule.HIDDEN_OCTAVE)

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
    supertonic = k.pitchFromDegree(2).name
    root1 = chord1.root().name
    root2 = chord2.root().name
    if root1 == k.pitchFromDegree(5).name or root1 == leadingTone:
        if root2 == k.tonic.name or root2 == k.pitchFromDegree(6):
            if leadingTone in chord1.pitchNames:
                leadingToneIndex = chord1.pitchNames.index(leadingTone)
                if horizontalIntervals[leadingToneIndex].directedName != "m2":
                    cost += applyRule(Rule.LEADINGTONE_UNRESOLVED)
            if supertonic in chord1.pitchNames:
                supertonicIndex = chord1.pitchNames.index(supertonic)
                if horizontalIntervals[supertonicIndex].directedName != "M-2":
                    cost += applyRule(Rule.SUPERTONIC_UNRESOLVED)

    return cost


@lru_cache(maxsize=None)
def chordCost(pitches):
    """Computes the cost of an individual voicing, regardless of context.

    The cost of a single voicing can be evaluated, for example, to prefer
    specific doublings or to prefer spelling all the notes in a seventh chord
    (over, for example, omitting the third or fifth)."""
    cachedChordCost.append(pitches)
    chord = getChordFromPitches(pitches)
    cost = 0
    if chord.seventh:
        if set(chord.pitchNames) != 4:
            cost += applyRule(Rule.VERTICAL_SEVENTH_MISSINGNOTE)
    else:
        if len(set(chord.pitchNames)) != 3:
            cost += applyRule(Rule.VERTICAL_INCOMPLETE_TRIAD)
        if chord.inversion() < 2:
            # In root postion and first inversion, double the root
            if chord.pitchNames.count(chord.root().name) <= 1:
                cost += applyRule(Rule.VERTICAL_NOT_DOUBLINGROOT)
    return cost


def solveProgression(
    romanNumerals,
    closePosition=False,
    firstVoicing=None,
    lastVoicing=None,
    allowedUnisons=0,
):
    """Voices a chord progression in a specified key using DP.

    Follows eighteenth-century voice leading procedures, as guided by the cost
    function defined in the `chordCost` and `progressionCost` functions.
    Returns a list of four-pitch chords, corresponding to successive Roman
    numerals in the chord progression.
    """
    keys = [rn.secondaryRomanNumeralKey or rn.key for rn in romanNumerals]
    costTable = [{} for _ in romanNumerals]
    for i, numeral in enumerate(romanNumerals):
        pitches = tuple([p.nameWithOctave for p in numeral.pitches])
        if i == 0 and firstVoicing:
            voicings = [firstVoicing]
        elif i == (len(romanNumerals) - 1) and lastVoicing:
            voicings = [lastVoicing]
        else:
            voicings = voiceChord(pitches, closePosition, allowedUnisons)
        if i == 0:
            for v in voicings:
                costTable[0][v] = (chordCost(v), None)
        else:
            for v in voicings:
                best = (float("inf"), None)
                for pv_pitches, (pcost, _) in costTable[i - 1].items():
                    pvkey = keys[i - 1].tonicPitchNameWithCase
                    ccost = pcost + progressionCost(pvkey, pv_pitches, v)
                    if ccost < best[0]:
                        best = (ccost, pv_pitches)
                costTable[i][v] = (best[0] + chordCost(v), best[1])
    return costTable


def decorateScore(romantext, progression):
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
    for rn, pitches in zip(romanNumerals, progression):
        b, t, a, s = [Note(p, quarterLength=rn.quarterLength) for p in pitches]
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


def generateHarmonization(costTable):
    """Yields a harmonization from the dynamic-programming cost table.

    The 'best' harmonization is the one with the lowest cost at the
    last chord of the array. Each iteration over the K voicings of
    the last chord yields the best kth solution.
    """
    sortedCosts = sorted(costTable[-1].items(), key=lambda p: p[1][0])
    solutions = len(sortedCosts)
    # progressions = [[] for _ in range(solutions)]
    for topNthAnswer in range(solutions):
        progression = []
        cur, (totalCost, _) = sortedCosts[topNthAnswer]
        for i in reversed(range(len(costTable))):
            progression.append(cur)
            cur = costTable[i][cur][1]
        yield (list(reversed(progression)), totalCost)
        # progressions[topNthAnswer] = (list(reversed(progression)), totalCost)
    return
