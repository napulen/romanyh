import unittest

from romanyh.voicing import Rule
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


class TestRules(unittest.TestCase):
    def test_rule_identical_voicing(self):
        pitches1 = ("C3", "C4", "E4", "G4")
        pitches2 = ("C3", "C4", "E4", "G4")
        key = "C"
        costGT = applyRule(Rule.IDENTICAL_VOICING)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_allvoices_same_direction(self):
        pitches1 = ("E3", "G4", "A4", "C5")
        pitches2 = ("D3", "F4", "G4", "B4")
        key = "C"
        costGT = applyRule(Rule.ALLVOICES_SAME_DIRECTION)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_melodicinterval_forbidden(self):
        pitches1 = ("B3", "D4", "F4", "B4")
        pitches2 = ("B3", "D4", "F4", "A-4")
        key = "c"
        costGT = applyRule(Rule.MELODIC_INTERVAL_FORBIDDEN)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_melodicinterval_beyondoctave(self):
        pitches1 = ("C3", "G4", "C5", "E5")
        pitches2 = ("E4", "G4", "C5", "E5")
        key = "C"
        costGT = applyRule(Rule.MELODIC_INTERVAL_BEYONDOCTAVE)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_melodicinterval_beyondfifth(self):
        pitches1 = ("C3", "G4", "C5", "E5")
        pitches2 = ("C4", "G4", "C5", "E5")
        key = "C"
        costGT = applyRule(Rule.MELODIC_INTERVAL_BEYONDFIFTH)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_melodicinterval_beyondthird(self):
        pitches1 = ("E4", "G4", "C5", "E5")
        pitches2 = ("A3", "F4", "C5", "F5")
        key = "C"
        costGT = applyRule(Rule.MELODIC_INTERVAL_BEYONDTHIRD)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_melodicinterval_beyondsecond(self):
        pitches1 = ("C4", "G4", "C5", "E5")
        pitches2 = ("E4", "G4", "C5", "E5")
        key = "C"
        costGT = applyRule(Rule.MELODIC_INTERVAL_BEYONDSECOND)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_unison_by_leap1(self):
        pitches1 = ("D3", "F4", "A4", "D5")
        pitches2 = ("E3", "G4", "C5", "C5")
        key = "C"
        costGT = applyRule(Rule.UNISON_BY_LEAP) + applyRule(
            Rule.MELODIC_INTERVAL_BEYONDSECOND
        )
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_unison_by_leap2(self):
        pitches1 = ("D3", "F4", "A4", "D5")
        pitches2 = ("D3", "F4", "B4", "B4")
        key = "C"
        costGT = applyRule(Rule.UNISON_BY_LEAP) + applyRule(
            Rule.MELODIC_INTERVAL_BEYONDSECOND
        )
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_parallel_fifth(self):
        pitches1 = ("D3", "B3", "D4", "F4")
        pitches2 = ("C3", "C4", "E4", "G4")
        key = "C"
        costGT = applyRule(Rule.PARALLEL_FIFTH)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_parallel_octave(self):
        pitches1 = ("C4", "G4", "C5", "E5")
        pitches2 = ("B3", "G4", "B4", "E5")
        key = "C"
        costGT = applyRule(Rule.PARALLEL_OCTAVE)
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_hidden_fifth(self):
        pitches1 = ("G3", "C4", "E4", "E4")
        pitches2 = ("B3", "D4", "D4", "F4")
        key = "C"
        costGT = applyRule(Rule.HIDDEN_FIFTH) + applyRule(
            Rule.MELODIC_INTERVAL_BEYONDSECOND
        )
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_hidden_octave(self):
        pitches1 = ("C3", "G4", "C5", "E5")
        pitches2 = ("F3", "A4", "C5", "F5")
        key = "C"
        costGT = applyRule(Rule.HIDDEN_OCTAVE) + applyRule(
            Rule.MELODIC_INTERVAL_BEYONDTHIRD
        )
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_voice_crossing(self):
        pitches1 = ("E3", "G3", "C4", "E4")
        pitches2 = ("A3", "G3", "C4", "E4")
        key = "C"
        costGT = applyRule(Rule.VOICE_CROSSING) + applyRule(
            Rule.MELODIC_INTERVAL_BEYONDTHIRD
        )
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_seventh_unprepared(self):
        pitches1 = ("C3", "E3", "C4", "G4")
        pitches2 = ("C3", "E3", "C4", "B-4")
        key = "C"
        costGT = applyRule(Rule.SEVENTH_UNPREPARED) + applyRule(
            Rule.MELODIC_INTERVAL_BEYONDSECOND
        )
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_seventh_unresolved(self):
        pitches1 = ("C3", "E3", "C4", "B-4")
        pitches2 = ("C3", "E3", "C4", "G4")
        key = "C"
        costGT = applyRule(Rule.SEVENTH_UNRESOLVED) + applyRule(
            Rule.MELODIC_INTERVAL_BEYONDSECOND
        )
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    def test_rule_leadingtone_unresolved(self):
        pitches1 = ("G3", "D4", "F4", "B4")
        pitches2 = ("G3", "C4", "E4", "E5")
        key = "C"
        costGT = applyRule(Rule.LEADINGTONE_UNRESOLVED) + applyRule(
            Rule.MELODIC_INTERVAL_BEYONDTHIRD
        )
        cost = progressionCost(key, pitches1, pitches2)
        self.assertEqual(cost, costGT)

    # TODO: LeadingTone is complex. Needs more test cases

    def test_rule_vertical_not_doublingroot(self):
        pitches = ("E3", "G3", "C4", "E4")
        costGT = applyRule(Rule.VERTICAL_NOT_DOUBLINGROOT)
        cost = chordCost(pitches)
        self.assertEqual(cost, costGT)

    def test_rule_vertical_seventh_missingnote(self):
        pitches = ("G3", "B3", "F4", "G4")
        costGT = applyRule(Rule.VERTICAL_SEVENTH_MISSINGNOTE)
        cost = chordCost(pitches)
        self.assertEqual(cost, costGT)

    def tearDown(self):
        cleanupCache()


if __name__ == "__main__":
    unittest.main()
