import re
from utils.printing import display


with open("day9.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


# first round to size the universe
def max_dimensions():
    def move_internal(line):
        nonlocal i, j
        direction_internal, number_internal = line.split(" ")
        number_value_internal = int(number_internal)
        if direction_internal == "U":
            i -= number_value_internal
        elif direction_internal == "D":
            i += number_value_internal
        elif direction_internal == "L":
            j -= number_value_internal
        elif direction_internal == "R":
            j += number_value_internal
        return i, j

    i, j = 0, 0
    x_min_internal = min((move_internal(line=line)[0] for line in lines))
    i, j = 0, 0
    y_min_internal = min((move_internal(line=line)[1] for line in lines))
    i, j = 0, 0
    x_max_internal = max((move_internal(line=line)[0] for line in lines))
    i, j = 0, 0
    y_max_internal = max((move_internal(line=line)[1] for line in lines))
    return x_min_internal, y_min_internal, x_max_internal, y_max_internal


display(max_dimensions())
x_min, y_min, x_max, y_max = max_dimensions()


def fill_visited(i, j):
    visited_grid[i - x_min][j - y_min] = True


def move(direction_internal, number_value_internal):
    if number_value_internal == 0:
        return
    if direction_internal == "U":
        i_position[0] -= 1
    elif direction_internal == "D":
        i_position[0] += 1
    elif direction_internal == "L":
        j_position[0] -= 1
    elif direction_internal == "R":
        j_position[0] += 1

    for k in range(len(i_position) - 1):
        if (i_position[k + 1] == i_position[k] + 2) and (j_position[k + 1] == j_position[k] + 2):
            i_position[k + 1], j_position[k + 1] = i_position[k] + 1, j_position[k] + 1
        elif (i_position[k + 1] == i_position[k] + 2) and (j_position[k + 1] == j_position[k] - 2):
            i_position[k + 1], j_position[k + 1] = i_position[k] + 1, j_position[k] - 1
        elif (i_position[k + 1] == i_position[k] - 2) and (j_position[k + 1] == j_position[k] + 2):
            i_position[k + 1], j_position[k + 1] = i_position[k] - 1, j_position[k] + 1
        elif (i_position[k + 1] == i_position[k] - 2) and (j_position[k + 1] == j_position[k] - 2):
            i_position[k + 1], j_position[k + 1] = i_position[k] - 1, j_position[k] - 1
        elif i_position[k + 1] == i_position[k] + 2:
            i_position[k + 1], j_position[k + 1] = i_position[k] + 1, j_position[k]
        elif i_position[k + 1] == i_position[k] - 2:
            i_position[k + 1], j_position[k + 1] = i_position[k] - 1, j_position[k]
        elif j_position[k + 1] == j_position[k] + 2:
            i_position[k + 1], j_position[k + 1] = i_position[k], j_position[k] + 1
        elif j_position[k + 1] == j_position[k] - 2:
            i_position[k + 1], j_position[k + 1] = i_position[k], j_position[k] - 1

    fill_visited(i=i_position[-1], j=j_position[-1])
    move(
        direction_internal=direction_internal,
        number_value_internal=number_value_internal - 1,
    )


visited_grid = [
    [False for y in range(y_min, y_max + 1)]
    for x in range(x_min, x_max + 1)
]
rope_length = 2
i_position = [0 for ki in range(rope_length)]
j_position = [0 for kj in range(rope_length)]
fill_visited(i=i_position[-1], j=j_position[-1])
for line in lines:
    direction, number = line.split(" ")
    number_value = int(number)
    move(direction, number_value)
display(sum(sum(visited_line) for visited_line in visited_grid))


for rope_length in range(2, 11):
    visited_grid = [
        [False for y in range(y_min, y_max + 1)]
        for x in range(x_min, x_max + 1)
    ]
    i_position = [0 for ki in range(rope_length)]
    j_position = [0 for kj in range(rope_length)]
    fill_visited(i=i_position[-1], j=j_position[-1])
    for line in lines:
        direction, number = line.split(" ")
        number_value = int(number)
        move(direction, number_value)
    display(rope_length)
    display(sum(sum(visited_line) for visited_line in visited_grid))
