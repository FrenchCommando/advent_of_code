import re
from utils.printing import display


with open("day22.txt", "r") as f:
    lines = f.readlines()


lines = [line.replace('\n', '') for line in lines]
display(lines)

max_line = max(len(line) for line in lines[:-2])
grid = [f"{line: <{max_line}}" for line in lines[:-2]]
display(grid)

path = lines[-1]
display(path)

for line in grid:
    print(line)
print()

turn_right = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
turn_left = {'>': '^', '^': '<', '<': 'v', 'v': '>'}
turn_invert = {'>': '<', '^': 'v', '<': '>', 'v': '^'}


def next_right(one_line):
    out = [-1 for i in one_line]
    left_index = -1
    for i, c in enumerate(one_line):
        if c == ' ':
            left_index = -1
        elif c == '.':
            if left_index == -1:
                left_index = i
            if i + 1 == len(one_line):
                next_char_wrap = one_line[left_index]
                if next_char_wrap == '.':
                    out[i] = left_index
                elif next_char_wrap == '#':
                    out[i] = i
            else:
                next_char = one_line[i + 1]
                if next_char == '.':
                    out[i] = i + 1
                elif next_char == ' ':
                    next_char_wrap = one_line[left_index]
                    if next_char_wrap == '.':
                        out[i] = left_index
                    elif next_char_wrap == '#':
                        out[i] = i
                else:
                    out[i] = i
        elif c == '#':
            if left_index == -1:
                left_index = i
    return out


def invert_right(one_right):
    out = [-1 for i in one_right]
    for i, val in enumerate(one_right):
        if val != -1:
            out[i] = i
    for i, val in enumerate(one_right):
        if val != -1:
            if val != i:
                out[val] = i
    return out


def transpose_grid(one_grid):
    return [[one_grid[i][j] for i in range(len(one_grid))] for j in range(len(one_grid[0]))]


right = [next_right(one_line=line) for line in grid]
left = [invert_right(one_right=line) for line in right]
trans_grid = transpose_grid(one_grid=grid)
trans_down = [next_right(one_line=line) for line in trans_grid]
trans_up = [invert_right(one_right=line) for line in trans_down]
down = transpose_grid(one_grid=trans_down)
up = transpose_grid(one_grid=trans_up)
# print("Right")
# for line in right:
#     print(line)
# print()
# print('Left')
# for line in left:
#     print(line)
# print()
# print('Down')
# for line in down:
#     print(line)
# print()
# print('Up')
# for line in up:
#     print(line)
# print()


def advance(position, action):
    if action == 0:
        return position
    if action == 'L':
        return position[0], position[1], turn_left[position[2]]
    if action == 'R':
        return position[0], position[1], turn_right[position[2]]
    if position[2] == '>':
        return advance(position=(position[0], right[position[0]][position[1]], position[2]), action=action - 1)
    if position[2] == '<':
        return advance(position=(position[0], left[position[0]][position[1]], position[2]), action=action - 1)
    if position[2] == 'v':
        return advance(position=(down[position[0]][position[1]], position[1], position[2]), action=action - 1)
    if position[2] == '^':
        return advance(position=(up[position[0]][position[1]], position[1], position[2]), action=action - 1)


def score(position):
    return 1000 * (position[0] + 1) + 4 * (position[1] + 1) + {'>': 0, 'v': 1, '<': 2, '^': 3}[position[2]]


n_path = list(map(
    lambda s: s if s in 'LR' else int(s),
    filter(lambda s: s != '', re.split(r'(\d+)', path))
))
print(n_path)
print()

start = (0, grid[0].index('.'), '>')
# print(start)
current_position = start
for step in n_path:
    current_position = advance(position=current_position, action=step)
    # print(step, current_position)
print(score(position=current_position))
# 200070 too high


