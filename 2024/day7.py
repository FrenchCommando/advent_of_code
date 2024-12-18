import re
from queue import Queue

from utils.printing import display

example = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""



with open("day7.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    c = []
    for line in l:
        # print(line)
        line_s, line_n = line.split(": ")
        nums = list(map(int, line_n.split(" ")))
        v = int(line_s)
        if solve(v, nums):
            # print(v, nums)
            c.append(v)
    print(c)
    return sum(c)


def solve(v, nums):
    q = Queue()
    q.put((v, nums))
    while not q.empty():
        val, n = q.get()
        if len(n) == 1:
            if val == n[0]:
                return True
        else:
            nn = n[:-1]
            last = n[-1]
            if val > last:
                q.put((val - last, nn))
            if val % last == 0:
                q.put((val // last, nn))
    return False


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    c = []
    for line in l:
        # print(line)
        line_s, line_n = line.split(": ")
        nums = list(map(int, line_n.split(" ")))
        v = int(line_s)
        if solve2(v, nums):
            # print(v, nums)
            c.append(v)
    print(c)
    return sum(c)


def solve2(v, nums):
    q = Queue()
    q.put((v, nums))
    while not q.empty():
        val, n = q.get()
        if len(n) == 1:
            if val == n[0]:
                return True
        else:
            nn = n[:-1]
            last = n[-1]
            if val > last:
                q.put((val - last, nn))
            if val % last == 0:
                q.put((val // last, nn))
            if str(val).endswith(str(last)) and len(str(val)) > len(str(last)):
                # print(val, last, nn)
                q.put((int(str(val)[:-len(str(last))]), nn))
    return False


p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
