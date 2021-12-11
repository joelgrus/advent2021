from typing import Iterable, Iterator, Tuple, List
from copy import deepcopy

RAW = """2199943210
3987894921
9856789892
8767896789
9899965678"""


class HeightMap:
    def __init__(self, raw: str):
        self.map = [[int(val) for val in row] for row in raw.splitlines()]
        self.nr = len(self.map)
        self.nc = len(self.map[0])

    def neighbors(self, r: int, c: int) -> Iterator[Tuple[int, int]]:
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if 0 <= r + dr < self.nr and 0 <= c + dc < self.nc:
                yield r + dr, c + dc

    def is_low_point(self, r: int, c: int) -> bool:
        ilp = all(
            self.map[r][c] < self.map[r_][c_]
            for r_, c_ in self.neighbors(r, c)
        )
        return ilp

    def risk_level(self, r: int, c: int) -> int:
        """
        The risk level of a point is one plus its height
        """
        return self.map[r][c] + 1

    def total_risk_level_of_low_points(self) -> int:
        return sum(
            self.risk_level(r, c)
            for r in range(self.nr)
            for c in range(self.nc)
            if self.is_low_point(r, c)
        )

    def find_basin_size(self, r: int, c: int) -> int:
        m = deepcopy(self.map)
        stack = [(r, c)]
        visited = {(r, c)}
        basin_size = 0
        while stack:
            r, c = stack.pop()
            basin_size += 1
            m[r][c] = 9

            for r_, c_ in self.neighbors(r, c):
                if m[r_][c_] != 9 and (r_, c_) not in visited:
                    stack.append((r_, c_))
                    visited.add((r_, c_))

        return basin_size

    def all_low_points(self) -> List[Tuple[int, int]]:
        """returns all low points"""
        return [(r, c) for r in range(self.nr) for c in range(self.nc) if self.is_low_point(r, c)]

    def all_basin_sizes(self) -> List[int]:
        """returns all basin sizes"""
        return [self.find_basin_size(r, c) for r, c in self.all_low_points()]

    def three_largest_basins_product(self) -> int:
        """returns the product of the three largest basins"""
        all_basin_sizes = sorted(self.all_basin_sizes(), reverse=True)
        return all_basin_sizes[0] * all_basin_sizes[1] * all_basin_sizes[2]

HM = HeightMap(RAW)
assert HM.total_risk_level_of_low_points() == 15
assert sorted(HM.all_basin_sizes()) == [3, 9, 9, 14]
assert HM.three_largest_basins_product() == 9 * 9 * 14

if __name__ == "__main__":
    raw = open("data/day09.txt").read()
    hm = HeightMap(raw)
    print(hm.total_risk_level_of_low_points())
    print(hm.three_largest_basins_product())