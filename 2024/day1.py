import re
from utils.printing import display

example = """3   4
4   3
2   5
1   3
3   9
3   3"""


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [(line.split(" ")[0], line.split(" ")[-1]) for line in l]

def get_count(p_internal):
    l1 = [int(item[0]) for item in p_internal]
    l2 = [int(item[-1]) for item in p_internal]
    count = 0
    for i1, i2 in zip(sorted(l1), sorted(l2)):
        count += abs(i1 - i2)
    print(count)


p = parsed(l=example.split("\n"))
print(p)
get_count(p_internal=p)
get_count(p_internal=parsed(l=s))


def get_count2(p_internal):
    l1 = [int(item[0]) for item in p_internal]
    l2 = [int(item[-1]) for item in p_internal]

    c = dict()
    for i in l2:
        if i in c:
            c[i] += 1
        else:
            c[i] = 1

    count = 0
    for i1 in l1:
        if i1 in c:
            count += i1 * c[i1]
    print(count)


get_count2(p_internal=p)
get_count2(p_internal=parsed(l=s))
