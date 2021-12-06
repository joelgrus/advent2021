from typing import List

RAW = "3,4,3,1,2"
INPUT = [int(x) for x in RAW.split(",")]

class LanternFish:
    def __init__(self, timers: List[int]) -> None:
        self.timers = [0 for i in range(9)]
        for timer in timers:
            self.timers[timer] += 1

    def step(self) -> None:
        new_timers = self.timers[1:] + [0]
        new_timers[8] += self.timers[0]
        new_timers[6] += self.timers[0]
        self.timers = new_timers

    def count(self) -> int:
        return sum(self.timers)


LF = LanternFish(INPUT)
for n in range(18):
    LF.step()
assert LF.count() == 26
for n in range(80 - 18):
    LF.step()
assert LF.count() == 5934
for n in range(256 - 80):
    LF.step()
assert LF.count() == 26984457539

if __name__ == "__main__":
    raw = open("data/day06.txt").read()
    input = [int(x) for x in raw.split(",")]
    lf = LanternFish(input)
    for _ in range(80):
        lf.step()
    print(lf.count())
    for _ in range(256 - 80):
        lf.step()
    print(lf.count())