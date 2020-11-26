import copy
import argparse
import logging
import itertools
from fractions import Fraction

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

voice_ranges = (
    (Pitch("C4"), Pitch("G5")),  # Soprano
    (Pitch("G3"), Pitch("D5")),  # Alto
    (Pitch("C3"), Pitch("G4")),  # Tenor
    (Pitch("E2"), Pitch("C4")),  # Bass
)

voicingCache = {}
costCache = {}

logging.basicConfig(filename="example.log", filemode="w", level=logging.DEBUG)


def fetchVoicing(key, chord):
    key_and_chord = (key, chord.figureAndKey)
    if key_and_chord in voicingCache:
        yield from voicingCache[key_and_chord]
    else:
        voicingCache[key_and_chord] = list(voiceChord(key, chord))
        yield from voicingCache[key_and_chord]


def fetchCost(key, chord1, chord2):
    key_and_chords = (key, chord1.pitches, chord2.pitches)
    if key_and_chords in costCache:
        return costCache[key_and_chords]
    else:
        costCache[key_and_chords] = progressionCost(key, chord1, chord2)
        return costCache[key_and_chords]


def _voice(part, voicingSoFar, remainingNotes):
    if part >= 0:
        voiceRange = voice_ranges[part]
        lowerVoice = voicingSoFar[-1]
        octaveStart = max(lowerVoice.octave, voiceRange[0].octave)
        octaveEnd = voiceRange[1].octave
        for noteName in set(remainingNotes):
            newRemaining = remainingNotes.copy()
            newRemaining.remove(noteName)
            for octave in range(octaveStart, octaveEnd + 1):
                pitch = Pitch(noteName, octave=octave)
                if (
                    pitch < lowerVoice
                    or pitch < voiceRange[0]
                    or pitch > voiceRange[1]
                ):
                    continue
                yield from _voice(
                    part - 1, voicingSoFar + [pitch], newRemaining
                )
    else:
        # Time to break the recursion
        notes = [Pitch(n) for n in voicingSoFar]
        intervals = [Interval(notes[i], notes[i + 1]) for i in range(3)]
        if (
            intervals.count(Interval("P1")) <= 1
            and 1 <= intervals[1].generic.directed <= 8
            and 1 <= intervals[2].generic.directed <= 8
        ):
            yield Chord(voicingSoFar)
        return


def voiceChord(key, chord):
    pitchNames = list(chord.pitchNames)
    if chord.isTriad():
        if chord.inversion() != 2:
            doublings = [
                pitchNames + [chord.root().name],
                pitchNames + [chord.fifth.name],
                pitchNames + [chord.third.name],
                pitchNames[:2] + [chord.root().name] * 2,
            ]
        elif chord.inversion() == 2:
            doublings = [pitchNames + [chord.fifth.name]]
    elif chord.isSeventh():
        doublings = [pitchNames]
        # TODO: Although it would be great to have sevenths
        # with omitted notes, they are no longer detected
        # as seventh chords by music21, and that makes it
        # very difficult (atm) to deal with them
        # if chord.inversion() == 0:
        #     root, third, fifth, seventh = pitchNames
        #     doublings += [
        #         [root, third, root, seventh],
        #         [root, root, fifth, seventh],
        #     ]
        # elif chord.inversion() == 1:
        #     third, fifth, seventh, root = pitchNames
        #     doublings += [
        #         [third, root, seventh, root],
        #     ]
        # elif chord.inversion() == 2:
        #     fifth, seventh, root, third = pitchNames
        #     doublings += [
        #         [fifth, seventh, root, root],
        #     ]
        # elif chord.inversion() == 3:
        #     seventh, root, third, fifth = pitchNames
        #     doublings += [
        #         [seventh, root, third, root],
        #         [seventh, root, root, fifth],
        #     ]
    for doubling in doublings:
        bassRange = voice_ranges[3]
        octaveStart = bassRange[0].octave
        octaveEnd = bassRange[1].octave
        for octave in range(octaveStart, octaveEnd + 1):
            noteName = doubling[0]
            pitch = Pitch(noteName, octave=octave)
            if bassRange[0] <= pitch <= bassRange[1]:
                yield from _voice(2, [pitch], doubling[1:])


