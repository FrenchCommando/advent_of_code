import re
from utils.printing import display

example = """AAAA
BBCD
BBCC
EEEC"""
example2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
example3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""



with open("day12.txt", "r") as f:
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
