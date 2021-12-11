from typing import Tuple, Iterable
import itertools

RAW = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


XY = Tuple[int, int]

class Grid:
    def __init__(self, grid: Iterable[Iterable[str]]):
        self.grid = [[int(x) for x in row] for row in grid]
        self.nr = len(self.grid)
        self.nc = len(self.grid[0])

    def neighbors(self, x: int, y: int) -> Iterable[XY]:
        """returns the coordinates of all neighbors of (x, y)"""
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if 0 <= i < self.nr and 0 <= j < self.nc and (i, j) != (x, y):
                    yield i, j

    def step(self) -> int:
        """returns the number of flashes"""
        # start by increasing every energy by 1
        for i in range(self.nr):
            for j in range(self.nc):
                self.grid[i][j] += 1

        flashed = set()

        while True:
            need_to_flash = [(i, j) 
                            for i in range(self.nr) 
                            for j in range(self.nc)
                            if self.grid[i][j] > 9
                            and (i, j) not in flashed]

            if not need_to_flash:
                break

            for i, j in need_to_flash:
                flashed.add((i, j))
                # increment all of the neighbors
                for ii, jj in self.neighbors(i, j):
                    self.grid[ii][jj] += 1

        # Set all flashed cells to 0
        for i, j in flashed:
            self.grid[i][j] = 0

        return len(flashed)

    def steps_to_all_flash(self) -> int:
        for step in itertools.count(1):
            if self.step() == self.nr * self.nc:
                return step
        raise RuntimeError("cannot get here")


GRID = Grid(RAW.splitlines())
assert sum(GRID.step() for _ in range(10)) == 204

GRID = Grid(RAW.splitlines())
assert sum(GRID.step() for _ in range(100)) == 1656

GRID = Grid(RAW.splitlines())
assert GRID.steps_to_all_flash() == 195

if __name__ == "__main__":
    raw = open("data/day11.txt").read()
    grid = Grid(raw.splitlines())
    print(sum(grid.step() for _ in range(100)))

    grid = Grid(raw.splitlines())
    print(grid.steps_to_all_flash())