def progressionCost(key, chord1, chord2):
    """An alternative algorithm for computing the cost"""
    idString = f"{key.tonicPitchNameWithCase}:"
    for i in range(4):
        idString += f" {chord1[i].pitch.nameWithOctave}{chord2[i].pitch.nameWithOctave}"
    if idString == "B-: B-3B-2 B-3B-3 B-3D4 D4F4":
        kp = 1
    logging.info(idString)
    FORBIDDEN = 64
    VERYBAD = 8
    BAD = 4
    MAYBEBAD = 2
    NOTIDEAL = 1
    horizontalIntervals = [Interval(chord1[i], chord2[i]) for i in range(4)]
    verticalIntervals1 = [
        Interval(chord1[i], chord1[j])
        for i in range(3)
        for j in range(i + 1, 4)
    ]
    verticalIntervals2 = [
        Interval(chord2[i], chord2[j])
        for i in range(3)
        for j in range(i + 1, 4)
    ]

    cost = 0
    penalizations = []

    # No duplicate chords
    if chord1.notes == chord2.notes:
        cost += VERYBAD
        penalizations.append("IDENTICAL_VOICING")

    # All voices in the same direction
    if (
        horizontalIntervals[0].direction
        == horizontalIntervals[1].direction
        == horizontalIntervals[2].direction
        == horizontalIntervals[3].direction
    ):
        cost += FORBIDDEN
        penalizations.append("ALLVOICES_SAME_DIRECTION")

    # Melodic intervals for individual voices
    for n1n2 in horizontalIntervals:
        if (
            n1n2.simpleName == "A2"
            or n1n2.simpleName == 'A4'
            or n1n2.simpleName == 'D5'
            or n1n2.simpleName == "m7"
            or n1n2.simpleName == "M7"
        ):
            cost += FORBIDDEN
            penalizations.append("MELODIC_INTERVAL_FORBIDDEN")
        elif abs(n1n2.semitones) > 12:
            cost += VERYBAD
            penalizations.append("MELODIC_INTERVAL_BEYONDOCTAVE")
        elif abs(n1n2.semitones) > 7:
            cost += BAD
            penalizations.append("MELODIC_INTERVAL_BEYONDFIFTH")
        elif abs(n1n2.semitones) > 4:
            cost += MAYBEBAD
            penalizations.append("MELODIC_INTERVAL_BEYONDTHIRD")
        elif abs(n1n2.semitones) > 2:
            cost += NOTIDEAL
            penalizations.append("MELODIC_INTERVAL_BEYONDSECOND")

    # Parallel motion and unison
    for i1j1, i2j2 in zip(verticalIntervals1, verticalIntervals2):
        # Unison arrival
        if (
            i2j2.name == "P1"
            and Interval(i1j1.noteStart, i2j2.noteStart).generic.directed != 2
            and Interval(i1j1.noteEnd, i2j2.noteStart).generic.directed != -2
        ):
            cost += VERYBAD
            penalizations.append("UNISON_BY_LEAP")
        # Oblique motion is fine
        elif i1j1.noteStart == i2j2.noteStart or i1j1.noteEnd == i2j2.noteEnd:
            continue
        # Parallel fifths
        if i1j1.generic.mod7 == 5 and i2j2.generic.mod7 == 5:
            cost += FORBIDDEN
            penalizations.append("PARALLEL_FIFTH")
        # Parallel octave/unison
        elif i1j1.generic.mod7 == 1 and i2j2.generic.mod7 == 1:
            cost += FORBIDDEN
            penalizations.append("PARALLEL_OCTAVE")

    # Hidden octaves/fifths in extreme voices
    if (
        verticalIntervals2[2].generic.mod7 == 5
        and horizontalIntervals[0].direction
        == horizontalIntervals[3].direction
    ):
        cost += FORBIDDEN
        penalizations.append("HIDDEN_FIFTH")

    if (
        verticalIntervals2[2].generic.mod7 == 1
        and horizontalIntervals[0].direction
        == horizontalIntervals[3].direction
    ):
        cost += FORBIDDEN
        penalizations.append("HIDDEN_OCTAVE")

    # Voice crossing
    for i in range(3):
        if (
            horizontalIntervals[i].noteEnd
            > horizontalIntervals[i + 1].noteStart
            or horizontalIntervals[i + 1].noteEnd
            < horizontalIntervals[i].noteStart
        ):
            cost += BAD
            penalizations.append("VOICE_CROSSING")

    # Sevenths preparation
    if chord2.seventh:
        seventhIndex = chord2.pitches.index(chord2.seventh)
        if (
            horizontalIntervals[seventhIndex].generic.directed != 1
            and horizontalIntervals[seventhIndex].generic.undirected != 2
        ):
            cost += BAD
            penalizations.append('SEVENTH_UNPREPARED')
    
    # Sevenths resolution
    if chord1.seventh:
        seventhIndex = chord1.pitches.index(chord1.seventh)
        if (
            horizontalIntervals[seventhIndex].generic.directed != 1
            and horizontalIntervals[seventhIndex].generic.directed != -2
        ):
            cost += VERYBAD
            penalizations.append("SEVENTH_UNRESOLVED")

    # Leading tone resolution
    leadingTone = key.getLeadingTone().name
    root1 = chord1.root().name
    root2 = chord2.root().name
    if root1 == key.pitchFromDegree(5).name or root1 == leadingTone:
        if root2 == key.pitchFromDegree(
            1
        ).name or root2 == key.pitchFromDegree(6):
            if leadingTone in chord1.pitchNames:
                leadingToneIndex = chord1.pitchNames.index(leadingTone)
                if (
                    horizontalIntervals[leadingToneIndex].name != "m2"
                    and horizontalIntervals[leadingToneIndex].name != "M-3"
                ):
                    cost += VERYBAD
                    penalizations.append("LEADINGTONE_UNRESOLVED")

    logging.info(cost)
    for rule in penalizations:
        logging.warning(rule)
    return cost


