# ![romany](romanyhlogo.png)

A voice-leading algorithm that accepts [RomanText](https://doi.org/10.5281/zenodo.3527756) inputs and produces harmonized scores.

Developed by Néstor Nápoles López. A fork of [Eric Zhang's `harmony`](https://github.com/ekzhang/harmony).

Powered by [music21](http://web.mit.edu/music21/).

## Why is it called romanyh?

1. Emphasizes the importance of roman numeral inputs.
2. Anagram of `harmony`.

## Usage

Example input in [RomanText](https://doi.org/10.5281/zenodo.3527756) form:

`example.rntxt`
```
Composer: Néstor Nápoles López
Title: A unit test in C

Time signature: 3/4 

m1 b1 C: I b2 ii b3 iii
m2 b1 IV b2 Cad64 b3 V
m3 vi b2 V6 b3 viio65/i
m4 b1 I6 b3 V
m5 b1 c: i b2 iio b3 III
m6 b1 N6 b2 Cad64 b3 V
m7 b1 It6 b3 V
m8 b1 Fr43 b3 V
m9 b1 Ger65
m10 b1 iv
m11 b1 V b3 V
m12 b1 I
```

### As a stand-alone binary

Generate a 4-part harmonization:

```shell
$ python -m romanyh example.rntxt
```

This generates a [MusicXML](https://www.musicxml.com/) file called `example.xml` within the current directory.

If you have set up `music21` to work with your music notation editor, you can add the `--show` flag:
```shell
$ python -m romanyh example.rntxt --show
```

This will render the harmonized score in your music notation editor (hopefully).

### As a library

`romanyh` exposes two functions: `harmonize` and `harmonizations`. Both receive a path to a [RomanText](https://doi.org/10.5281/zenodo.3527756) file.

```python
import romanyh

inputFile = "example.rntxt"
score = romanyh.harmonize(inputFile)
score.show()
```

The function returns a [music21.stream.Stream](https://web.mit.edu/music21/doc/moduleReference/moduleStream.html) object.

The difference between `harmonize` and `harmonizations` is that the latter is a generator producing a different harmonizations for the same progression:

```python
import romanyh

inputFile = "example.rntxt"
for score in romanyh.harmonizations(inputFile):
    score.show()
```

This is useful when you want to generate alternative harmonizations of the same input.

The harmonizations are sorted according to the voice-leading algorithm. 
You can expect each successive harmonization to be worse than the previous one.

Similarly, you can expect the first harmonization to be the *best* one.

The first harmonization provided by `harmonizations` should always be the same than the one provided by `harmonize`.

## License

Licensed under the [BSD 3-Clause License](LICENSE.txt).
