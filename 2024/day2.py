import re
from utils.printing import display

example = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


with open("day2.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [list(map(int, line.split(" "))) for line in l]

def get_count(p_internal):
    def is_valid2(line):
        if not is_one(line):
            return False
        if not is_three(line):
            return False
        return True
    def is_valid1(line):
        if is_increasing(line):
            return True
        if is_decreasing(line):
            return True
        return False
    def is_one(line):
        one = True
        for i, j in zip(line, line[1:]):
            if abs(i - j) < 1:
                one = False
                break
        return one
    def is_three(line):
        three = True
        for i, j in zip(line, line[1:]):
            if abs(i - j) > 3:
                three = False
                break
        return three

    def is_increasing(line):
        increasing = True
        for i, j in zip(line, line[1:]):
            if i > j:
                increasing = False
                break
        return increasing

    def is_decreasing(line):
        decreasing = True
        for i, j in zip(line, line[1:]):
            if i < j:
                decreasing = False
                break
        return decreasing

    count = 0
    for line in p_internal:
        if is_valid1(line=line):
            if is_valid2(line=line):
                count += 1
    print(count)


p = parsed(l=example.split("\n"))
print(p)
get_count(p_internal=p)
get_count(p_internal=parsed(l=s))


def get_count2(p_internal):
    def is_valid2(line):
        if not is_one(line):
            return False
        if not is_three(line):
            return False
        return True
    def is_valid1(line):
        if is_increasing(line):
            return True
        if is_decreasing(line):
            return True
        return False
    def is_one(line):
        one = True
        for i, j in zip(line, line[1:]):
            if abs(i - j) < 1:
                one = False
                break
        return one
    def is_three(line):
        three = True
        for i, j in zip(line, line[1:]):
            if abs(i - j) > 3:
                three = False
                break
        return three

    def is_increasing(line):
        increasing = True
        for i, j in zip(line, line[1:]):
            if i > j:
                increasing = False
                break
        return increasing

    def is_decreasing(line):
        decreasing = True
        for i, j in zip(line, line[1:]):
            if i < j:
                decreasing = False
                break
        return decreasing

    count = 0
    for line in p_internal:
        for i in range(len(line)):
            sub_line = line[:i] + line[i + 1:]
            if is_valid1(line=sub_line):
                if is_valid2(line=sub_line):
                    count += 1
                    break
    print(count)


get_count2(p_internal=p)
get_count2(p_internal=parsed(l=s))