def chordCost(key, chord):
    """Computes elements of cost that only pertain to a single chord."""
    FORBIDDEN = 64
    VERYBAD = 8
    BAD = 4
    MAYBEBAD = 2
    NOTIDEAL = 1

    idString = f"{key.tonicPitchNameWithCase}:"
    for i in range(4):
        idString += f" {chord[i].pitch.nameWithOctave}"
    if idString == "B-: B-3B-2 B-3B-3 B-3D4 D4F4":
        kp = 1
    logging.info(idString)

    cost = 0
    penalizations = []
    if chord.isTriad():
        if chord.inversion() < 2:
            # In root postion and first inversion, double the root
            if chord.pitchNames.count(chord.root().name) <= 1:
                cost += NOTIDEAL
                penalizations.append('VERTICAL_NOT_DOUBLINGROOT')
    elif chord.isSeventh():
        # In seventh chords, prefer to play all the notes
        if set(chord.pitchNames) != 4:
            cost += MAYBEBAD
            penalizations.append('VERTICAL_SEVENTH_MISSINGNOTE')
    
    logging.info(cost)
    for rule in penalizations:
        logging.warning(rule)

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
        key = keys[i]
        voicings = fetchVoicing(key, numeral)
        if i == 0:
            for v in voicings:
                dp[0][v.pitches] = (chordCost(key, v), None)
        else:
            for v in voicings:
                best = (float("inf"), None)
                for pv_pitches, (pcost, _) in dp[i - 1].items():
                    pv = Chord(pv_pitches)
                    pvkey = keys[i - 1]
                    ccost = pcost + fetchCost(pvkey, pv, v)
                    if ccost < best[0]:
                        best = (ccost, pv_pitches)
                dp[i][v.pitches] = (best[0] + chordCost(key, v), best[1])

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
