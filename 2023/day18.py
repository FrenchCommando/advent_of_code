import re

from utils.printing import display
import queue

example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


with open("day18.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def parse(text):
    pattern = r"(?P<letter>([DLUR])) (?P<number>([0-9]+)) \(#(?P<hexcode>(.*))\)"
    res = []
    for line in text:
        d = re.fullmatch(pattern=pattern, string=line).groupdict()
        res.append((d['letter'], int(d['number'])))
    return res


def parse2(text):
    pattern = r"(?P<letter>([DLUR])) (?P<number>([0-9]+)) \(#(?P<hexcode>(.*))(?P<direction>[0-3])\)"
    direction_mapping = {
        '0': "R",
        '1': "D",
        '2': "L",
        '3': "U",
    }
    res = []
    for line in text:
        d = re.fullmatch(pattern=pattern, string=line).groupdict()
        val = (direction_mapping[d['direction']], int(d['hexcode'], 16))
        res.append(val)
    return res


def build(steps):
    x_min, x_max = 0, 0
    y_min, y_max = 0, 0
    x, y = 0, 0
    for d in steps:
        letter, number = d
        if letter == "U":
            x -= number
            x_min = min(x_min, x)
        elif letter == "D":
            x += number
            x_max = max(x_max, x)
        elif letter == "L":
            y -= number
            y_min = min(y_min, y)
        elif letter == "R":
            y += number
            y_max = max(y_max, y)
    n_x = x_max - x_min + 1
    n_y = y_max - y_min + 1
    grid = [["." for j in range(n_y)] for i in range(n_x)]
    x, y = -x_min, -y_min
    print(f"{x=}, {y=}, {n_x=}, {n_y=}")
    q = queue.Queue()
    for d in steps:
        letter, number = d
        if letter == "U":
            for i in range(number):
                x -= 1
                grid[x][y] = "#"
                if y + 1 < n_y:
                    if grid[x][y + 1] == ".":
                        grid[x][y + 1] = "x"
                        q.put((x, y + 1))
        elif letter == "D":
            for i in range(number):
                x += 1
                grid[x][y] = "#"
                if y - 1 >= 0:
                    if grid[x][y - 1] == ".":
                        grid[x][y - 1] = "x"
                        q.put((x, y - 1))
        elif letter == "L":
            for i in range(number):
                y -= 1
                grid[x][y] = "#"
                if x - 1 >= 0:
                    if grid[x - 1][y] == ".":
                        grid[x - 1][y] = "x"
                        q.put((x - 1, y))
        elif letter == "R":
            for i in range(number):
                y += 1
                grid[x][y] = "#"
                if x + 1 < n_x:
                    if grid[x + 1][y] == ".":
                        grid[x + 1][y] = "x"
                        q.put((x + 1, y))
    while not q.empty():
        x, y = q.get()
        if grid[x][y] == "#":
            continue
        if x - 1 >= 0:
            if grid[x - 1][y] == ".":
                grid[x - 1][y] = "a"
                q.put((x - 1, y))
        if x + 1 < n_x:
            if grid[x + 1][y] == ".":
                grid[x + 1][y] = "a"
                q.put((x + 1, y))
        if y - 1 >= 0:
            if grid[x][y - 1] == ".":
                grid[x][y - 1] = "a"
                q.put((x, y - 1))
        if y + 1 < n_y:
            if grid[x][y + 1] == ".":
                grid[x][y + 1] = "a"
                q.put((x, y + 1))
    # for line in grid:
    #     print(line)
    # print()
    print(grid[-1])

    return grid


def count_grid(grid):
    return {
        symbol: sum(line.count(symbol) for line in grid) for symbol in ["#", "x", "a", "."]
    }


def count_grid2(steps):
    c = 1
    chain = "".join(u[0] for u in steps)
    numbers = [u[1] for u in steps]
    print(chain)
    print(numbers)

    def reduce_positive(p):
        nonlocal c, chain
        index = chain.find(p)
        c1, c2, c3 = p
        if index != -1:
            int_d = numbers[index]
            int_l = numbers[index + 1]
            int_u = numbers[index + 2]
            if int_u == int_d:
                chain = chain[:index] + c2 + chain[index + 3:]
                numbers.pop(index + 2)
                numbers.pop(index)
            elif int_u > int_d:
                chain = chain[:index] + c2 + c3 + chain[index + 3:]
                numbers[index + 2] = int_u - int_d
                numbers.pop(index)
            elif int_u < int_d:
                chain = chain[:index] + c1 + c2 + chain[index + 3:]
                numbers[index] = int_d - int_u
                numbers.pop(index + 2)
            c += (int_l + 1) * min(int_u, int_d)
            # print(int_l, int_u, int_d)
        reduce_all()

    def reduce_negative(p):
        nonlocal c, chain
        index = chain.find(p)
        c1, c2, c3 = p
        if index != -1:
            int_d = numbers[index]
            int_l = numbers[index + 1]
            int_u = numbers[index + 2]
            if int_u == int_d:
                chain = chain[:index] + c2 + chain[index + 3:]
                numbers.pop(index + 2)
                numbers.pop(index)
            elif int_u > int_d:
                chain = chain[:index] + c2 + c3 + chain[index + 3:]
                numbers[index + 2] = int_u - int_d
                numbers.pop(index)
            elif int_u < int_d:
                chain = chain[:index] + c1 + c2 + chain[index + 3:]
                numbers[index] = int_d - int_u
                numbers.pop(index + 2)
            c -= (int_l - 1) * min(int_u, int_d)
            # print(int_l, int_u, int_d)
        reduce_all()

    def reduce_duplicate(p):
        nonlocal c, chain
        pp = p + p
        index = chain.find(pp)
        if index != -1:
            int_1 = numbers[index]
            int_2 = numbers[index + 1]
            chain = chain[:index] + p + chain[index + 2:]
            numbers[index] = int_1 + int_2
            numbers.pop(index + 1)
        # print(c, "\t", chain, "\t", numbers)

    def reduce_round(p):
        nonlocal c, chain
        index = chain.find(p)
        c0, c1, c2 = p
        if index != -1:
            int_1 = numbers[index + 1]
            int_2 = numbers[index + 2]
            if int_1 == int_2:
                chain = chain[:index + 1] + chain[index + 3:]
                numbers.pop(index + 2)
                numbers.pop(index + 1)
            elif int_2 > int_1:
                chain = chain[:index + 1] + c2 + chain[index + 3:]
                numbers[index + 2] = int_2 - int_1
                numbers.pop(index + 1)
            elif int_2 < int_1:
                chain = chain[:index + 1] + c1 + chain[index + 3:]
                numbers[index + 1] = int_1 - int_2
                numbers.pop(index + 2)
            c += min(int_1, int_2)

    def reduce_all_duplicates():
        reduce_duplicate(p="U")
        reduce_duplicate(p="D")
        reduce_duplicate(p="L")
        reduce_duplicate(p="R")

    positive_set = ["DLU", "RDL", "URD", "LUR"]
    negative_set = ["DRU", "RUL", "ULD", "LDR"]  # depends on orientation
    round_set = ["DRL", "RUD", "ULR", "LDU"] + ["RDU", "URL", "LUD", "DLR"]

    def reduce_all():
        reduce_all_duplicates()
        for r in round_set:
            reduce_round(p=r)
        reduce_all_duplicates()

    count = 0
    while len(chain) > 2 and count < 100:
        # print(c, "\t", chain, "\t", numbers)
        for pos in positive_set:
            reduce_positive(p=pos)
        for neg in negative_set:
            reduce_negative(p=neg)
        reduce_all()
        count += 1
    print("Chain", chain)
    print("Number", numbers)
    if len(chain) == 2:
        c += numbers[0]  # only once
    return c


grid_value = example.split("\n")
# grid_value = s
l_parsed = parse(text=grid_value)
l_grid = build(steps=l_parsed)
l_count = count_grid(grid=l_grid)
display(x=l_count)
display(x=sum(l_count[u] for u in "#xa"))
display(x=sum(l_count[u] for u in "#.a"))  # in case oriented the other way

l_parsed2 = parse2(text=grid_value)
# l_parsed2 = l_parsed
l_count2 = count_grid2(steps=l_parsed2)
display(x=l_parsed2)
display(x=l_count2)
