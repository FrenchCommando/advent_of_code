import queue
import re
from utils.printing import display

example = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""


example2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


with open("day16.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    n = len(l)
    m = len(l[0])
    ll = ''.join(l)
    l_s = ll.index("S")
    l_e = ll.index("E")
    pose_s = l_s // m, l_s % m
    pose_e = l_e // m, l_e % m
    print("Size", n, m)
    print("Start", pose_s)
    print("End", pose_e)

    big_number = 1e100
    grid = [[dict(N=big_number, S=big_number, E=big_number, W=big_number) for j in range(m)] for i in range(n)]
    print(grid)
    grid[pose_s[0]][pose_s[-1]]['E'] = 0

    q = queue.Queue()
    q.put((pose_s, "E"))

    c_move = 1
    c_turn = 1000

    def move(pos, d):
        if d == "E":
            return pos[0], pos[-1] + 1
        if d == "S":
            return pos[0] + 1, pos[-1]
        if d == "W":
            return pos[0], pos[-1] - 1
        if d == "N":
            return pos[0] - 1, pos[-1]

    while not q.empty():
        pose, d = q.get()
        v = grid[pose[0]][pose[-1]][d]
        if d == "E":
            for d_next, mult in dict(
                N=1, W=2, S=1,
            ).items():
                grid[pose[0]][pose[-1]][d_next] = min(grid[pose[0]][pose[-1]][d_next], v + mult * c_turn)
        if d == "W":
            for d_next, mult in dict(
                N=1, S=1, E=2,
            ).items():
                grid[pose[0]][pose[-1]][d_next] = min(grid[pose[0]][pose[-1]][d_next], v + mult * c_turn)
        if d == "N":
            for d_next, mult in dict(
                W=1, S=2, E=1,
            ).items():
                grid[pose[0]][pose[-1]][d_next] = min(grid[pose[0]][pose[-1]][d_next], v + mult * c_turn)
        if d == "S":
            for d_next, mult in dict(
                N=2, W=1, E=1,
            ).items():
                grid[pose[0]][pose[-1]][d_next] = min(grid[pose[0]][pose[-1]][d_next], v + mult * c_turn)

        for d in ["E", "S", "W", "N"]:
            pose_next = move(pose, d)
            if l[pose_next[0]][pose_next[-1]] != "#":
                if grid[pose_next[0]][pose_next[-1]][d] > grid[pose[0]][pose[-1]][d] + c_move:
                    q.put((pose_next, d))
                    grid[pose_next[0]][pose_next[-1]][d] = grid[pose[0]][pose[-1]][d] + c_move
    print(grid[pose_e[0]][pose_e[-1]])

    return min(grid[pose_e[0]][pose_e[-1]].values())


p = count(l=example.split("\n"))
p2 = count(l=example2.split("\n"))
print("count", p, p2)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    n = len(l)
    m = len(l[0])
    ll = ''.join(l)
    l_s = ll.index("S")
    l_e = ll.index("E")
    pose_s = l_s // m, l_s % m
    pose_e = l_e // m, l_e % m
    print("Size", n, m)
    print("Start", pose_s)
    print("End", pose_e)

    big_number = 1e100
    grid = [
        [
            dict(N=big_number, S=big_number, E=big_number, W=big_number)
            for j in range(m)
        ]
        for i in range(n)
    ]
    path = [
        [
            dict(N=set(), S=set(), E=set(), W=big_number)
            for j in range(m)
        ]
        for i in range(n)
    ]
    # print(grid)
    grid[pose_s[0]][pose_s[-1]]['E'] = 0
    path[pose_s[0]][pose_s[-1]]['E'] = set()

    q = queue.Queue()
    q.put((pose_s, "E"))

    c_move = 1
    c_turn = 1000

    def move(pos, d):
        if d == "E":
            return pos[0], pos[-1] + 1
        if d == "S":
            return pos[0] + 1, pos[-1]
        if d == "W":
            return pos[0], pos[-1] - 1
        if d == "N":
            return pos[0] - 1, pos[-1]

    while not q.empty():
        pose, d = q.get()
        v = grid[pose[0]][pose[-1]][d]
        if d == "E":
            for d_next, mult in dict(
                N=1, W=2, S=1,
            ).items():
                if grid[pose[0]][pose[-1]][d_next] < v + mult * c_turn:
                    continue
                if grid[pose[0]][pose[-1]][d_next] > v + mult * c_turn:
                    grid[pose[0]][pose[-1]][d_next] = v + mult * c_turn
                    path[pose[0]][pose[-1]][d_next] = path[pose[0]][pose[-1]][d].copy()
                elif grid[pose[0]][pose[-1]][d_next] == v + mult * c_turn:
                    if any(u not in path[pose[0]][pose[-1]][d_next] for u in path[pose[0]][pose[-1]][d]):
                        path[pose[0]][pose[-1]][d_next] = set(path[pose[0]][pose[-1]][d] | path[pose[0]][pose[-1]][d_next])

        if d == "W":
            for d_next, mult in dict(
                N=1, S=1, E=2,
            ).items():
                if grid[pose[0]][pose[-1]][d_next] < v + mult * c_turn:
                    continue
                if grid[pose[0]][pose[-1]][d_next] > v + mult * c_turn:
                    grid[pose[0]][pose[-1]][d_next] = v + mult * c_turn
                    path[pose[0]][pose[-1]][d_next] = path[pose[0]][pose[-1]][d].copy()
                elif grid[pose[0]][pose[-1]][d_next] == v + mult * c_turn:
                    if any(u not in path[pose[0]][pose[-1]][d_next] for u in path[pose[0]][pose[-1]][d]):
                        path[pose[0]][pose[-1]][d_next] = set(path[pose[0]][pose[-1]][d] | path[pose[0]][pose[-1]][d_next])
        if d == "N":
            for d_next, mult in dict(
                W=1, S=2, E=1,
            ).items():
                if grid[pose[0]][pose[-1]][d_next] < v + mult * c_turn:
                    continue
                if grid[pose[0]][pose[-1]][d_next] > v + mult * c_turn:
                    grid[pose[0]][pose[-1]][d_next] = v + mult * c_turn
                    path[pose[0]][pose[-1]][d_next] = path[pose[0]][pose[-1]][d].copy()
                elif grid[pose[0]][pose[-1]][d_next] == v + mult * c_turn:
                    if any(u not in path[pose[0]][pose[-1]][d_next] for u in path[pose[0]][pose[-1]][d]):
                        path[pose[0]][pose[-1]][d_next] = set(path[pose[0]][pose[-1]][d] | path[pose[0]][pose[-1]][d_next])
        if d == "S":
            for d_next, mult in dict(
                N=2, W=1, E=1,
            ).items():
                if grid[pose[0]][pose[-1]][d_next] < v + mult * c_turn:
                    continue
                if grid[pose[0]][pose[-1]][d_next] > v + mult * c_turn:
                    grid[pose[0]][pose[-1]][d_next] = v + mult * c_turn
                    path[pose[0]][pose[-1]][d_next] = path[pose[0]][pose[-1]][d].copy()
                elif grid[pose[0]][pose[-1]][d_next] == v + mult * c_turn:
                    if any(u not in path[pose[0]][pose[-1]][d_next] for u in path[pose[0]][pose[-1]][d]):
                        path[pose[0]][pose[-1]][d_next] = set(path[pose[0]][pose[-1]][d] | path[pose[0]][pose[-1]][d_next])

        for d in ["E", "S", "W", "N"]:
            pose_next = move(pose, d)
            if l[pose_next[0]][pose_next[-1]] != "#":
                if grid[pose_next[0]][pose_next[-1]][d] > grid[pose[0]][pose[-1]][d] + c_move:
                    q.put((pose_next, d))
                    grid[pose_next[0]][pose_next[-1]][d] = grid[pose[0]][pose[-1]][d] + c_move
                    path[pose_next[0]][pose_next[-1]][d] = set(path[pose[0]][pose[-1]][d] | {pose_next})
                elif grid[pose_next[0]][pose_next[-1]][d] == grid[pose[0]][pose[-1]][d] + c_move:
                    if any(u not in path[pose_next[0]][pose_next[-1]][d] for u in path[pose[0]][pose[-1]][d]):
                        q.put((pose_next, d))
                        path[pose_next[0]][pose_next[-1]][d] = set(path[pose[0]][pose[-1]][d] | path[pose_next[0]][pose_next[-1]][d] | {pose_next})
    # print(grid[pose_e[0]][pose_e[-1]])
    e_min = min(grid[pose_e[0]][pose_e[-1]].values())
    e_dir = [k for k, v in grid[pose_e[0]][pose_e[-1]].items() if v == e_min]
    e_path = set(u for d in e_dir for u in path[pose_e[0]][pose_e[-1]][d])
    return len(e_path) + 1  # don't know which one is missing


p21 = count2(l=example.split("\n"))
p22 = count2(l=example2.split("\n"))
print("count2", p21, p22)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
