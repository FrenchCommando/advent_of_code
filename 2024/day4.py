import re
from utils.printing import display

example = """..X...
.SAMX.
.A..A.
XMAS.S
.X...."""


example2 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


with open("day4.txt", "r") as f:
    s = f.readlines()
    display(s)


xmas = "XMAS"


def count(l):
    n = len(l)
    m = len(l[0])
    def count_dir(i_internal, j_internal, di, dj, remaining):
        if len(remaining) == 0:
            # print(i, j, i_internal, j_internal, di, dj, )
            return 1
        if 0 <= i_internal < n:
            if 0 <= j_internal < m:
                # print(i_internal, n, j_internal, m, remaining)
                # print(l[i_internal][j_internal])
                if l[i_internal][j_internal] == remaining[0]:
                    return count_dir(i_internal+di, j_internal+dj, di, dj, remaining[1:])
        return 0

    def count_internal(i_internal, j_internal):
        return sum((count_dir(i_internal, j_internal, di, dj, xmas) for di, dj in [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]))


    c = 0
    for i in range(n):
        for j in range(m):
            c += count_internal(i, j)
    return c


p = count(l=example.split("\n"))
print("count", p)
p2 = count(l=example2.split("\n"))
print("count", p2)
ps = count(l=[line.strip() for line in s])
print("count", ps)


example3 = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
.........."""


def count2(l):
    n = len(l)
    m = len(l[0])
    def count_dir(i_internal, j_internal, di, dj, remaining):
        if len(remaining) == 0:
            # print(i, j, i_internal, j_internal, di, dj, )
            return 1
        if 0 <= i_internal < n:
            if 0 <= j_internal < m:
                # print(i_internal, n, j_internal, m, remaining)
                # print(l[i_internal][j_internal])
                if l[i_internal][j_internal] == remaining[0]:
                    return count_dir(i_internal+di, j_internal+dj, di, dj, remaining[1:])
        return 0

    def count_internal(i_internal, j_internal):
        for ms in [
            ((-1, -1), (-1, 1)),
            ((-1, 1), (1, 1)),
            ((1, -1), (1, 1)),
            ((-1, -1), (1, -1)),
        ]:
            m1, m2 = ms
            x1 = (-m1[0], -m1[-1])
            x2 = (-m2[0], -m2[-1])
            if 0 <= i_internal + m1[0] < n:
                if 0 <= i_internal + m2[0] < n:
                    if 0 <= i_internal + x1[0] < n:
                        if 0 <= i_internal + x2[0] < n:
                            if 0 <= j_internal + m1[1] < m:
                                if 0 <= j_internal + m2[1] < m:
                                    if 0 <= j_internal + x1[1] < m:
                                        if 0 <= j_internal + x2[1] < m:
                                            if l[i_internal + m1[0]][j_internal + m1[1]] == "M":
                                                if l[i_internal + m2[0]][j_internal + m2[1]] == "M":
                                                    if l[i_internal + x1[0]][j_internal + x1[1]] == "S":
                                                        if l[i_internal + x2[0]][j_internal + x2[1]] == "S":
                                                            return 1
        return 0

    c = 0
    for i in range(n):
        for j in range(m):
            if l[i][j] == "A":
                c += count_internal(i, j)
    return c


p3 = count2(l=example3.split("\n"))
print("count", p3)
ps2 = count2(l=[line.strip() for line in s])
print("count", ps2)
