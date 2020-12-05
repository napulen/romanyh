# romanyh

A voice-leading algorithm that accepts [RomanText](https://doi.org/10.5281/zenodo.3527756) inputs and produces harmonized scores.

Developed by Néstor Nápoles López. Forked from [Eric Zhang's project](https://github.com/ekzhang/harmony).

## Why is it called romanyh?

1. Emphasizes the importance of roman numeral inputs.
2. Anagram of [harmony](https://github.com/ekzhang/harmony), the repository that `romanyh` is based on.


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

To generate a 4-part harmonization:

```shell
$ python voicing.py example.rntxt
```

## License

Licensed under the [BSD 3-Clause License](LICENSE.txt).
