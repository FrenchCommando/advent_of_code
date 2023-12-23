from utils.printing import display

example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


with open("day21.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def walk(grid, n_steps):
    n = len(grid)
    m = len(grid[0])

    def find_s():
        for i, line in enumerate(grid):
            for j, c in enumerate(line):
                if c == "S":
                    return i, j
    i_s, j_s = find_s()
    q = set()
    q.add((i_s, j_s))
    for i_step in range(n_steps):
        p = set()
        for x, y in q:
            if x - 1 >= 0:
                if grid[x - 1][y] != "#":
                    p.add((x - 1, y))
            if y - 1 >= 0:
                if grid[x][y - 1] != "#":
                    p.add((x, y - 1))
            if x + 1 < n:
                if grid[x + 1][y] != "#":
                    p.add((x + 1, y))
            if y + 1 < m:
                if grid[x][y + 1] != "#":
                    p.add((x, y + 1))
        q = p

    grid_out = [["." for j in range(m)] for i in range(n)]
    for x, y in q:
        grid_out[x][y] = "O"
    return grid_out


grid_value = example.split("\n")
out_grid = walk(grid=grid_value, n_steps=6)
display(x=''.join(''.join(line) for line in out_grid).count("O"))

grid_value = s
out_grid = walk(grid=grid_value, n_steps=64)
display(x=''.join(''.join(line) for line in out_grid).count("O"))
print()


def walk2(grid, n_steps):

    n = len(grid)
    m = len(grid[0])

    def find_s():
        for i, line in enumerate(grid):
            for j, c in enumerate(line):
                if c == "S":
                    return i, j
    i_s, j_s = find_s()
    q0 = set()
    q0.add((i_s, j_s))
    q1 = set()
    q0_last = set()
    q0_last.add((i_s, j_s))
    q1_last = set()

    for i_step in range(n_steps):
        if i_step % 2 == 0:
            q1_last.clear()
            for x, y in q0_last:
                def process1(xx, yy):
                    if grid[xx % n][yy % m] != "#":
                        if (xx, yy) not in q1:
                            q1_last.add((xx, yy))
                            q1.add((xx, yy))
                process1(xx=x - 1, yy=y)
                process1(xx=x + 1, yy=y)
                process1(xx=x, yy=y - 1)
                process1(xx=x, yy=y + 1)
        else:
            q0_last.clear()
            for x, y in q1_last:
                def process0(xx, yy):
                    if grid[xx % n][yy % m] != "#":
                        if (xx, yy) not in q0:
                            q0_last.add((xx, yy))
                            q0.add((xx, yy))
                process0(xx=x - 1, yy=y)
                process0(xx=x + 1, yy=y)
                process0(xx=x, yy=y - 1)
                process0(xx=x, yy=y + 1)
    return len(q0) if n_steps % 2 == 0 else len(q1)


def walk2bis(grid, n_steps):

    n = len(grid)
    m = len(grid[0])

    def find_s():
        for i, line in enumerate(grid):
            for j, c in enumerate(line):
                if c == "S":
                    return i, j
    i_s, j_s = find_s()

    def solve(i, j):
        # i, j is the starting point
        # gets the function step -> n_spots

        results = [1]

        q0 = set()
        q0.add((i, j))
        q1 = set()
        q0_last = set()
        q0_last.add((i, j))
        q1_last = set()
        i_step = 0
        while len(q0_last) != 0 or len(q1_last) != 0:
            if i_step % 2 == 0:
                q1_last.clear()
                for x, y in q0_last:
                    def process1(xx, yy):
                        if grid[xx % n][yy % m] != "#":
                            if 0 <= xx < n and 0 <= yy < m:
                                if (xx, yy) not in q1:
                                    q1_last.add((xx, yy))
                                    q1.add((xx, yy))

                    process1(xx=x - 1, yy=y)
                    process1(xx=x + 1, yy=y)
                    process1(xx=x, yy=y - 1)
                    process1(xx=x, yy=y + 1)
                results.append(len(q1))
            else:
                q0_last.clear()
                for x, y in q1_last:
                    def process0(xx, yy):
                        if grid[xx % n][yy % m] != "#":
                            if 0 <= xx < n and 0 <= yy < m:
                                if (xx, yy) not in q0:
                                    q0_last.add((xx, yy))
                                    q0.add((xx, yy))

                    process0(xx=x - 1, yy=y)
                    process0(xx=x + 1, yy=y)
                    process0(xx=x, yy=y - 1)
                    process0(xx=x, yy=y + 1)
                results.append(len(q0))
            i_step += 1
        return results

    r_s = solve(i=i_s, j=j_s)
    r_0s = solve(i=0, j=j_s)
    r_ns = solve(i=n - 1, j=j_s)
    r_s0 = solve(i=i_s, j=0)
    r_sm = solve(i=i_s, j=m - 1)
    r_00 = solve(i=0, j=0)
    r_0m = solve(i=0, j=m - 1)
    r_n0 = solve(i=n - 1, j=0)
    r_nm = solve(i=n - 1, j=m - 1)
    # display(r_s)
    # display(r_0s)
    # display(r_s0)
    # display(r_ns)
    # display(r_sm)
    # display(r_00)
    # display(r_n0)
    # display(r_0m)
    # display(r_nm)

    center_total = r_s[-1] if (n_steps - len(r_s)) % 2 == 1 else r_s[-2]
    center_total_skip = r_s[-1] if (n_steps - len(r_s)) % 2 == 0 else r_s[-2]
    # print(n, m, i_s, j_s, "Grid is a square with odd number of cells, starting point is exact center")

    total_mid = 0
    remaining_steps_mid = n_steps
    remaining_steps_mid -= i_s
    remaining_steps_mid -= 1
    while remaining_steps_mid >= 0:
        for r in [r_0s, r_ns, r_s0, r_sm]:
            total_mid += r[remaining_steps_mid] if remaining_steps_mid < len(r) else center_total_skip
        remaining_steps_mid -= n
        if remaining_steps_mid >= 0:
            for r in [r_0s, r_ns, r_s0, r_sm]:
                total_mid += r[remaining_steps_mid] if remaining_steps_mid < len(r) else center_total
            remaining_steps_mid -= n

    total_corner = 0
    grid_count = 0
    remaining_steps_corner = n_steps
    remaining_steps_corner -= i_s
    remaining_steps_corner -= i_s
    remaining_steps_corner -= 1
    remaining_steps_corner -= 1
    while remaining_steps_corner >= 0:
        grid_count += 1
        for r in [r_00, r_0m, r_n0, r_nm]:
            total_corner += (
                                r[remaining_steps_corner] if remaining_steps_corner < len(r) else center_total
                            ) * grid_count
        remaining_steps_corner -= n
        if remaining_steps_corner >= 0:
            grid_count += 1
            for r in [r_00, r_0m, r_n0, r_nm]:
                total_corner += (
                                    r[remaining_steps_corner] if remaining_steps_corner < len(r) else center_total_skip
                                ) * grid_count
            remaining_steps_corner -= n
    return center_total + total_mid + total_corner


grid_value = example.split("\n")
display(x=walk2(grid=grid_value, n_steps=6))
display(x=walk2(grid=grid_value, n_steps=10))
display(x=walk2(grid=grid_value, n_steps=50))
display(x=walk2(grid=grid_value, n_steps=100))
# display(x=walk2(grid=grid_value, n_steps=500))
# display(x=walk2(grid=grid_value, n_steps=1000))
# display(x=walk2(grid=grid_value, n_steps=5000))
# print()


grid_value = s
display(x=walk2(grid=grid_value, n_steps=6))
display(x=walk2(grid=grid_value, n_steps=10))
display(x=walk2(grid=grid_value, n_steps=50))
display(x=walk2(grid=grid_value, n_steps=100))
display(x=walk2(grid=grid_value, n_steps=500))
print()

# n = 390
# test_range = range(n, n + 20)
# for n in test_range:
#     print(n)
#     display(x=walk2(grid=grid_value, n_steps=n))
#     display(x=walk2bis(grid=grid_value, n_steps=n))
#     display(x=walk2bis(grid=grid_value, n_steps=n) - walk2(grid=grid_value, n_steps=n))
#     print()
# display(x=walk2(grid=grid_value, n_steps=1000))
# display(x=walk2(grid=grid_value, n_steps=5000))
# display(x=walk2(grid=grid_value, n_steps=26501365))
print()

# walk2 is too slow
# count the grids fully completed
# count the number of plots for any number of steps for given starting points
# the central grid is complete
# starting points are either a corner or a middle of edge
# these are optimal entry points because of manhattan distance (not a real circle)
# because our grid has traversing lines and open edges
grid_value = s
display(x=walk2bis(grid=grid_value, n_steps=26501365))
