from itertools import cycle
from utils.printing import display


with open("day23.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)

for line in lines:
    print(line)
print()


def large_grid(grid, grid_extension):
    large_grid_out = [
        [
            False for j in range(len(grid[0]) + 2 * grid_extension)
        ] for i in range(len(grid) + 2 * grid_extension)
    ]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "#":
                large_grid_out[i + grid_extension][j + grid_extension] = True
    return large_grid_out


def get_positions(grid):
    l_positions = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]:
                l_positions.append((i, j))
    return l_positions


direction_obstacle = [
    ((-1, 0), ((-1, 0), (-1, -1), (-1, 1))),
    ((+1, 0), ((+1, 0), (+1, -1), (+1, 1))),
    ((0, -1), ((0, -1), (-1, -1), (+1, -1))),
    ((0, +1), ((0, +1), (-1, +1), (+1, +1))),
]
surrounding = [
    (-1, -1), (-1, 0), (-1, +1),
    (0, -1), (0, +1),
    (+1, -1), (+1, 0), (+1, +1),
]


def process(grid, l_positions):
    collision = [[0 for j in range(len(grid[0]))] for i in range(len(grid))]
    grid_end = [[False for j in range(len(grid[0]))] for i in range(len(grid))]
    direction = next(steps)
    next_position = dict()
    no_one_moved_out = True
    for position in l_positions:
        next_position[position] = position
        if not any(grid[position[0] + pos[0]][position[1] + pos[1]] for pos in surrounding):
            continue
        for chosen_direction in range(len(direction_obstacle)):
            target, obstacles = direction_obstacle[(chosen_direction + direction) % len(direction_obstacle)]
            if any(grid[position[0] + pos[0]][position[1] + pos[1]] for pos in obstacles):
                continue
            else:
                next_position[position] = position[0] + target[0], position[1] + target[1]
                collision[position[0] + target[0]][position[1] + target[1]] += 1
                break
    positions_end = []
    for pos_old in next_position:
        pos_new = next_position[pos_old]
        if collision[pos_new[0]][pos_new[1]] == 1:
            positions_end.append(pos_new)
            if pos_new != pos_old:
                no_one_moved_out = False
        else:
            positions_end.append(pos_old)
    for position in positions_end:
        grid_end[position[0]][position[1]] = True

    return grid_end, positions_end, no_one_moved_out


n_periods = 10
n_grid_extension = n_periods
grid_large = large_grid(grid=lines, grid_extension=n_grid_extension)
# for line in grid_large:
#     print(''.join("#" if value else '.' for value in line))
# print()
steps = cycle(range(len(direction_obstacle)))
positions = get_positions(grid=grid_large)
print(len(positions), positions)
for period in range(n_periods):
    grid_large, positions, no_one_moved = process(grid=grid_large, l_positions=positions)
    # for line in grid_large:
    #     print(''.join("#" if value else '.' for value in line))
    # print(positions)
    if no_one_moved:
        print(period + 1, no_one_moved)
        break
    # print()
min_i = min(i for i in range(len(grid_large)) for j in range(len(grid_large[0])) if grid_large[i][j])
max_i = max(i for i in range(len(grid_large)) for j in range(len(grid_large[0])) if grid_large[i][j])
min_j = min(j for i in range(len(grid_large)) for j in range(len(grid_large[0])) if grid_large[i][j])
max_j = max(j for i in range(len(grid_large)) for j in range(len(grid_large[0])) if grid_large[i][j])
print(min_i, max_i, min_j, max_j)
print((max_i - min_i + 1) * (max_j - min_j + 1))
print((max_i - min_i + 1) * (max_j - min_j + 1) - len(positions))
print()


n_periods = 1000
n_grid_extension = len(lines)
grid_large = large_grid(grid=lines, grid_extension=n_grid_extension)
# for line in grid_large:
#     print(''.join("#" if value else '.' for value in line))
# print()
steps = cycle(range(len(direction_obstacle)))
positions = get_positions(grid=grid_large)
print(len(positions), positions)
for period in range(n_periods):
    grid_large, positions, no_one_moved = process(grid=grid_large, l_positions=positions)
    # for line in grid_large:
    #     print(''.join("#" if value else '.' for value in line))
    # print(positions)
    if period % 100 == 0:
        print("Running", period + 1, no_one_moved)
    if no_one_moved:
        print(period + 1, no_one_moved)
        break
    # print()
print()
