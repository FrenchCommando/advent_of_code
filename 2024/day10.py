import re
from utils.printing import display

example = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"""

example2 = """..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""

example3 = """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01"""

example4 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""



with open("day10.txt", "r") as f:
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
