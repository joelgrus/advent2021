from typing import Dict
from collections import Counter

RAW = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def template(raw: str) -> str:
    return raw.splitlines()[0]

Rules = Dict[str, str]

def rules(raw: str) -> Rules:
    lines = raw.splitlines()[2:]
    pairs = [line.split(' -> ') for line in lines]
    return {pair: insertion for pair, insertion in pairs}

def perform_insertion(template: str, rules: Rules) -> str:
    pairs = [template[i:i+2] for i in range(len(template)-1)]
    insertions = [rules[pair] for pair in pairs]

    result = []
    for c, insertion in zip(template, insertions):
        result.append(c)
        result.append(insertion)
    result.append(template[-1])
    return ''.join(result)

def solve(raw: str, num_steps: int = 10) -> int:
    rules_ = rules(raw)
    template_ = template(raw)
    for _ in range(num_steps):
        template_ = perform_insertion(template_, rules_)

    counts = Counter(template_).most_common()
    return counts[0][1] - counts[-1][1]

TEMPLATE = template(RAW)
RULES = rules(RAW)
assert perform_insertion(TEMPLATE, RULES) == 'NCNBCHB'
assert perform_insertion('NCNBCHB', RULES) == 'NBCCNBBBCBHCB'
assert solve(RAW) == 1588


# part 2

"""
NNCB

(None N) (N N) (N C) (C B) (B None)

(None N) -> (None N)
(N N) -> (N C) (C N)
(N C) -> (N B) (B C)
(C B) -> (C H) (H B)
(B None) -> (B None)

(None N) (N C) (C N) (N B) (B C) (C H) (H B) (B None)
N C N B C H B
NCNBCHB
"""

class Solution:
    def __init__(self, template: str, rules: Rules) -> None:
        self.template = template
        self.rules = {tuple(pair): insertion for pair, insertion in rules.items()}
        # This actually double counts
        self.pair_counts = Counter()
        self.pair_counts[(None, template[0])] = 1
        self.pair_counts[(template[-1], None)] = 1
        for prev, next in zip(template, template[1:]):
            self.pair_counts[(prev, next)] += 1

    def step(self) -> None:
        new_counts = Counter()
        for key in self.pair_counts:
            if None in key:
                new_counts[key] += 1
            else:
                p, n = key
                insert = self.rules[(p, n)]
                new_counts[(p, insert)] += self.pair_counts[key]
                new_counts[(insert, n)] += self.pair_counts[key]
        self.pair_counts = new_counts

    def run(self, num_steps: int) -> int:
        for _ in range(num_steps):
            self.step()

        counts = Counter()
        for (prev, nxt), count in self.pair_counts.items():
            if prev is not None:
                counts[prev] += count
            if nxt is not None:
                counts[nxt] += count
        
        mc = list(counts.most_common())
        double_counted = mc[0][1] - mc[-1][1]
        # because each character appears once as the first in a pair
        # and once as the second in a pair we have to divide by 2
        return double_counted // 2


SOLUTION = Solution(TEMPLATE, RULES)
assert SOLUTION.run(10) == 1588
SOLUTION = Solution(TEMPLATE, RULES)
assert SOLUTION.run(40) == 2188189693529

if __name__ == '__main__':
    raw = open('data/day14.txt').read()
    print(solve(raw))
    temp = template(raw)
    rulz = rules(raw)
    solution = Solution(temp, rulz)
    print(solution.run(40))
