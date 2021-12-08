from dataclasses import dataclass
from collections import Counter

RAW = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def count_1478(raw: str) -> int:
    digits = raw.split(" | ")[-1].split()
    return sum(len(digit) in (2, 3, 4, 7) for digit in digits)

DISPLAYS = RAW.splitlines()
assert sum(count_1478(display) for display in DISPLAYS) == 26


"""

acdg

0: ag
1: c
2: acdg
3: acdg
4: cd
5: adg
6: adg
7: a
8: acdg
9: acdg


 0:6     1+      2:+     3:5     4+
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:5     6:6      7+      8+      9:6
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

e: 4
b: 6

d: 7
g: 7

# c: 8
# a: 8

f: 9


"""
def wires_to_int(wires: str) -> str:
    return {
        "abcefg": "0",
        "cf": "1",
        "acdeg": "2",
        "acdfg": "3",
        "bcdf": "4",
        "abdfg": "5",
        "abdefg": "6",
        "acf": "7",
        "abcdefg": "8",
        "abcdfg": "9"
    }[wires]

def decode(raw: str) -> int:
    digits = raw.split(" | ")[0].split()
    counts = Counter(c for digit in digits for c in digit)
    mapping = {}
    for wire in 'abcdefg':
        if counts[wire] == 4:
            mapping[wire] = 'e'
        elif counts[wire] == 6:
            mapping[wire] = 'b'
        elif counts[wire] == 9:
            mapping[wire] = 'f'

    remaining = [wire for wire in 'abcdefg' if wire not in mapping]

    # find c, by finding 1
    one = next(d for d in digits if len(d) == 2)
    c = next(ch for ch in one if ch in remaining)
    mapping[c] = 'c'
    remaining.remove(c)

    # find a, only one remaining that appears 8 times
    a = next(ch for ch in remaining if counts[ch] == 8)
    mapping[a] = 'a'
    remaining.remove(a)

    # find d by looking for the four
    four = next(d for d in digits if len(d) == 4) 
    d = next(ch for ch in remaining if ch in four)
    mapping[d] = 'd'
    remaining.remove(d)

    # g is the only one left
    g, = remaining
    mapping[g] = 'g'

    raw_number = raw.split(" | ")[-1].split()
    def remap(digit: str) -> str:
        wires = ''.join(sorted(mapping[ch] for ch in digit))
        return wires_to_int(wires)

    value = int(''.join(remap(digit) for digit in raw_number))

    return value

assert sum(decode(display) for display in DISPLAYS) == 61229


if __name__ == "__main__":
    raw = open('data/day08.txt').read()
    displays = raw.splitlines()
    print(sum(count_1478(display) for display in displays))
    print(sum(decode(display) for display in displays))