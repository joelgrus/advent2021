from typing import List

RAW = """199
200
208
210
200
207
240
269
260
263"""

INPUT = [int(x) for x in RAW.split('\n')]

def count_increases(depths: List[int], gap: int = 1) -> int:
    count = 0
    for i in range(len(depths) - gap):
        if depths[i] < depths[i + gap]:
            count += 1

    return count

assert count_increases([1, 2, 3]) == 2
assert count_increases(INPUT) == 7

assert count_increases(INPUT, gap=3) == 5

if __name__ == '__main__':
    with open('data/day01.txt') as f:
        raw = f.read()
    input = [int(x) for x in raw.split('\n')]
    print(count_increases(input))
    print(count_increases(input, gap=3))
    