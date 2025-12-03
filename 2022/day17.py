from itertools import cycle
from utils.printing import display


with open("day17.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


width = 7
offset_x, offset_y = 3, 2
blocks = [
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)),
    ((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 0), (0, 1), (1, 0), (1, 1)),
]


def print_rocks(x):
    for line in x:
        print("".join("#" if u else "." for u in line))


def print_block(x):
    x_max = max(u[0] for u in x)
    y_max = max(u[-1] for u in x)
    block_grid = [[False for j in range(y_max + 1)] for i in range(x_max + 1)]
    for (i, j) in x:
        block_grid[i][j] = True
    print_rocks(x=block_grid)


def place_block(grid, block, winds):
    offset = len(grid) + offset_x, offset_y
    progressing = True
    while progressing:
        def progress_wind(offset_internal, wind):
            offset_shifted = offset_internal[0], offset_internal[-1] + (1 if wind == ">" else -1)
            for (cell_x_internal, cell_y_internal) in block:
                target_x_internal, target_y_internal = \
                    cell_x_internal + offset_shifted[0], cell_y_internal + offset_shifted[-1]
                if target_y_internal < 0 or target_y_internal >= width:
                    return offset_internal
                if target_x_internal < len(grid):
                    if grid[target_x_internal][target_y_internal]:
                        return offset_internal
            return offset_shifted
        offset = progress_wind(offset, next(winds))

        def progress_fall(offset_internal):
            offset_shifted = offset_internal[0] - 1, offset_internal[-1]
            for (cell_x_internal, cell_y_internal) in block:
                target_x_internal, target_y_internal = \
                    cell_x_internal + offset_shifted[0], cell_y_internal + offset_shifted[-1]
                if target_x_internal < len(grid):
                    if len(grid) == 0:
                        return offset_internal, False
                    if grid[target_x_internal][target_y_internal]:
                        return offset_internal, False
            return offset_shifted, True
        offset, progressing = progress_fall(offset)
    for (cell_x, cell_y) in block:
        target_x, target_y = cell_x + offset[0], cell_y + offset[-1]
        if target_x == len(grid):
            grid.append([False for i in range(width)])
        grid[target_x][target_y] = True


def find_full_line(grid, empty_start):
    for i, line in enumerate(grid[empty_start:], empty_start):
        # print(i, line)
        if all(line):
            return i


def fall_one_block(grid, block, winds):
    # print_rocks(x=grid)
    # print()
    # print_block(block)
    # print()
    place_block(grid, block, winds)


def fall(grid, n_blocks):
    block_stream = cycle(blocks)
    winds = cycle(lines[0])

    n_blocks_for_period = len(lines[0]) * len(blocks) * 10
    print(f"N blocks for period {n_blocks_for_period}")

    l_size = [len(grid)]
    for i_block in range(min(n_blocks_for_period, n_blocks)):
        fall_one_block(grid, next(block_stream), winds)
        l_size.append(len(grid))

    if n_blocks < len(l_size):
        return l_size[n_blocks]

    index_min = len(lines[0]) * len(blocks)
    start_period = index_min

    def get_period():
        start_candidate = start_period + index_min
        offset = 0
        while start_candidate + offset + 1 < len(l_size):
            offset = 0
            while (l_size[start_candidate + offset + 1] - l_size[start_candidate + offset]) == \
                    (l_size[start_period + offset + 1] - l_size[start_period + offset]):
                if start_candidate == start_period + offset:
                    return offset
                offset += 1
            start_candidate += 1

    period = get_period()
    if period is not None:
        n_post_start = n_blocks - start_period
        quotient, remainder = n_post_start // period, n_post_start % period
        period_increment = l_size[start_period + period] - l_size[start_period]
        remainder_increment = l_size[start_period + remainder] - l_size[start_period]
        return l_size[start_period] + period_increment * quotient + remainder_increment


grid_init = []
answer = fall(grid=grid_init, n_blocks=2022)
print(answer)
# print_rocks(x=grid_init)
# print(len(grid_init))


grid_init2 = []
answer = fall(grid=grid_init2, n_blocks=1000000000000)
print(answer)
# print_rocks(x=grid_init)
# print(len(grid_init2))
