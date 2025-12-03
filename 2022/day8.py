import re
from utils.printing import display


with open("day8.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)

visible_grid = [
    [False for ii in range(len(line))] for line in lines
]


def process():
    for i, line in enumerate(lines):
        s = list(map(lambda x: int(x), line))
        # print(s)
        index = 0
        value = s[index]
        visible_grid[i][index] = True
        while index < len(s):
            if s[index] > value:
                value = s[index]
                visible_grid[i][index] = True
            index += 1


process()
display(sum(sum(line) for line in visible_grid))

lines = [line[::-1] for line in lines]
visible_grid = [line[::-1] for line in visible_grid]
process()
display(sum(sum(line) for line in visible_grid))

lines = [[lines[x][y] for x in range(len(lines))] for y in range(len(lines[0]))]
visible_grid = [[visible_grid[x][y] for x in range(len(visible_grid))] for y in range(len(visible_grid[0]))]
process()
display(sum(sum(line) for line in visible_grid))

lines = [line[::-1] for line in lines]
visible_grid = [line[::-1] for line in visible_grid]
process()
display(sum(sum(line) for line in visible_grid))

display(len(visible_grid) * len(visible_grid[0]))


def scenic_score(i, j):
    value = lines[i][j]
    i_left = i
    while i_left > 0 and (lines[i_left][j] < value or i == i_left):
        i_left -= 1
    i_right = i
    while i_right < len(lines) - 1 and (lines[i_right][j] < value or i == i_right):
        i_right += 1
    j_left = j
    while j_left > 0 and (lines[i][j_left] < value or j == j_left):
        j_left -= 1
    j_right = j
    while j_right < len(lines[0]) - 1 and (lines[i][j_right] < value or j == j_right):
        j_right += 1
    print(i, j, (i - i_left), (i_right - i), (j - j_left), (j_right - j), (i - i_left) * (i_right - i) * (j - j_left) * (j_right - j))
    return (i - i_left) * (i_right - i) * (j - j_left) * (j_right - j)


display(max(
    scenic_score(i=i, j=j)
    for i in range(len(lines))
    for j in range(len(lines[0]))
))
