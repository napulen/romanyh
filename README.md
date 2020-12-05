# Comparison with Eric Zhang's algorithm

The voicing of individual chords has been simplified/optimized.

The original algorithm duplicates several voicings, particularly when there is a doubling of the same scale degree.

A query for all possible voicings of a `C Major` triad in the context of the `C Major` key throws 73 results.

In the simplified/optimized version. There are 27 possible voicings. Beside handling the duplicates, a few other 
changes have been made
- Voicings with three voices in unison (i.e., tripling the root but all voices doing doubling it in the same note) have been removed
  - It would be difficult to imagine any scenario where that voicing is useful. It also degrades 4-part writing into 2-part writing

The simplified algorithm is recursive, it requires less code, and runs ~2.7x faster, according to the following test:

```python
>>> import music21
>>> import voicing
>>> import timeit
>>> s = """\
import music21
import voicing
 
list(voicing.voiceChord(music21.key.Key('C'), music21.roman.RomanNumeral('I', 'C')))
"""
>>> s2 = s1.replace('Chord(', 'Chord2(')

>>> timeit.timeit(stmt=s, number=100)
4.010645985999872

>>> timeit.timeit(stmt=s2, number=100)
1.5458245070003613
```
# How does the algorithm work?

Three steps:

1. Given a roman numeral and key, filter all possible voicings for that chord
  - The ranges of the voices should be taken into account
  - Basic checks should be done (e.g., bass is lower than the tenor)
  - Allow to omit the third/fifth depending on the inversion
  - Allow unisons, but not 3 voices playing the same note

The result of that process will provide a clean, curated list of possible voicings.

The idea is that all of the voicings from this list are **valid** voicings.

2. Given each of the possible voicings for a chord, penalize the ones that depart from stylistic conventions
  - A root position chord doubling the third is *valid* but also **unlikely**
  - A seventh chord that omits the fifth is *valid* but playing all the notes is preferred
  - Etcetera

The idea is that all the voicings are ranked according to whether they are, by themselves, **stylistic**. 

A non-conventional voicing should be an option under special circumstances (which the algorithm will decide). 

By default, chords that are stylistic will be preferred.

1. For each pair of ranked voicings in two contiguous roman numerals, penalize connected voicings with bad voice leading.
  - The "meat" of the algorithm.
  - Almost every check can be derived from 16 intervals
  - Horizontal intervals
    - B1 to B2
    - T1 to T2
    - A1 to A2
    - S1 to S2
  - Vertical intervals 1
    - B1 to T1
    - B1 to A1
    - B1 to S1
    - T1 to A1
    - T1 to S1
    - A1 to S1
  - Vertical intervals 2
    - B2 to T2
    - B2 to A2
    - B2 to S2
    - T2 to A2
    - T2 to S2
    - A2 to S2
  - Horizontal rules
    - A4 is forbidden
    - D5 is forbidden
    - A2 is forbidden
  - Parallel motion
    - Parallel fifths are forbidden
    - Parallel octaves are forbidden
    - Hidden fifths are forbidden between extreme voices
    - Hidden octaves are forbidden between extreme voices
    - Unisons are forbidden unless they come from a third that resolves stepwise in both voices
      - This rule was added because the algorithm quickly figured out how to "abuse" of oblique motion to reduce the texture to 3-part writing with unison jumps from one voice to another
  - Resolution
    - Leading tone should resolve to the tonic or the fifth
    - The seventh can't go anywhere but a descending second or remain in the same place (oblique motion)  
