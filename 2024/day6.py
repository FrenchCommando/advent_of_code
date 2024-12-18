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
    print("Start", start, start_x, start_y)

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
    increment = dict(
        up=(-1, 0),
        right=(0, 1),
        down=(1, 0),
        left=(0, -1),
    )

    def direction(first_direction):
        dirs = seen.keys()
        found = False
        for one_direction in dirs:
            if not found and one_direction != first_direction:
                continue
            found = True
            yield one_direction
        while True:
            for one_direction in dirs:
                yield one_direction
    it_direction = direction(first_direction="up")

    flat = "".join(l)
    # flat_length = len(flat)
    start = flat.index("^")
    start_x, start_y = start // m, start % m
    print("Start", start, start_x, start_y)

    loops = set()
    current_position = start_x, start_y
    while True:
        current_direction = next(it_direction)
        current_increment = increment[current_direction]

        inside = True
        walking = True
        while inside and walking:
            next_position = (current_position[0] + current_increment[0], current_position[-1] + current_increment[-1])

            def confirm_obstacle(candidate_internal):
                position_internal = (start_x, start_y)
                direction_internal = "up"
                if not (0 <= candidate_internal[0] < n and 0 <= candidate_internal[-1] < m):
                    return False
                if l[candidate_internal[0]][candidate_internal[-1]] == "^":
                    return False
                if l[candidate_internal[0]][candidate_internal[-1]] == "#":
                    return False
                seen_for_obstacle = dict(up=set(), right=set(), down=set(), left=set())

                it_direction_obs = direction(first_direction=direction_internal)
                while True:
                    direction_internal = next(it_direction_obs)
                    increment_internal = increment[direction_internal]
                    walking_internal = True
                    while walking_internal:
                        # print(loops, seen, seen_for_obstacle, direction_internal, position_internal)
                        position_internal_next = (position_internal[0] + increment_internal[0],
                                                  position_internal[-1] + increment_internal[-1])
                        if not (0 <= position_internal_next[0] < n and 0 <= position_internal_next[-1] < m):
                            return False

                        if (l[position_internal_next[0]][position_internal_next[-1]] == "#"
                                or position_internal_next == candidate_internal):
                            walking_internal = False
                            if position_internal in seen_for_obstacle[direction_internal]:
                                return True
                            else:
                                seen_for_obstacle[direction_internal].add(position_internal)
                            break
                        position_internal = position_internal_next

            if confirm_obstacle(
                    candidate_internal=next_position,
            ):
                loops.add(next_position)
                # print(next_position, loops)

            if not (0 <= next_position[0] < n and 0 <= next_position[-1] < m):
                inside = False
                break
            if l[next_position[0]][next_position[-1]] == "#":
                walking = False
                if current_position in seen[current_direction]:
                    inside = False
                else:
                    seen[current_direction].add(current_position)
                break

            current_position = next_position
        if not inside:
            break
    return len(loops)


p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
