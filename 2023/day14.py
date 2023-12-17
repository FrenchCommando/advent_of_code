from utils.printing import display


example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


with open("day14.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def cube_rock(grid):
    rocks = {(i, j) for i, line in enumerate(grid) for j, r in enumerate(line) if r == "#"}
    elements = [[] for i in range(len(grid[0]))]
    for i, j in rocks:
        elements[j].append(i)
    return [sorted(l_elements) for l_elements in elements]


def rock_count(grid, l_cube_rock):
    counts = [{i: 0 for i in line} for line in l_cube_rock]
    for d in counts:
        d[-1] = 0
    rocks = {(i, j) for i, line in enumerate(grid) for j, r in enumerate(line) if r == "O"}
    for i, j in rocks:
        obstacle = max(d for d in counts[j].keys() if d < i)
        counts[j][obstacle] += 1
    return counts


def weight_count(grid, l_rock_count):
    n = len(grid)

    def weight(count, last):
        out = (last + last - count + 1) * count // 2  # is int
        return out

    def weight_d(d):
        return sum(weight(last=n - k - 1, count=v) for k, v in d.items())

    return [weight_d(d=one_rock_count) for one_rock_count in l_rock_count]


# i_grid = example.split("\n")
i_grid = s
i_cube_rock = cube_rock(grid=i_grid)
i_rock_count = rock_count(grid=i_grid, l_cube_rock=i_cube_rock)
i_weight = weight_count(grid=i_grid, l_rock_count=i_rock_count)
display(x=i_rock_count)
display(x=i_weight)
display(x=sum(i_weight))


def gravitate(grid):
    l_cube_rock = cube_rock(grid=grid)
    l_rock_count = rock_count(grid=grid, l_cube_rock=l_cube_rock)
    n = len(grid)
    m = len(grid[0])
    out_grid = [["." for j in range(m)] for i in range(n)]

    # fill cube rocks
    for j, d in enumerate(l_cube_rock):
        for i in d:
            out_grid[i][j] = "#"
    for j, d in enumerate(l_rock_count):
        for i, c in d.items():
            for k in range(c):
                out_grid[i + k + 1][j] = "O"
    return out_grid


def rotate_grid(grid):
    n = len(grid)
    m = len(grid[0])
    out = [[grid[n - 1 - i][j] for i in range(n)] for j in range(m)]
    return out


def apply_cycle(grid):
    for i in range(4):
        grid = gravitate(grid=grid)
        grid = rotate_grid(grid=grid)

    # for line in grid:
    #     print(line)
    # print()
    return grid


def clean_weight(grid):
    rep = []
    n = len(grid)
    for i, line in enumerate(grid):
        count = line.count("O")
        rep.append(count * (n - i))
    return rep


def weight_cycle(grid, n):
    l_grid = grid
    l_weight = 0
    weight_index = {}
    weight_gap = {}
    for cycle in range(n):
        l_grid = apply_cycle(grid=l_grid)
        l_weight = sum(clean_weight(grid=l_grid))
        if l_weight in weight_index:
            weight_gap[l_weight] = cycle + 1 - weight_index[l_weight]
        weight_index[l_weight] = cycle + 1

        print(cycle, l_weight)
        print("Gap", weight_gap)
        print("Index", weight_index)
        max_gap = max(weight_gap.values()) if weight_gap else None
        for k, v in weight_gap.items():
            remainder = (n_cycles - weight_index[k]) % v
            if remainder == 0:
                if v == max_gap:
                    print(k, remainder, v)
                    print()
            # spot zero remainder, and max period
    return l_weight


n_cycles = 1000000000
i_weight_post_cycle = weight_cycle(grid=i_grid, n=n_cycles)
display(x=i_weight_post_cycle)
