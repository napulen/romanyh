import unittest
from music21.chord import Chord
from music21.pitch import Pitch
from music21.roman import RomanNumeral
from music21.converter import parse

from voicing import Cost
import voicing

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
    voicing.getChordFromPitches.cache_clear()
    voicing.getKeyFromString.cache_clear()
    voicing.getPitchFromString.cache_clear()
    voicing.getLeadingTone.cache_clear()
    voicing.getVerticalIntervalsFromPitches.cache_clear()
    voicing.getInterval.cache_clear()
    voicing.isTriad.cache_clear()
    voicing.voiceChord.cache_clear()
    voicing.progressionCost.cache_clear()
    voicing.chordCost.cache_clear()


def getCaches():
    return (
        ("getChordFromPitches", voicing.getChordFromPitches.cache_info()),
        ("getKeyFromString", voicing.getKeyFromString.cache_info()),
        ("getPitchFromString", voicing.getPitchFromString.cache_info()),
        ("getLeadingTone", voicing.getLeadingTone.cache_info()),
        (
            "getVerticalIntervalsFromPitches",
            voicing.getVerticalIntervalsFromPitches.cache_info(),
        ),
        ("getInterval", voicing.getInterval.cache_info()),
        ("isTriad", voicing.isTriad.cache_info()),
        ("voiceChord", voicing.voiceChord.cache_info()),
        ("progressionCost", voicing.progressionCost.cache_info()),
        ("chordCost", voicing.chordCost.cache_info()),
    )


class TestGeneral(unittest.TestCase):
    def test_voicing_length_strings(self):
        pitches = ("C4", "E4", "G4")
        voicings = voicing.voiceChord(pitches)
        self.assertEqual(len(voicings), 43)

    def test_voicing_length_music21(self):
        chord = Chord("C4 E4 G4")
        pitches = [p.nameWithOctave for p in chord.pitches]
        voicings = voicing.voiceChord(tuple(pitches))
        self.assertEqual(len(voicings), 43)

    def test_voicing_length_romannumerals(self):
        rn = RomanNumeral("I", "C")
        pitches = [p.nameWithOctave for p in rn.pitches]
        voicings = voicing.voiceChord(tuple(pitches))
        self.assertEqual(len(voicings), 43)

    def test_voicing_cost_strings(self):
        chords = {
            ("C3", "C4", "E4", "G4"): 0,
            ("C3", "G3", "E4", "G4"): Cost.NOTIDEAL,
        }
        for pitches, costGT in chords.items():
            with self.subTest(msg=pitches):
                cost = voicing.chordCost(pitches)
                self.assertEqual(cost, costGT)

    def test_cache_info(self):
        progression = [
            RomanNumeral("I", "C"),
            RomanNumeral("V", "C"),
        ]
        voicing.voiceProgression(progression)
        caches = getCaches()
        cachesGT = (
            {"hits": 3956, "misses": 95, "currsize": 95},
            {"hits": 1978, "misses": 1, "currsize": 1},
            {"hits": 905, "misses": 17, "currsize": 17},
            {"hits": 1977, "misses": 1, "currsize": 1},
            {"hits": 3867, "misses": 89, "currsize": 89},
            {"hits": 8761, "misses": 114, "currsize": 114},
            {"hits": 87, "misses": 4, "currsize": 4},
            {"hits": 0, "misses": 2, "currsize": 2},
            {"hits": 0, "misses": 1978, "currsize": 1978},
            {"hits": 0, "misses": 89, "currsize": 89},
        )
        for i in range(len(cachesGT)):
            cacheName, cacheInfo = caches[i]
            cacheGT = cachesGT[i]
            with self.subTest(msg=cacheName):
                self.assertEqual(cacheInfo.hits, cacheGT["hits"])
                self.assertEqual(cacheInfo.misses, cacheGT["misses"])
                self.assertEqual(cacheInfo.currsize, cacheGT["currsize"])

    def test_progression_cost(self):
        pitches1 = ("C3", "C4", "E4", "G4")
        pitches2 = ("G2", "B3", "D4", "G4")
        key = "C"
        costGT = voicing.applyRule(voicing.Rule.MELODIC_INTERVAL_BEYONDTHIRD)
        cost = voicing.progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def tearDown(self):
        cleanupCache()


# class TestBasic(unittest.TestCase):
#     def test_cache_info(self):
#         progression = [
#             RomanNumeral("I", "C"),
#             RomanNumeral("IV", "C"),
#             RomanNumeral("Cad64", "C"),
#             RomanNumeral("V", "C"),
#             RomanNumeral("I", "C"),
#         ]
#         voicing.voiceProgression(progression)
#         caches = (
#             ("getChordFromPitches", voicing.getChordFromPitches.cache_info()),
#             ("getKeyFromString", voicing.getKeyFromString.cache_info()),
#             ("getPitchFromString", voicing.getPitchFromString.cache_info()),
#             ("getLeadingTone", voicing.getLeadingTone.cache_info()),
#             (
#                 "getVerticalIntervalsFromPitches",
#                 voicing.getVerticalIntervalsFromPitches.cache_info(),
#             ),
#             ("getInterval", voicing.getInterval.cache_info()),
#             ("isTriad", voicing.isTriad.cache_info()),
#             ("voiceChord", voicing.voiceChord.cache_info()),
#             ("progressionCost", voicing.progressionCost.cache_info()),
#             ("chordCost", voicing.chordCost.cache_info()),
#         )
#         cachesGT = (
#             {"hits": 13064, "misses": 173, "currsize": 173},
#             {"hits": 6532, "misses": 1, "currsize": 1},
#             {"hits": 1780, "misses": 24, "currsize": 24},
#             {"hits": 6531, "misses": 1, "currsize": 1},
#             {"hits": 12901, "misses": 163, "currsize": 163},
#             {"hits": 27617, "misses": 266, "currsize": 266},
#             {"hits": 161, "misses": 6, "currsize": 6},
#             {"hits": 1, "misses": 4, "currsize": 4},
#             {"hits": 0, "misses": 6532, "currsize": 6532},
#             {"hits": 43, "misses": 163, "currsize": 163},
#         )
#         for i in range(len(cachesGT)):
#             cacheName, cacheInfo = caches[i]
#             cacheGT = cachesGT[i]
#             with self.subTest(msg=cacheName):
#                 self.assertEqual(cacheInfo.hits, cacheGT["hits"])
#                 self.assertEqual(cacheInfo.misses, cacheGT["misses"])
#                 self.assertEqual(cacheInfo.currsize, cacheGT["currsize"])

#     def tearDown(self):
#         cleanupCache()


# class TestExampleTrivial(unittest.TestCase):
#     def setUp(self):
#         self.s = parse(trivial, format="romantext")
#         self.romanNumerals = [
#             rn for rn in self.s.flat.getElementsByClass("RomanNumeral")
#         ]
#         self.pitches = [rn.pitches for rn in self.romanNumerals]
#         self.pitchTuples = []
#         for pitches in self.pitches:
#             self.pitchTuples.append(tuple([p.nameWithOctave for p in pitches]))

#     def test_voicing_length(self):
#         voicings = voicing.voiceChord(self.pitchTuples[0])
#         self.assertEqual(len(voicings), 43)

#     def tearDown(self):
#         cleanupCache()


# class TestCaching(unittest.TestCase):
#     def test_caching(self):
#         self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()