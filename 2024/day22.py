import re
from utils.printing import display

example = """1
10
100
2024"""



with open("day22.txt", "r") as f:
    s = f.readlines()
    display(s)


def generate(number, skip):
    for turn in range(skip):
        v = number * 64
        number = number ^ v
        number = number % 16777216
        v = number // 32
        number = number ^ v
        number = number % 16777216
        v = number * 2048
        number = number ^ v
        number = number % 16777216
    return number

def count(l):
    c = []
    for line in l:
        number = int(line)
        generated = generate(number=number, skip=2000)
        c.append(generated)
    print(c)
    return sum(c)


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
