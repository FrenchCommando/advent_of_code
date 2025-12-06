import itertools

from utils.printing import display


examples = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""


with open("day18.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p, n):
    m = len(p)
    count = sum(l.count("#") for l in p)
    print(count)

    for k in range(n):
        # print(p)
        neighs = [
            [
                sum(map(lambda x: 1 if x == "#" else 0, (a, b, c)))
                for a, b, c in zip(i, "." + i[:-1], i[1:] + ".")
            ]
            for i in p
        ]
        c = [[0 for _ in range(m)]for i in range(m)]
        for i in range(m):
            for j in range(m):
                c[i][j] += neighs[i][j]
                if i > 0:
                    c[i][j] += neighs[i - 1][j]
                if i < m - 1:
                    c[i][j] += neighs[i + 1][j]
        q = [[
            "#" if p[i][j] == "#" and c[i][j] - 1 in [2, 3] or p[i][j] == "." and c[i][j] == 3 else "."
            for j in range(m)]for i in range(m)]
        p = [''.join(i) for i in q]

        # print("\n".join(p))
        count = sum(l.count("#") for l in p)
        print(k, count)
    print()


get_count(p=[sss.strip() for sss in s], n=100)
get_count(p=[sss.strip() for sss in examples.split("\n")], n=4)
print()


def get_count2(p, n):
    m = len(p)
    count = sum(l.count("#") for l in p)
    print(count)

    q = [["#" if p[i][j] == "#"  else "." for j in range(m)] for i in range(m)]
    q[0][0] = "#"
    q[0][m - 1] = "#"
    q[m - 1][0] = "#"
    q[m - 1][m - 1] = "#"
    p = [''.join(i) for i in q]
    # print("\n".join(p))
    # print()

    for k in range(n):
        # print(p)
        neighs = [
            [
                sum(map(lambda x: 1 if x == "#" else 0, (a, b, c)))
                for a, b, c in zip(i, "." + i[:-1], i[1:] + ".")
            ]
            for i in p
        ]
        c = [[0 for _ in range(m)]for i in range(m)]
        for i in range(m):
            for j in range(m):
                c[i][j] += neighs[i][j]
                if i > 0:
                    c[i][j] += neighs[i - 1][j]
                if i < m - 1:
                    c[i][j] += neighs[i + 1][j]
        q = [[
            "#" if p[i][j] == "#" and c[i][j] - 1 in [2, 3] or p[i][j] == "." and c[i][j] == 3 else "."
            for j in range(m)]for i in range(m)]
        q[0][0] = "#"
        q[0][m-1] = "#"
        q[m-1][0] = "#"
        q[m-1][m-1] = "#"
        p = [''.join(i) for i in q]

        # print("\n".join(p))
        count = sum(l.count("#") for l in p)
        print(k, count)
    print()


get_count2(p=[sss.strip() for sss in s], n=100)
get_count2(p=[sss.strip() for sss in examples.split("\n")], n=5)
print()
