from typing import List, Tuple
from collections import defaultdict
from dataclasses import dataclass

RAW1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

def is_big(cave: str) -> bool:
    return cave.isupper()

class Caves:
    def __init__(self, pairs: List[Tuple[str, str]]) -> None:
        self.caves = defaultdict(list)

        for cave1, cave2 in pairs:
            self.caves[cave1].append(cave2)
            self.caves[cave2].append(cave1)

    @staticmethod
    def parse(raw: str) -> 'Caves':
        pairs = []
        for line in raw.splitlines():
            cave1, cave2 = line.split('-')
            pairs.append((cave1, cave2))
        return Caves(pairs)

    def find_all_paths(self) -> List[List[str]]:
        paths = []

        frontier = [['start']]

        while frontier:
            path = frontier.pop()
            cave = path[-1]

            if cave == 'end':
                paths.append(path)
            else:
                for next_cave in self.caves[cave]:
                    if next_cave not in path or is_big(next_cave):
                        frontier.append(path + [next_cave]) 

        return paths


    def find_all_paths2(self) -> List[List[str]]:
        paths = set()
        lowers = {
            cave 
            for cave in self.caves 
            if cave.islower() and cave not in ('start', 'end')
        }

        frontier = [['start']]

        while frontier:
            path = frontier.pop()

            cave = path[-1]

            if cave == 'end':
                paths.add(tuple(path))
            else:
                for next_cave in self.caves[cave]:
                    duplicate_smalls = [cave for cave in lowers if path.count(cave) > 1]
                    if (is_big(next_cave) or 
                        (not duplicate_smalls and next_cave != "start") or
                        (next_cave not in path)):                    
                        frontier.append(path + [next_cave])
        return list(paths)


CAVES1 = Caves.parse(RAW1)
AP1 = CAVES1.find_all_paths()
assert len(AP1) == 10 
AP12 = CAVES1.find_all_paths2()
assert len(AP12) == 36

RAW2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
CAVES2 = Caves.parse(RAW2)
AP2 = CAVES2.find_all_paths()
assert len(AP2) == 19
AP12 = CAVES2.find_all_paths2()
assert len(AP12) == 103

RAW3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
CAVES3 = Caves.parse(RAW3)
AP3 = CAVES3.find_all_paths()
assert len(AP3) == 226
AP32 = CAVES3.find_all_paths2()
assert len(AP32) == 3509

if __name__ == "__main__":
    raw = open('data/day12.txt').read()
    caves = Caves.parse(raw)
    paths = caves.find_all_paths()
    print(f"Part 1: {len(paths)}")
    paths = caves.find_all_paths2()
    print(f"Part 2: {len(paths)}")