from utils.printing import display

# replaces "\" by "l" to avoid python escaping chars

example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


with open("day13.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def parse_grid(text):
    out_grids = []
    g = None
    for line in text:
        if g is None:
            g = [line]
        else:
            if line == "":
                out_grids.append(g)
                g = None
            else:
                g.append(line)
    if g is not None:
        out_grids.append(g)
    return out_grids


def solve(grid):
    n = len(grid)
    m = len(grid[0])

    def check_h(x):
        i = 0
        while x - i - 1 >= 0 and x + i < n:
            for y in range(m):
                if grid[x - i - 1][y] != grid[x + i][y]:
                    return False
            i += 1
        return True

    def check_v(y):
        i = 0
        while y - i - 1 >= 0 and y + i < m:
            for x in range(n):
                if grid[x][y - i - 1] != grid[x][y + i]:
                    return False
            i += 1
        return True

    answer = []
    for l_x in range(1, n):
        if check_h(x=l_x):
            answer.append(("H", l_x))
    for l_y in range(1, m):
        if check_v(y=l_y):
            answer.append(("V", l_y))

    if not answer:
        for g in grid:
            print(g)
        print()

    return answer


def solve2(grid):
    n = len(grid)
    m = len(grid[0])

    def check_h(x):
        smudged = False
        i = 0
        while x - i - 1 >= 0 and x + i < n:
            for y in range(m):
                if grid[x - i - 1][y] != grid[x + i][y]:
                    if not smudged:
                        smudged = True
                    else:
                        return False
            i += 1
        return smudged

    def check_v(y):
        smudged = False
        i = 0
        while y - i - 1 >= 0 and y + i < m:
            for x in range(n):
                if grid[x][y - i - 1] != grid[x][y + i]:
                    if not smudged:
                        smudged = True
                    else:
                        return False
            i += 1
        return smudged

    answer = []
    for l_x in range(1, n):
        if check_h(x=l_x):
            answer.append(("H", l_x))
    for l_y in range(1, m):
        if check_v(y=l_y):
            answer.append(("V", l_y))

    if not answer:
        for g in grid:
            print(g)
        print()

    return answer


def number(solved):
    count_v = sum(v for d, v in solved if d == "V")
    count_h = sum(v for d, v in solved if d == "H")
    return count_v + 100 * count_h


grids = parse_grid(text=example.split("\n"))
# grids = parse_grid(text=s)
l_solved = [g for grid in grids for g in solve(grid=grid)]
l_solved2 = [g for grid in grids for g in solve2(grid=grid)]
display(x=l_solved)
display(x=l_solved2)
display(x=number(solved=l_solved))
display(x=number(solved=l_solved2))
# low 28139
