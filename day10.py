from typing import Optional, List

RAW = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

OC = {"[": "]", "(": ")", "<": ">", "{": "}"}

def first_illegal_character(s: str) -> Optional[str]:
    stack = []
    for c in s:
        if c in OC:
            stack.append(c)
        else:
            if not stack or OC[stack.pop()] != c:
                return c
    return None

SCORE = {
    "]": 57,
    "}": 1197,
    ">": 25137,
    ")": 3
}

def score(line: str) -> int:
    if fic := first_illegal_character(line):
        return SCORE[fic]
    else:
        return 0


LINES = RAW.splitlines()
assert sum(score(line) for line in LINES) == 26397

COMPLETION_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

def completion(s: str) -> List[str]:
    assert first_illegal_character(s) is None

    stack = []
    for c in s:
        if c in OC:
            stack.append(c)
        else:
            assert c == OC[stack.pop()]

    return [OC[c] for c in reversed(stack)]

def score_completion(completion: List[str]) -> int:
    score = 0
    for c in completion:
        score *= 5
        score += COMPLETION_SCORES[c]
    return score

def median_completion_score(lines: List[str]) -> int:
    completion_scores = [
        score_completion(completion(line))
        for line in lines
        if first_illegal_character(line) is None
    ]

    # assert that there is an odd number of scores
    assert len(completion_scores) % 2 == 1

    return sorted(completion_scores)[len(completion_scores) // 2]

assert median_completion_score(LINES) == 288957


if __name__ == "__main__":
    raw = open("data/day10.txt").read()
    lines = raw.splitlines()
    print(sum(score(line) for line in lines))
    print(median_completion_score(lines))

    