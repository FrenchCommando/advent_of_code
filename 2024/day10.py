import queue
import re
from utils.printing import display

example = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"""

example2 = """..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""

example3 = """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01"""

example4 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""



with open("day10.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    zeros = []
    n = len(l)
    m = len(l[0])
    for i in range(n):
        for j in range(m):
            if l[i][j] == "0":
                zeros.append((i, j))

    print("zeros", zeros)

    order = "0123456789"
    positions = zeros.copy()
    source_map = {"0": {position: {position} for position in positions}}
    print("positions", len(positions), positions)

    def neighbours(position):
        for positions_near in [
            (-1, 0), (1, 0), (0, -1), (0, 1),
        ]:
            candidate = position[0] + positions_near[0], position[-1] + positions_near[-1]
            if 0<=candidate[0]<n and 0<=candidate[-1]<m:
                yield candidate

    for c_from, c_to in zip(order, order[1:]):
        positions_start = source_map[c_from]
        source_map[c_to] = dict()
        for position, sources in positions_start.items():
            for neighbour in neighbours(position):
                if l[neighbour[0]][neighbour[-1]] == c_to:
                    if neighbour not in source_map[c_to]:
                        source_map[c_to][neighbour] = {pos for pos in sources}
                    else:
                        for pos in sources:
                            source_map[c_to][neighbour].add(pos)

    source_count = {k: sum(len(v) for v in val.values()) for k, val in source_map.items()}
    print("source count", source_count)

    return source_count.get("9", None)


p = count(l=example.split("\n"))
p2 = count(l=example2.split("\n"))
p3 = count(l=example3.split("\n"))
p4 = count(l=example4.split("\n"))
print("count examples", p, p2, p3, p4)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    zeros = []
    n = len(l)
    m = len(l[0])
    for i in range(n):
        for j in range(m):
            if l[i][j] == "0":
                zeros.append((i, j))

    print("zeros", zeros)

    order = "0123456789"
    positions = zeros.copy()
    source_map = {"0": {position: 1 for position in positions}}
    print("positions", len(positions), positions)

    def neighbours(position):
        for positions_near in [
            (-1, 0), (1, 0), (0, -1), (0, 1),
        ]:
            candidate = position[0] + positions_near[0], position[-1] + positions_near[-1]
            if 0<=candidate[0]<n and 0<=candidate[-1]<m:
                yield candidate

    for c_from, c_to in zip(order, order[1:]):
        positions_start = source_map[c_from]
        source_map[c_to] = dict()
        for position, n_sources in positions_start.items():
            for neighbour in neighbours(position):
                if l[neighbour[0]][neighbour[-1]] == c_to:
                    if neighbour not in source_map[c_to]:
                        source_map[c_to][neighbour] = n_sources
                    else:
                        source_map[c_to][neighbour] += n_sources

    source_count = {k: sum(v for v in val.values()) for k, val in source_map.items()}
    print("source count", source_count)

    return source_count.get("9", None)


example22 = """.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9...."""

example23 = """..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""

example24 = """012345
123456
234567
345678
4.6789
56789."""

example25 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

p22 = count2(l=example22.split("\n"))
p23 = count2(l=example23.split("\n"))
p24 = count2(l=example24.split("\n"))
p25 = count2(l=example25.split("\n"))
print("count2", p22, p23, p24, p25)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
