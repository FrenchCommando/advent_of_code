import queue
from utils.printing import display

# replaces "\" by "l" to avoid python escaping chars

example = """.|...l....
|.-.l.....
.....|-...
........|.
..........
.........l
..../.ll..
.-.-/..|..
.|....-|.l
..//.|...."""


with open("day16.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def solve(grid, x_init, y_init, d_init):
    n = len(grid)
    status = [["." for j in range(n)] for i in range(n)]
    seen = set()

    def go_down(x, y):
        i = 1
        while x + i < n and grid[x + i][y] in [".", "|"]:
            status[x + i][y] = "v"
            i += 1
        if x + i != n:
            add_if_not_seen(element=(x + i, y, "v"))

    def go_up(x, y):
        i = 1
        while x - i >= 0 and grid[x - i][y] in [".", "|"]:
            status[x - i][y] = "^"
            i += 1
        if x - i != -1:
            add_if_not_seen(element=(x - i, y, "^"))

    def go_right(x, y):
        i = 1
        while y + i < n and grid[x][y + i] in [".", "-"]:
            status[x][y + i] = ">"
            i += 1
        if y + i != n:
            add_if_not_seen(element=(x, y + i, ">"))

    def go_left(x, y):
        i = 1
        while y - i >= 0 and grid[x][y - i] in [".", "-"]:
            status[x][y - i] = "<"
            i += 1
        if y - i != -1:
            add_if_not_seen(element=(x, y - i, "<"))

    def process(x, y, d):
        g = grid[x][y]
        if g == "|":
            if d in ["<"]:
                status[x][y] = "<"
                go_up(x=x, y=y)
                go_down(x=x, y=y)
            if d in [">"]:
                status[x][y] = ">"
                go_up(x=x, y=y)
                go_down(x=x, y=y)
        if g == "-":
            if d in ["^"]:
                status[x][y] = "^"
                go_left(x=x, y=y)
                go_right(x=x, y=y)
            if d in ["v"]:
                status[x][y] = "v"
                go_left(x=x, y=y)
                go_right(x=x, y=y)
        if g == "/":
            if d in ["^"]:
                status[x][y] = "^"
                go_right(x=x, y=y)
            if d in ["v"]:
                status[x][y] = "v"
                go_left(x=x, y=y)
            if d in ["<"]:
                status[x][y] = "<"
                go_down(x=x, y=y)
            if d in [">"]:
                status[x][y] = ">"
                go_up(x=x, y=y)
        if g == "l":
            if d in ["^"]:
                status[x][y] = "^"
                go_left(x=x, y=y)
            if d in ["v"]:
                status[x][y] = "v"
                go_right(x=x, y=y)
            if d in ["<"]:
                status[x][y] = "<"
                go_up(x=x, y=y)
            if d in [">"]:
                status[x][y] = ">"
                go_down(x=x, y=y)

    def add_if_not_seen(element):
        if element not in seen:
            seen.add(element)
            q.put(element)

    q = queue.Queue()
    if d_init == ">":
        go_right(x=x_init, y=y_init)
    if d_init == "<":
        go_left(x=x_init, y=y_init)
    if d_init == "^":
        go_up(x=x_init, y=y_init)
    if d_init == "v":
        go_down(x=x_init, y=y_init)
    while not q.empty():
        x0, y0, d0 = q.get()
        process(x=x0, y=y0, d=d0)

    return status


def solve_and_count(grid, x_init, y_init, d_init):
    solved = solve(grid=grid, x_init=x_init, y_init=y_init, d_init=d_init)
    l_light = [[c != '.' for c in line] for line in solved]
    return sum(sum(line) for line in l_light)


def solve_all(grid):
    res = []
    n = len(grid)
    for x in range(n):
        out = solve_and_count(grid=grid, x_init=x, y_init=-1, d_init=">")
        res.append(out)
        out = solve_and_count(grid=grid, x_init=x, y_init=n, d_init="<")
        res.append(out)
    for y in range(n):
        out = solve_and_count(grid=grid, x_init=-1, y_init=y, d_init="v")
        res.append(out)
        out = solve_and_count(grid=grid, x_init=n, y_init=y, d_init="^")
        res.append(out)
    return res


l_parsed = solve(grid=example.split("\n"), x_init=0, y_init=-1, d_init=">")
# l_parsed = solve(grid=s, x_init=0, y_init=-1, d_init=">")

display(x=l_parsed)
light = [[c != '.' for c in line] for line in l_parsed]
# display(x=light)
display(x=sum(sum(line) for line in light))


l_solved = solve_all(grid=example.split("\n"))
# l_solved = solve_all(grid=s)
display(x=max(l_solved))
