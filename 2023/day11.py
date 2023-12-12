from utils.printing import display

example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


with open("day11.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def transpose(grid):
    n = len(grid)
    m = len(grid[0])

    return [''.join(grid[i][j] for i in range(n)) for j in range(m)]


def compute(grid, zero_gap=2):
    counts = [line.count("#") for line in grid]
    result = 0
    current_n = 0
    current_d = 0
    for c in counts:
        result += c * current_d
        current_n += c
        current_d += current_n * (zero_gap if c == 0 else 1)
    return result


l_grid = example.split("\n")
t_grid = transpose(grid=l_grid)
display(x=l_grid)
display(x=t_grid)

l_result = compute(grid=l_grid)
t_result = compute(grid=t_grid)
display(x=l_result)
display(x=t_result)
display(x=l_result + t_result)

display(x=compute(grid=l_grid, zero_gap=2) + compute(grid=t_grid, zero_gap=2))
display(x=compute(grid=l_grid, zero_gap=10) + compute(grid=t_grid, zero_gap=10))
display(x=compute(grid=l_grid, zero_gap=100) + compute(grid=t_grid, zero_gap=100))

l_grid = s
t_grid = transpose(grid=l_grid)
display(x=compute(grid=l_grid, zero_gap=2) + compute(grid=t_grid, zero_gap=2))
display(x=compute(grid=l_grid, zero_gap=1_000_000) + compute(grid=t_grid, zero_gap=1_000_000))
