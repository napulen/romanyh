import unittest

from romanyh.transposition import findKeysInRomanTextString
from romanyh.transposition import transposeKeys

transpositionTest = """
Composer: Néstor Nápoles López
Title: Changing keys

Time signature: 4/4

m1 b1 C: I a: b4 i
m2 G: I e: b3 i
m3 b1 D: I b: b4 I
m4 A: I f#: b3 i
m5 b1 E: I c#: b4 i
Note: Moving to the flat side here
m6 B: I ab: b3 i
m7 b1 Gb: I eb: b4 i
m8 Db: I bb: b3 i
m9 b1 Ab: I f: b4 i
m10 Eb: I c: b3 i
m11 b1 Bb: I g: b4 i
m12 F: I d: b3 i
m13 b1 C: I a: b3 i
"""


class TestTransposition(unittest.TestCase):
    def test_get_keys(self):
        keysGT = (
            "C",
            "a",
            "G",
            "e",
            "D",
            "b",
            "A",
            "f#",
            "E",
            "c#",
            "B",
            "ab",
            "Gb",
            "eb",
            "Db",
            "bb",
            "Ab",
            "f",
            "Eb",
            "c",
            "Bb",
            "g",
            "F",
            "d",
            "C",
            "a",
        )
        keys = findKeysInRomanTextString(transpositionTest)
        self.assertEqual(tuple(keys), keysGT)

    def test_transpose_keys_flat(self):
        keys = findKeysInRomanTextString(transpositionTest)
        transposedKeysGT = (
            "Db",
            "bb",
            "Ab",
            "f",
            "Eb",
            "c",
            "Bb",
            "g",
            "F",
            "d",
            "C",
            "a",
            "G",
            "e",
            "D",
            "b",
            "A",
            "f#",
            "E",
            "c#",
            "B",
            "g#",
            "Gb",
            "eb",
            "Db",
            "bb",
        )
        transposedKeys = transposeKeys(keys, "Db")
        self.assertEqual(tuple(transposedKeys), transposedKeysGT)

    def test_transpose_keys_sharp(self):
        keys = findKeysInRomanTextString(transpositionTest)
        transposedKeysGT = (
            "B",
            "g#",
            "F#",
            "d#",
            "Db",
            "bb",
            "Ab",
            "f",
            "Eb",
            "c",
            "Bb",
            "g",
            "F",
            "d",
            "C",
            "a",
            "G",
            "e",
            "D",
            "b",
            "A",
            "f#",
            "E",
            "c#",
            "B",
            "g#",
        )
        transposedKeys = transposeKeys(keys, "b")
        self.assertEqual(tuple(transposedKeys), transposedKeysGT)


if __name__ == "__main__":
    unittest.main()
