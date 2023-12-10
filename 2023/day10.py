import queue
from utils.printing import display

example = """.....
.S-7.
.|.|.
.L-J.
....."""

example_more = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

example_complex = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

example_complex_more = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""


with open("day10.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def solve(grid):
    n = len(grid)
    m = len(grid[0])

    def find(c):
        for i, line in enumerate(grid):
            try:
                j = line.index(c)
                return i, j
            except ValueError:
                pass

    s_i, s_j = find(c="S")
    # print("S coordinates", s_i, s_j)

    counts = [[-1 for j in range(m)] for i in range(n)]

    def neighbours_start(i, j):
        if i - 1 >= 0:
            c = grid[i - 1][j]
            if c in ['F', '7', '|']:
                yield i - 1, j
        if i + 1 < n:
            c = grid[i + 1][j]
            if c in ['L', 'J', '|']:
                yield i + 1, j
        if j - 1 >= 0:
            c = grid[i][j - 1]
            if c in ['L', 'F', '|']:
                yield i, j - 1
        if j + 1 < m:
            c = grid[i][j + 1]
            if c in ['J', '7', '-']:
                yield i, j + 1

    def neighbours(i, j):
        c = grid[i][j]
        if c == '|':
            yield i - 1, j
            yield i + 1, j
        if c == '-':
            yield i, j - 1
            yield i, j + 1
        if c == 'L':
            yield i - 1, j
            yield i, j + 1
        if c == 'J':
            yield i - 1, j
            yield i, j - 1
        if c == '7':
            yield i + 1, j
            yield i, j - 1
        if c == 'F':
            yield i + 1, j
            yield i, j + 1

    q = queue.Queue()
    m_count = 0

    counts[s_i][s_j] = 0
    for l_i, l_j in neighbours_start(i=s_i, j=s_j):
        q.put((l_i, l_j))
        counts[l_i][l_j] = 1

    while not q.empty():
        l_i, l_j = q.get()
        count = counts[l_i][l_j]
        # print(count, l_i, l_j, q)
        m_count = max(m_count, count)
        for n_i, n_j in neighbours(i=l_i, j=l_j):
            if counts[n_i][n_j] == -1:
                counts[n_i][n_j] = count + 1
                q.put((n_i, n_j))

    return m_count


display(x=solve(grid=example.split("\n")))
display(x=solve(grid=example_more.split("\n")))
display(x=solve(grid=example_complex.split("\n")))
display(x=solve(grid=example_complex_more.split("\n")))
display(x=solve(grid=s))


example_tile = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""


example_tile_2 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""


example_tile_3 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


def solve2(grid):
    n = len(grid)
    m = len(grid[0])

    def find(c):
        for i, line in enumerate(grid):
            try:
                j = line.index(c)
                return i, j
            except ValueError:
                pass

    s_i, s_j = find(c="S")
    # print("S coordinates", s_i, s_j)

    tags = [["." for j in range(m)] for i in range(n)]

    def neighbours_start(i, j):
        if i - 1 >= 0:
            c = grid[i - 1][j]
            if c in ['F', '7', '|']:
                yield i - 1, j, "S"
        if i + 1 < n:
            c = grid[i + 1][j]
            if c in ['L', 'J', '|']:
                yield i + 1, j, "N"
        if j - 1 >= 0:
            c = grid[i][j - 1]
            if c in ['L', 'F', '|']:
                yield i, j - 1, "E"
        if j + 1 < m:
            c = grid[i][j + 1]
            if c in ['J', '7', '-']:
                yield i, j + 1, "W"

    def next_step(i, j, origin):
        c = grid[i][j]
        if c == '|':
            if origin == "S":
                return i - 1, j, "S", [(i, j - 1)], [(i, j + 1)]
            if origin == "N":
                return i + 1, j, "N", [(i, j + 1)], [(i, j - 1)]
        if c == '-':
            if origin == "E":
                return i, j - 1, "E", [(i + 1, j)], [(i - 1, j)]
            if origin == "W":
                return i, j + 1, "W", [(i - 1, j)], [(i + 1, j)]
        if c == 'L':
            if origin == "E":
                return i - 1, j, "S", [(i, j - 1), (i + 1, j)], []
            if origin == "N":
                return i, j + 1, "W", [], [(i + 1, j), (i, j - 1)]
        if c == 'J':
            if origin == "W":
                return i - 1, j, "S", [], [(i, j + 1), (i + 1, j)]
            if origin == "N":
                return i, j - 1, "E", [(i, j + 1), (i + 1, j)], []
        if c == '7':
            if origin == "W":
                return i + 1, j, "N", [(i, j + 1), (i - 1, j)], []
            if origin == "S":
                return i, j - 1, "E", [], [(i, j + 1), (i - 1, j)]
        if c == 'F':
            if origin == "E":
                return i + 1, j, "N", [], [(i, j - 1), (i - 1, j)]
            if origin == "S":
                return i, j + 1, "W", [(i, j - 1), (i - 1, j)], []

    q = queue.Queue()

    tags[s_i][s_j] = "F"
    for l_i, l_j, l_origin in neighbours_start(i=s_i, j=s_j):
        q.put((l_i, l_j, l_origin))
        tags[l_i][l_j] = "F"
        break  # orient in one direction - it's a loop anyway

    while not q.empty():
        l_i, l_j, l_origin = q.get()
        n_i, n_j, n_origin, l_color_left, l_color_right = next_step(i=l_i, j=l_j, origin=l_origin)
        for i, j in l_color_left:
            if 0 <= i < n and 0 <= j < m:
                if tags[i][j] not in ['F']:
                    tags[i][j] = "L"
        for i, j in l_color_right:
            if 0 <= i < n and 0 <= j < m:
                if tags[i][j] not in ['F']:
                    tags[i][j] = "R"
        if tags[n_i][n_j] != "F":
            tags[n_i][n_j] = "F"
            q.put((n_i, n_j, n_origin))

    # print("\n".join(''.join(line) for line in tags))

    # don't need to color the outside
    outside_direction = ''.join(''.join(line) for line in tags).replace(".", "")[0]  # left or right
    # print("Outside direction", outside_direction)

    def neighbours(i, j):
        if 0 <= i-1 < n and 0 <= j < m:
            yield i-1, j
        if 0 <= i+1 < n and 0 <= j < m:
            yield i+1, j
        if 0 <= i < n and 0 <= j-1 < m:
            yield i, j-1
        if 0 <= i < n and 0 <= j+1 < m:
            yield i, j+1

    inside_direction = "L" if outside_direction == "R" else "R"
    # finish coloring inside
    lower_inside_direction = inside_direction.lower()  # for plotting
    q_inside = queue.Queue()
    for i in range(n):
        for j in range(m):
            if tags[i][j] == inside_direction:
                q_inside.put((i, j))
    while not q_inside.empty():
        i, j = q_inside.get()
        for n_i, n_j in neighbours(i=i, j=j):
            if tags[n_i][n_j] == ".":
                tags[n_i][n_j] = lower_inside_direction
                q_inside.put((n_i, n_j))

    # print("\n".join(''.join(line) for line in tags))

    l_count = sum(line.count("L") + line.count("l") for line in tags)
    r_count = sum(line.count("R") + line.count("r") for line in tags)
    return dict(
        answer=l_count if inside_direction == "L" else r_count,
        inside=inside_direction,
        l=l_count, r=r_count,
    )


display(x=solve2(grid=example_tile.split("\n")))
display(x=solve2(grid=example_tile_2.split("\n")))
display(x=solve2(grid=example_tile_3.split("\n")))
display(x=solve2(grid=s))
