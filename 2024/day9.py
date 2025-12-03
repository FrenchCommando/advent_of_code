import re
from utils.printing import display

example = """2333133121414131402"""



with open("day9.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    sequence = l[0]
    n = len(sequence)
    print("length", n)
    c = sum(int(sequence[i]) for i in range(n) if i % 2 == 0)
    print("files", c)
    space = [-1 for i in range(c)]
    index_empty = 0
    file = True
    forward = True
    for i, v in enumerate(sequence):
        for a in range(int(v)):
            if forward:
                if file:
                    space[index_empty] = i // 2
                index_empty += 1
                if index_empty == c:
                    forward = False
                    index_empty -= 1
                    while space[index_empty] != -1:
                        index_empty -= 1
            elif file:
                space[index_empty] = i // 2
                while index_empty >= 0 and space[index_empty] != -1:
                    index_empty -= 1
            else:
                while index_empty >= 0 and space[index_empty] != -1:
                    index_empty -= 1

        file = not file

    return sum(i * v for i, v in enumerate(space))


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    sequence = l[0]
    n = len(sequence)
    print("length", n)

    full = dict()
    empty = dict()
    index_empty = 0
    for i, v in enumerate(sequence):
        if i % 2 == 0:
            full[index_empty] = (i // 2, int(v))
        else:
            empty[index_empty] = int(v)
        index_empty += int(v)

    # print("Full", full)
    # print("Empty", empty)

    order = list(full.keys())[::-1]
    print("Order", order)
    for item in order:
        v1, v2 = full[item]
        for index in sorted(empty):
            if index >= item:
                continue
            width = empty[index]
            if width >= v2:
                full[index] = (v1, v2)
                if width != v2:
                    empty[index + v2] = width - v2
                del empty[index]
                del full[item]
                break

    # print("PostFull", full)
    # print("PostEmpty", empty)

    last_space = max(index + val[-1] for index, val in full.items())
    space = [0 for i in range(last_space)]
    for index, val in full.items():
        for x in range(val[-1]):
            space[index + x] = val[0]
    # print("Space", space)
    return sum(i * v for i, v in enumerate(space))


p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
