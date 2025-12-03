from utils.printing import display

example = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

example2 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""


with open("day15.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    i = iter(l)
    grid = []
    try:
        while True:
            line = next(i)
            if not line:
                break
            grid.append(list(line.strip()))
    except StopIteration:
        pass
    for u, line in enumerate(grid):
        print(line, u)

    l_moves = []

    try:
        while True:
            line = next(i)
            l_moves.append(line.strip())
    except StopIteration:
        pass
    moves = "".join(l_moves)
    print(moves)


    def increment(move_internal, position):
        if move_internal == "^":
            return position[0] - 1, position[-1]
        if move_internal == "v":
            return position[0] + 1, position[-1]
        if move_internal == ">":
            return position[0], position[-1] + 1
        if move_internal == "<":
            return position[0], position[-1] - 1


    n = len(grid)
    m = len(grid[0])
    print("GridSize", n, m)
    z_location = "".join(''.join(line) for line in grid).find("@")
    location = z_location // m, z_location % m
    print("Location",location)
    for move in moves:
        end_location = location
        while grid[end_location[0]][end_location[-1]] not in ".#":
            end_location = increment(move, end_location)

        if grid[end_location[0]][end_location[-1]] == "#":
            continue

        grid[location[0]][location[-1]] = "."
        location_plus_one = increment(move, location)
        grid[location_plus_one[0]][location_plus_one[-1]] = "@"
        if end_location != location_plus_one:
            grid[end_location[0]][end_location[-1]] = "O"
        location = location_plus_one

        # print(move)
        # for u, line in enumerate(grid):
        #     print(line, u)

    c = 0
    for ii in range(n):
        for jj in range(m):
            if grid[ii][jj] == "O":
                c += ii * 100 + jj
    return c


p = count(l=example.split("\n"))
p2 = count(l=example2.split("\n"))
print("count", p, p2)
ps = count(l=[line.strip() for line in s])
print("count", ps)
print()


def count2(l):
    i = iter(l)
    grid = []
    try:
        while True:
            line = next(i)
            if not line:
                break
            uber_line = (
                line
                .replace("#", "##")
                .replace(".", "..")
                .replace("O", "[]")
                .replace("@", "@.")
            )
            grid.append(list(uber_line))
    except StopIteration:
        pass
    for u, line in enumerate(grid):
        print(line, u)

    l_moves = []

    try:
        while True:
            line = next(i)
            l_moves.append(line.strip())
    except StopIteration:
        pass
    moves = "".join(l_moves)
    print(moves)


    def increment(move_internal, position):
        if move_internal == "^":
            return position[0] - 1, position[-1]
        if move_internal == "v":
            return position[0] + 1, position[-1]
        if move_internal == ">":
            return position[0], position[-1] + 1
        if move_internal == "<":
            return position[0], position[-1] - 1


    n = len(grid)
    m = len(grid[0])
    print("GridSize", n, m)
    z_location = "".join(''.join(line) for line in grid).find("@")
    location = z_location // m, z_location % m
    print("Location",location)
    for move in moves:
        def push(position):
            # print(position)
            if grid[position[0]][position[-1]] == "#":
                nonlocal good
                good = False
                return
            if grid[position[0]][position[-1]] == ".":
                return

            position_next = increment(move, position)
            gg = grid[position[0]][position[-1]]
            target[position_next] = gg

            if move in "^v":
                if grid[position[0]][position[-1]] == "]":
                    if (position[0], position[-1] - 1) not in target:
                        target[(position[0], position[-1] - 1)] = "."
                        push((position[0], position[-1] - 1))
                if grid[position[0]][position[-1]] == "[":
                    if (position[0], position[-1] + 1) not in target:
                        target[(position[0], position[-1] + 1)] = "."
                        push((position[0], position[-1] + 1))
            push((position_next[0], position_next[-1]))

        target = {location: "."}
        good = True
        push(location)
        if good:
            for pp, cc in target.items():
                grid[pp[0]][pp[-1]] = cc
            location = increment(move, location)

        # print(move)
        # for u, line in enumerate(grid):
        #     print(line, u)

    c = 0
    for ii in range(n):
        for jj in range(m):
            if grid[ii][jj] == "[":
                c += ii * 100 + jj
    return c


p21 = count2(l=example.split("\n"))
p22 = count2(l=example2.split("\n"))
print("count2", p21, p22)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
