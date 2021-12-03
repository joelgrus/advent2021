from typing import List
from collections import Counter

RAW = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

INPUT = RAW.splitlines()

def gamma_rate(numbers: List[str]) -> str:
    m = len(numbers[0])
    counts = [
        Counter(number[i] for number in numbers)
        for i in range(m)
    ]

    return ''.join(
        counter.most_common(1)[0][0]
        for counter in counts
    )

def epsilon_rate(numbers: List[str]) -> str:
    gr = gamma_rate(numbers)
    return ''.join('1' if c == '0' else '0' for c in gr)

assert gamma_rate(INPUT) == "10110"
assert epsilon_rate(INPUT) == "01001"

def power_consumption(numbers: List[str]) -> int:
    """
    Computes the gamma rate and epsilon rate,
    converts them to base 10, and returns their product.
    """
    return int(gamma_rate(numbers), 2) * int(epsilon_rate(numbers), 2)


assert power_consumption(INPUT) == 198


def oxygen_generator_rating(numbers: List[str]) -> str:
    m = len(numbers[0])

    for i in range(m):
        zeros = 0
        ones = 0
        for number in numbers:
            if number[i] == '0':
                zeros += 1
            elif number[i] == '1':
                ones += 1

        if ones >= zeros:
            numbers = [n for n in numbers if n[i] == '1']
        else:
            numbers = [n for n in numbers if n[i] == '0']

        if len(numbers) == 1:
            return numbers[0]

    raise ValueError("No solution found")

assert oxygen_generator_rating(INPUT) == "10111"


def co2_scrubber_rating(numbers: List[str]) -> str:
    m = len(numbers[0])

    for i in range(m):
        zeros = 0
        ones = 0
        for number in numbers:
            if number[i] == '0':
                zeros += 1
            elif number[i] == '1':
                ones += 1

        if zeros <= ones:
            numbers = [n for n in numbers if n[i] == '0']
        else:
            numbers = [n for n in numbers if n[i] == '1']

        if len(numbers) == 1:
            return numbers[0]

    raise ValueError("No solution found")

assert co2_scrubber_rating(INPUT) == "01010"


def life_support_rating(numbers: List[str]) -> int:
    """
    Computes the oxygen generator rating and co2 scrubber rating,
    converts them to base 10, and returns their product.
    """
    return int(oxygen_generator_rating(numbers), 2) * int(co2_scrubber_rating(numbers), 2)

assert life_support_rating(INPUT) == 230



if __name__ == "__main__":
    numbers = open('data/day03.txt').read().splitlines()
    print(power_consumption(numbers))
    print(life_support_rating(numbers))