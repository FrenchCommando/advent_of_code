import re
from utils.printing import display

example = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""



with open("day8.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    d = dict()
    for i, line in enumerate(l):
        for j, c in enumerate(line):
            if c != ".":
                if c in d:
                    d[c].append((i, j))
                else:
                    d[c] = [(i, j)]
    print(d)
    n = len(l)
    m = len(l[0])
    grid = [[False for j in range(m)] for i in range(n)]

    for c, lines in d.items():
        for x,y in lines:
            for a,b in lines:
                if (x,y) == (a,b):
                    continue
                d1 = a - x
                d2 = b - y
                t1 = a + d1
                t2 = b + d2
                if 0<= t1 < n and 0 <= t2 < m:
                    grid[t1][t2] = True
    for line in grid:
        print("".join("#" if u else "." for u in line))
    return sum(sum(line) for line in grid)


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    d = dict()
    for i, line in enumerate(l):
        for j, c in enumerate(line):
            if c != ".":
                if c in d:
                    d[c].append((i, j))
                else:
                    d[c] = [(i, j)]
    print(d)
    n = len(l)
    m = len(l[0])
    grid = [[False for j in range(m)] for i in range(n)]

    for c, lines in d.items():
        for x,y in lines:
            for a,b in lines:
                if (x,y) == (a,b):
                    continue
                d1 = a - x
                d2 = b - y

                t1 = a
                t2 = b
                while 0<= t1 < n and 0 <= t2 < m:
                    grid[t1][t2] = True
                    t1 += d1
                    t2 += d2
    for line in grid:
        print("".join("#" if u else "." for u in line))
    return sum(sum(line) for line in grid)


p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
