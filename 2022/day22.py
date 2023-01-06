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


print("Right")
right = [next_right(one_line=line) for line in grid]
for line in right:
    print(line)
print()
print('Left')
left = [invert_right(one_right=line) for line in right]
for line in left:
    print(line)
print()

trans_grid = transpose_grid(one_grid=grid)
trans_down = [next_right(one_line=line) for line in trans_grid]
trans_up = [invert_right(one_right=line) for line in trans_down]
down = transpose_grid(one_grid=trans_down)
up = transpose_grid(one_grid=trans_up)
print('Down')
for line in down:
    print(line)
print()
print('Up')
for line in up:
    print(line)
print()


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
print(start)

current_position = start
for step in n_path:
    current_position = advance(position=current_position, action=step)
    print(step, current_position)


print(score(position=current_position))
# 200070 too high
