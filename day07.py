from typing import List

RAW = "16,1,2,0,4,2,7,1,2,14"
POSITIONS = [int(x) for x in RAW.split(",")]

def total_distance_to(positions: List[int], target: int) -> int:
    return sum(abs(x - target) for x in positions)

def best_position(positions: List[int]) -> int:
    lo = min(positions)
    hi = max(positions)

    return min(range(lo, hi+1), key=lambda x: total_distance_to(positions, x))


BP = best_position(POSITIONS)
assert BP == 2
TD = total_distance_to(POSITIONS, BP)
assert TD == 37

def cost(num_steps: int) -> int:
    """
    the first step costs 1
    the second step costs 2 additional
    the third step costs 3 additional
    and so on

    uses the well-known fact that 
    1 + 2 + ... + n = n(n+1)/2
    """
    return num_steps * (num_steps + 1) // 2

def sum_of_squares(n: int) -> int:
    """
    returns the sum of the first n squares
    using the mathematical fact that
    1^2 + 2^2 + ... + n^2 = n(n+1)(2n+1)/6
    """
    return n * (n + 1) * (2 * n + 1) // 6

assert cost(11) == 66

def cost_to_target(positions: List[int], target: int) -> int:
    return sum(cost(abs(x - target)) for x in positions)

def lowest_cost_position(positions: List[int]) -> int:
    lo = min(positions)
    hi = max(positions)

    return min(range(lo, hi+1), key=lambda x: cost_to_target(positions, x))

LCP = lowest_cost_position(POSITIONS)
assert LCP == 5
TC = cost_to_target(POSITIONS, LCP)
assert TC == 168


if __name__ == "__main__":
    raw = open("data/day07.txt").read()
    positions = [int(x) for x in raw.split(",")]
    bp = best_position(positions)
    td = total_distance_to(positions, bp)
    print(f"Best position: {bp}")
    print(f"Total distance: {td}")

    lcp = lowest_cost_position(positions)
    tc = cost_to_target(positions, lcp)
    print(f"Lowest cost position: {lcp}")
    print(f"Total cost: {tc}")