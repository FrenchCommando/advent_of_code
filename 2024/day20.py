import queue
import re
from utils.printing import display

example = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""



with open("day20.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l, gain_threshold):
    n = len(l)
    m = len(l[0])
    print(n, m)

    ll = "".join(l)
    l_s = ll.index("S")
    l_e = ll.index("E")
    pos_s = l_s // m, l_s % m
    pos_e = l_e // m, l_e % m
    print("Start", pos_s)
    print("End", pos_e)

    n_big_number = 1e50
    c = [[n_big_number for j in range(m)] for i in range(n)]
    q = queue.Queue()
    c[pos_s[0]][pos_s[-1]] = 0
    q.put(pos_s)
    path = [pos_s]
    while not q.empty():
        pos = q.get()
        for pos_next in [(pos[0], pos[-1] - 1),(pos[0], pos[-1] + 1),(pos[0] - 1, pos[-1]),(pos[0] + 1, pos[-1])]:
            if l[pos_next[0]][pos_next[-1]] == "#":
                continue
            if c[pos_next[0]][pos_next[-1]] > c[pos[0]][pos[-1]] + 1:
                c[pos_next[0]][pos_next[-1]] = c[pos[0]][pos[-1]] + 1
                path.append(pos_next)
                q.put(pos_next)
    print(len(path), path)

    n_cheats = 0
    for i_from, pos_from in enumerate(path):
        for i_to, pos_to in enumerate(path):
            if i_from >= i_to:
                continue
            if (abs(pos_from[0] - pos_to[0]), abs(pos_from[-1] - pos_to[-1])) in [(0, 2), (2, 0)]:
                d_i = i_to - i_from
                gain = d_i - 2
                if gain >= gain_threshold:
                    n_cheats += 1

    print()
    return n_cheats


p = count(l=example.split("\n"), gain_threshold=64)
p15 = count(l=example.split("\n"), gain_threshold=15)
print("count", p, p15)
# ps = count(l=[line.strip() for line in s], gain_threshold=100)
# print("count", ps)



def count2(l, gain_threshold):
    n = len(l)
    m = len(l[0])
    print(n, m)

    ll = "".join(l)
    l_s = ll.index("S")
    l_e = ll.index("E")
    pos_s = l_s // m, l_s % m
    pos_e = l_e // m, l_e % m
    print("Start", pos_s)
    print("End", pos_e)

    n_big_number = 1e50
    c = [[n_big_number for j in range(m)] for i in range(n)]
    q = queue.Queue()
    c[pos_s[0]][pos_s[-1]] = 0
    q.put(pos_s)
    path = [pos_s]
    while not q.empty():
        pos = q.get()
        for pos_next in [(pos[0], pos[-1] - 1),(pos[0], pos[-1] + 1),(pos[0] - 1, pos[-1]),(pos[0] + 1, pos[-1])]:
            if l[pos_next[0]][pos_next[-1]] == "#":
                continue
            if c[pos_next[0]][pos_next[-1]] > c[pos[0]][pos[-1]] + 1:
                c[pos_next[0]][pos_next[-1]] = c[pos[0]][pos[-1]] + 1
                path.append(pos_next)
                q.put(pos_next)
    print(len(path), path)

    n_cheats = 0
    for i_from, pos_from in enumerate(path):
        for i_to, pos_to in enumerate(path):
            if i_from >= i_to:
                continue
            distance = (abs(pos_from[0] - pos_to[0]) + abs(pos_from[-1] - pos_to[-1]))
            if distance <= 20:
                d_i = i_to - i_from
                gain = d_i - distance
                if gain >= gain_threshold:
                    n_cheats += 1

    print()
    return n_cheats


p276 = count2(l=example.split("\n"), gain_threshold=76)
p274 = count2(l=example.split("\n"), gain_threshold=74)
p272 = count2(l=example.split("\n"), gain_threshold=72)
p270 = count2(l=example.split("\n"), gain_threshold=70)
p260 = count2(l=example.split("\n"), gain_threshold=60)
print("count2", p276, p274, p272, p270, p260)
ps2 = count2(l=[line.strip() for line in s], gain_threshold=100)
print("count2", ps2)
