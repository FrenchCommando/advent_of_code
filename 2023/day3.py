import re
from utils.printing import display

example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


with open("day3.txt", "r") as f:
    s = f.readlines()
    display(s)
    display(x=set(''.join(s)))

symbols = "*#+$/@%=-&"


def label(grid):
    n = len(grid)
    n1 = len(grid[0])

    labels = [[False for j in range(n1)] for i in range(n)]

    symbol_index = []
    for i, v in enumerate(grid):
        for j, vv in enumerate(v):
            if vv in symbols:
                symbol_index.append((i, j))
    for i, j in symbol_index:
        labels[max(i-1, 0)][max(j-1, 0)] = True
        labels[max(i-1, 0)][j] = True
        labels[max(i-1, 0)][min(j+1, n1)] = True
        labels[i][max(j-1, 0)] = True
        labels[i][j] = True
        labels[i][min(j+1, n1)] = True
        labels[min(i+1, n)][max(j-1, 0)] = True
        labels[min(i+1, n)][j] = True
        labels[min(i+1, n)][min(j+1, n1)] = True

    chosen = []
    for i, line in enumerate(grid):
        j_shift = 0
        while line[j_shift:]:
            symbol_part = re.split(pattern=r"\d+", string=line[j_shift:], maxsplit=1)[0]
            j_shift += len(symbol_part)
            parsed = re.split(pattern=r"\D+", string=line[j_shift:], maxsplit=1)[0]
            next_j = j_shift + len(parsed)
            if any(labels[i][j] for j in range(j_shift, next_j)):
                chosen.append(int(parsed))
            j_shift = next_j
    return chosen


# out = label(grid=s)
out = label(grid=example.split("\n"))

display(x=out)
display(x=sum(out))


def gear(grid):
    n = len(grid)
    n1 = len(grid[0])

    labels = [[[] for j in range(n1)] for i in range(n)]

    gear_index = []
    for i, v in enumerate(grid):
        for j, vv in enumerate(v):
            if vv == "*":
                gear_index.append((i, j))
    for g, (i, j) in enumerate(gear_index):
        labels[max(i-1, 0)][max(j-1, 0)].append(g)
        labels[max(i-1, 0)][j].append(g)
        labels[max(i-1, 0)][min(j+1, n1)].append(g)
        labels[i][max(j-1, 0)].append(g)
        labels[i][j].append(g)
        labels[i][min(j+1, n1)].append(g)
        labels[min(i+1, n)][max(j-1, 0)].append(g)
        labels[min(i+1, n)][j].append(g)
        labels[min(i+1, n)][min(j+1, n1)].append(g)

    gear_count = [[] for g in range(len(gear_index))]
    for i, line in enumerate(grid):
        j_shift = 0
        while line[j_shift:]:
            symbol_part = re.split(pattern=r"\d+", string=line[j_shift:], maxsplit=1)[0]
            j_shift += len(symbol_part)
            parsed = re.split(pattern=r"\D+", string=line[j_shift:], maxsplit=1)[0]
            next_j = j_shift + len(parsed)

            gear_match = set(g for j in range(j_shift, next_j) for g in labels[i][j])
            for g in gear_match:
                gear_count[g].append(int(parsed))
            j_shift = next_j
    return gear_count


# out = gear(grid=s)
out = gear(grid=example.split("\n"))

display(x=out)
display(x=[gl[0] * gl[1] for gl in out if len(gl) == 2])
display(x=sum(gl[0] * gl[1] for gl in out if len(gl) == 2))