def step_direction(position, opposite=False):
    direction_right = turn_left[position[2]] if opposite else turn_right[position[2]]
    if direction_right == '>':
        if position[1] == len(grid[0]) - 1:
            return None
        position_0 = position[0]
        position_1 = position[1] + 1
    if direction_right == 'v':
        if position[0] == len(grid) - 1:
            return None
        position_0 = position[0] + 1
        position_1 = position[1]
    if direction_right == '<':
        if position[1] == 0:
            return None
        position_0 = position[0]
        position_1 = position[1] - 1
    if direction_right == '^':
        if position[0] == 0:
            return None
        position_0 = position[0] - 1
        position_1 = position[1]
    if grid[position_0][position_1] == " ":
        return None
    return position_0, position_1, position[2]


def rotate_left(position):
    return position[0], position[1], turn_left[position[2]]


def rotate_right(position):
    return position[0], position[1], turn_right[position[2]]


def rotate_invert(position):
    return position[0], position[1], turn_invert[position[2]]


def advance_border(position, s_corners_out, s_corners_in):
    position_one = step_direction(position=position)
    if position_one is None:
        s_corners_in.add(position)
        position_right = rotate_right(position=position)
        return position_right
    position_left = rotate_left(position=position_one)
    position_one_left = step_direction(position=position_left)
    if position_one_left is None:
        return position_one
    s_corners_out.add(position_one)
    return position_one_left


def build_surgical_grid():
    for line in grid:
        print(line)
    print()
    corners_out = set()
    corners_in = set()
    points = set()
    d = dict()
    surgical_start = (0, grid[0].index('.'), '^')  # interior in on the right
    surgical_end = (0, grid[0].index('.'), '<')
    print(surgical_start)
    print(surgical_end)
    point = surgical_start
    while point != surgical_end:
        points.add(point)
        point = advance_border(position=point, s_corners_out=corners_out, s_corners_in=corners_in)
    points.add(point)
    print("CornersIn", corners_in)
    print("CornersOut", corners_out)
    print("Points", len(points), points)
    for corner_out in corners_out:
        right_corner = rotate_left(position=corner_out)
        left_corner = corner_out
        right_corner_next = step_direction(position=right_corner)
        left_corner_next = step_direction(position=left_corner, opposite=True)
        while right_corner_next is not None and left_corner_next is not None:
            right_corner = right_corner_next
            left_corner = left_corner_next
            if right_corner not in points or left_corner not in points:
                print(f"{right_corner=} or {left_corner=} not in {points=}")
            points.remove(left_corner)
            points.remove(right_corner)
            d[left_corner] = rotate_invert(position=right_corner)
            d[right_corner] = rotate_invert(position=left_corner)
            print(left_corner, right_corner)
            right_corner_next = step_direction(position=right_corner)
            left_corner_next = step_direction(position=left_corner, opposite=True)
            if right_corner_next is None and left_corner_next is not None:
                right_corner_next = rotate_right(position=right_corner)
                print("RightCorner", right_corner_next)
            elif right_corner_next is not None and left_corner_next is None:
                left_corner_next = rotate_left(position=left_corner)
                print("LeftCorner", left_corner_next)
        print()

    print("Points", len(points), points)
    print("Surgery", d)
    # for k, v in d.items():
    #     print("\t\t", k, v)
    return d


surgical_move = build_surgical_grid()


def move_surgical(position):
    if position in surgical_move:
        destination = surgical_move[position]
        if grid[destination[0]][destination[1]] == ".":
            return destination
        else:
            return position


def advance2(position, action):
    print("\t", position, action)
    if action == 0:
        return position
    if action == 'L':
        return position[0], position[1], turn_left[position[2]]
    if action == 'R':
        return position[0], position[1], turn_right[position[2]]
    surgical_out = move_surgical(position=position)
    if surgical_out is not None:
        return advance2(position=surgical_out, action=action - 1)
    if position[2] == '>':
        return advance2(position=(position[0], right[position[0]][position[1]], position[2]), action=action - 1)
    if position[2] == '<':
        return advance2(position=(position[0], left[position[0]][position[1]], position[2]), action=action - 1)
    if position[2] == 'v':
        return advance2(position=(down[position[0]][position[1]], position[1], position[2]), action=action - 1)
    if position[2] == '^':
        return advance2(position=(up[position[0]][position[1]], position[1], position[2]), action=action - 1)


current_position = start
for step in n_path:
    current_position = advance2(position=current_position, action=step)
    print(step, current_position)
print(score(position=current_position))
