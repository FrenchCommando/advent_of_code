import re
from utils.printing import display

example = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""



with open("day25.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    i = iter(l)
    locks = []
    keys = []
    try:
        while True:
            top = next(i)
            is_lock = all(u[0] == "#" for u in top)
            c = "#" if is_lock else "."
            item = [0 for k in range(5)]
            while True:
                line = next(i)
                if not line:
                    break
                for k in range(5):
                    if line[k] == c:
                        item[k] += 1
            if is_lock:
                locks.append(item)
            else:
                keys.append(item)
    except StopIteration:
        if is_lock:
            locks.append(item)
        else:
            keys.append(item)
    print("Locks", locks)
    print("Keys", keys)

    couple = 0
    for lock in locks:
        for key in keys:
            if all(lock[k] <= key[k] for k in range(5)):
                couple += 1
    return couple


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)
