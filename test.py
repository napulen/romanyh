import unittest

from music21.chord import Chord
from music21.roman import RomanNumeral
from music21.converter import parseData as m21ParseData

from voicing import Cost, Rule
from voicing import voiceProgression
from voicing import applyRule
from voicing import getChordFromPitches
from voicing import getKeyFromString
from voicing import getPitchFromString
from voicing import getLeadingTone
from voicing import getVerticalIntervalsFromPitches
from voicing import getInterval
from voicing import isTriad
from voicing import voiceChord
from voicing import progressionCost
from voicing import chordCost


trivial = """
Composer: Néstor Nápoles López
Title: Changing keys

Time signature: 4/4

m1 b1 C: I b2 I
m2 I b2 I
m3 I
"""

basic = """
Composer: Néstor Nápoles López
Title: Basic

Time signature: 4/4

m1 b1 C: I b3 IV
m2 Cad64 b3 V
m3 I
"""

changingKeys = """
Composer: Néstor Nápoles López
Title: Changing keys

Time signature: 3/4

m1 b1 C: I c: b3 I
m2 C: V c: b3 V
m3 C: I c: b3 I
"""


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
        voiceProgression(progression)
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


class TestTrivialExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testFile = trivial
        cls.voicingsLengthGT = (43, 43, 43, 43, 43)
        cls.cachesGT = (
            {"hits": 3698, "misses": 46},  # getChordFromPitches
            {"hits": 1849, "misses": 1},  # getKeyFromString
            {"hits": 449, "misses": 10},  # getPitchFromString
            {"hits": 1848, "misses": 1},  # getLeadingTone
            {"hits": 3655, "misses": 43},  # getVerticalIntervalsFromPitches
            {"hits": 7799, "misses": 71},  # getInterval
            {"hits": 42, "misses": 2},  # isTriad
            {"hits": 4, "misses": 1},  # voiceChord
            {"hits": 5547, "misses": 1849},  # progressionCost
            {"hits": 172, "misses": 43},  # chordCost
        )

    def setUp(self):
        self.s = m21ParseData(self.testFile, format="romantext")
        self.romanNumerals = [
            rn for rn in self.s.flat.getElementsByClass("RomanNumeral")
        ]

    def test_voicing_length(self):
        pitchTuples = romanNumeralsToPitches(self.romanNumerals)
        for i, pitches in enumerate(pitchTuples):
            voicings = voiceChord(pitches)
            voicingLengthGT = self.voicingsLengthGT[i]
            with self.subTest(msg=str(pitches)):
                self.assertEqual(len(voicings), voicingLengthGT)

    def test_cache_info(self):
        voiceProgression(self.romanNumerals)
        caches = getCaches()
        for i, cache in enumerate(caches):
            cacheName, cacheInfo = cache
            cacheGT = self.cachesGT[i]
            with self.subTest(msg=cacheName):
                self.assertEqual(cacheInfo.hits, cacheGT["hits"])
                self.assertEqual(cacheInfo.misses, cacheGT["misses"])

    def tearDown(self):
        cleanupCache()


class TestBasicExample(TestTrivialExample):
    @classmethod
    def setUpClass(cls):
        cls.testFile = basic
        cls.voicingsLengthGT = (43, 46, 28, 46, 43)
        cls.cachesGT = (
            {"hits": 13064, "misses": 173},  # getChordFromPitches
            {"hits": 6532, "misses": 1},  # getKeyFromString
            {"hits": 1780, "misses": 24},  # getPitchFromString
            {"hits": 6531, "misses": 1},  # getLeadingTone
            {"hits": 12901, "misses": 163},  # getVerticalIntervalsFromPitches
            {"hits": 27617, "misses": 266},  # getInterval
            {"hits": 161, "misses": 6},  # isTriad
            {"hits": 1, "misses": 4},  # voiceChord
            {"hits": 0, "misses": 6532},  # progressionCost
            {"hits": 43, "misses": 163},  # chordCost
        )


class TestChangingKeysExample(TestTrivialExample):
    @classmethod
    def setUpClass(cls):
        cls.testFile = changingKeys
        cls.voicingsLengthGT = (43, 43, 46, 46, 43, 43)
        cls.cachesGT = (
            {"hits": 15842, "misses": 95},  # getChordFromPitches
            {"hits": 7921, "misses": 2},  # getKeyFromString
            {"hits": 1033, "misses": 17},  # getPitchFromString
            {"hits": 7919, "misses": 2},  # getLeadingTone
            {"hits": 15753, "misses": 89},  # getVerticalIntervalsFromPitches
            {"hits": 32469, "misses": 178},  # getInterval
            {"hits": 87, "misses": 4},  # isTriad
            {"hits": 4, "misses": 2},  # voiceChord
            {"hits": 1849, "misses": 7921},  # progressionCost
            {"hits": 175, "misses": 89},  # chordCost
        )


if __name__ == "__main__":
    unittest.main()
