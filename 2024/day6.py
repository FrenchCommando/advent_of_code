import re
from utils.printing import display

example = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""



with open("day6.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    n = len(l)
    m = len(l[0])

    seen = dict(
        up=set(),
        right=set(),
        down=set(),
        left=set(),
    )
    increment = dict(
        up=(-1, 0),
        right=(0, 1),
        down=(1, 0),
        left=(0, -1),
    )

    def direction():
        dirs = seen.keys()
        while True:
            for one_direction in dirs:
                yield one_direction
    it_direction = direction()

    flat = "".join(l)
    flat_length = len(flat)
    start = flat.index("^")
    start_x, start_y = start // m, start % m
    print(start, start_x, start_y)

    grid = [[False for j in range(m)] for i in range(n)]

    current_position = start_x, start_y
    while True:
        current_direction = next(it_direction)
        current_increment = increment[current_direction]

        inside = True
        walking = True
        while inside and walking:
            grid[current_position[0]][current_position[-1]] = True
            if not (0<=current_position[0] + current_increment[0] <n and 0<=current_position[-1] + current_increment[-1]<m):
                inside = False
                break
            if l[current_position[0] + current_increment[0]][current_position[-1] + current_increment[-1]] == "#":
                walking = False
                if current_position in seen[current_direction]:
                    inside = False
                else:
                    seen[current_direction].add(current_position)
                break
            current_position = current_position[0] + current_increment[0], current_position[-1] + current_increment[-1]
        if not inside:
            break
    return sum(sum(line) for line in grid)


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    n = len(l)
    m = len(l[0])

    seen = dict(
        up=set(),
        right=set(),
        down=set(),
        left=set(),
    )
    seen_for_loop = dict(
        up=set(),
        right=set(),
        down=set(),
        left=set(),
    )
    increment = dict(
        up=(-1, 0),
        right=(0, 1),
        down=(1, 0),
        left=(0, -1),
    )

    def direction():
        dirs = seen.keys()
        while True:
            for one_direction in dirs:
                yield one_direction
    it_direction = direction()

    flat = "".join(l)
    flat_length = len(flat)
    start = flat.index("^")
    start_x, start_y = start // m, start % m
    print(start, start_x, start_y)

    grid = [[False for j in range(m)] for i in range(n)]

    loop_count = 0
    current_position = start_x, start_y
    current_direction = next(it_direction)
    while True:
        next_direction = next(it_direction)
        current_increment = increment[current_direction]

        inside = True
        walking = True
        while inside and walking:
            grid[current_position[0]][current_position[-1]] = True
            i_loop = 0
            while True:
                this_position = (current_position[0]- i_loop * current_increment[0], current_position[-1]- i_loop * current_increment[-1])
                if not (0 <= this_position[0] < n and 0 <= this_position[-1] < m):
                    break
                if l[this_position[0]][this_position[-1]] == "#":
                    break
                seen_for_loop[current_direction].add(this_position)
                i_loop += 1
            if current_position in seen_for_loop[next_direction]:
                print(current_position, current_direction, next_direction)
                loop_count += 1
            if not (0<=current_position[0] + current_increment[0] <n and 0<=current_position[-1] + current_increment[-1]<m):
                inside = False
                break
            if l[current_position[0] + current_increment[0]][current_position[-1] + current_increment[-1]] == "#":
                walking = False
                if current_position in seen[current_direction]:
                    inside = False
                else:
                    seen[current_direction].add(current_position)
                break
            current_position = current_position[0] + current_increment[0], current_position[-1] + current_increment[-1]
        if not inside:
            break
        current_direction = next_direction
    return loop_count


p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
