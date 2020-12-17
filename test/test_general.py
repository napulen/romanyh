import unittest

from music21.chord import Chord
from music21.roman import RomanNumeral

from romanyh.voicing import Cost, Rule
from romanyh.voicing import solveProgression
from romanyh.voicing import applyRule
from romanyh.voicing import getChordFromPitches
from romanyh.voicing import getKeyFromString
from romanyh.voicing import getPitchFromString
from romanyh.voicing import getLeadingTone
from romanyh.voicing import getVerticalIntervalsFromPitches
from romanyh.voicing import getInterval
from romanyh.voicing import isTriad
from romanyh.voicing import voiceChord
from romanyh.voicing import progressionCost
from romanyh.voicing import chordCost


def cleanupCache():
    getChordFromPitches.cache_clear()
    getKeyFromString.cache_clear()
    getPitchFromString.cache_clear()
    getLeadingTone.cache_clear()
    getVerticalIntervalsFromPitches.cache_clear()
    getInterval.cache_clear()
    isTriad.cache_clear()
    voiceChord.cache_clear()
    progressionCost.cache_clear()
    chordCost.cache_clear()


def getCaches():
    return (
        ("getChordFromPitches", getChordFromPitches.cache_info()),
        ("getKeyFromString", getKeyFromString.cache_info()),
        ("getPitchFromString", getPitchFromString.cache_info()),
        ("getLeadingTone", getLeadingTone.cache_info()),
        (
            "getVerticalIntervalsFromPitches",
            getVerticalIntervalsFromPitches.cache_info(),
        ),
        ("getInterval", getInterval.cache_info()),
        ("isTriad", isTriad.cache_info()),
        ("voiceChord", voiceChord.cache_info()),
        ("progressionCost", progressionCost.cache_info()),
        ("chordCost", chordCost.cache_info()),
    )


def romanNumeralsToPitches(romanNumerals):
    pitchTuples = []
    for rn in romanNumerals:
        pitchTuples.append(tuple(p.nameWithOctave for p in rn.pitches))
    return pitchTuples


class TestGeneral(unittest.TestCase):
    def test_voicing_length_strings(self):
        pitches = ("C4", "E4", "G4")
        voicings = voiceChord(pitches)
        self.assertEqual(len(voicings), 43)

    def test_voicing_length_chord(self):
        chord = Chord("C4 E4 G4")
        pitches = [p.nameWithOctave for p in chord.pitches]
        voicings = voiceChord(tuple(pitches))
        self.assertEqual(len(voicings), 43)

    def test_voicing_length_romannumerals(self):
        rn = RomanNumeral("I", "C")
        pitches = [p.nameWithOctave for p in rn.pitches]
        voicings = voiceChord(tuple(pitches))
        self.assertEqual(len(voicings), 43)

    def test_voicing_cost(self):
        chords = {
            ("C3", "C4", "E4", "G4"): 0,
            ("C3", "G3", "E4", "G4"): Cost.NOTIDEAL,
        }
        for pitches, costGT in chords.items():
            with self.subTest(msg=pitches):
                cost = chordCost(pitches)
                self.assertEqual(cost, costGT)

    def test_cache_info(self):
        progression = [
            RomanNumeral("I", "C"),
            RomanNumeral("V", "C"),
        ]
        solveProgression(progression)
        caches = getCaches()
        cachesGT = (
            {"hits": 3956, "misses": 95},  # getChordFromPitches
            {"hits": 1978, "misses": 1},  # getKeyFromString
            {"hits": 905, "misses": 17},  # getPitchFromString
            {"hits": 1977, "misses": 1},  # getLeadingTone
            {"hits": 3867, "misses": 89},  # getVerticalIntervalsFromPitches
            {"hits": 8761, "misses": 114},  # getInterval
            {"hits": 87, "misses": 4},  # isTriad
            {"hits": 0, "misses": 2},  # voiceChord
            {"hits": 0, "misses": 1978},  # progressionCost
            {"hits": 0, "misses": 89},  # chordCost
        )
        for i in range(len(cachesGT)):
            cacheName, cacheInfo = caches[i]
            cacheGT = cachesGT[i]
            with self.subTest(msg=cacheName):
                self.assertEqual(cacheInfo.hits, cacheGT["hits"])
                self.assertEqual(cacheInfo.misses, cacheGT["misses"])

    def test_progression_cost(self):
        pitches1 = ("C3", "C4", "E4", "G4")
        pitches2 = ("G2", "B3", "D4", "G4")
        key = "C"
        costGT = applyRule(Rule.MELODIC_INTERVAL_BEYONDTHIRD)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def tearDown(self):
        cleanupCache()


if __name__ == "__main__":
    unittest.main()
