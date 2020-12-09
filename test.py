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

    def tearDown(self):
        cleanupCache()


if __name__ == "__main__":
    unittest.main()