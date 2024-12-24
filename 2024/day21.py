import re
from utils.printing import display

example = """029A
980A
179A
456A
379A"""



with open("day21.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    return 1


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    return 1


p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
