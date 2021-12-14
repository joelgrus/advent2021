from typing import Tuple, List, Iterable, NamedTuple

XY = Tuple[int, int]



class Fold(NamedTuple):
    fold_along: str
    fold_at: int

    @staticmethod
    def parse(raw: str) -> 'Fold':
        raw = raw.replace("fold along", "").strip()
        along, at = raw.split("=")
        return Fold(along, int(at))

def get_folds(raw: str) -> List[Fold]:
    raw = raw.split("\n\n")[-1]
    return [Fold.parse(line) for line in raw.splitlines()]


class Transparency:
    def __init__(self, dots: Iterable[XY]) -> None:
        self.dots = set(dots)

    @staticmethod
    def parse(raw: str) -> 'Transparency':
        raw = raw.split("\n\n")[0]
        lines = [line.split(",") for line in raw.splitlines()]
        dots = {(int(x), int(y)) for x, y in lines}
        return Transparency(dots)


    def fold_along_x(self, x_fold: int) -> None:
        """
        After folding vertically, all points with x coordinate less
        than x stay the same, all points with x coordinate greater 
        than x are flipped across x e.g. x+h -> x-h
        """
        keep = {(x, y) for x, y in self.dots if x < x_fold}
        flip = {(x_fold - (x - x_fold), y) 
                for x, y in self.dots 
                if x > x_fold}
        self.dots = keep | flip

    def fold_along_y(self, y_fold: int) -> None:
        """
        After folding horizontally, all points with y coordinate less
        than y stay the same, all points with y coordinate greater 
        than y are flipped across y e.g. y+h -> y-h
        """
        keep = {(x, y) for x, y in self.dots if y < y_fold}
        flip = {(x, y_fold - (y - y_fold)) 
                for x, y in self.dots 
                if y > y_fold}
        self.dots = keep | flip

    def fold(self, fold: Fold) -> None:
        if fold.fold_along == "x":
            self.fold_along_x(fold.fold_at)
        elif fold.fold_along == "y":
            self.fold_along_y(fold.fold_at)
        else:
            raise ValueError(f"Unknown fold along {fold.fold_along}")

    def num_dots(self) -> int:
        return len(self.dots)

    def __str__(self) -> str:
        x_max = max(x for x, y in self.dots)
        y_max = max(y for x, y in self.dots)

        lines = []
        for y in range(y_max + 1):
            line = []
            for x in range(x_max + 1):
                if (x, y) in self.dots:
                    line.append("#")
                else:
                    line.append(" ")
            lines.append("".join(line))
        return "\n".join(lines)


RAW = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

TRANSPARENCY = Transparency.parse(RAW)
FOLDS = get_folds(RAW)
TRANSPARENCY.fold(FOLDS[0])
assert TRANSPARENCY.num_dots() == 17


if __name__ == "__main__":
    raw = open("data/day13.txt").read()
    transparency = Transparency.parse(raw)
    folds = get_folds(raw)
    transparency.fold(folds[0])
    print(transparency.num_dots())

    for fold in folds[1:]:
        transparency.fold(fold)
    print(transparency)
