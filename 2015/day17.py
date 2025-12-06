import itertools

from utils.printing import display


examples = """20
15
10
5
5"""


with open("day17.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p, n):
    count = 0
    for k in range(1, len(p) + 1):
        for i in itertools.combinations(p, k):
            if sum(i) == n:
                count += 1
    print(count)


get_count(p=[int(sss.strip()) for sss in s], n=150)
get_count(p=[int(sss.strip()) for sss in examples.split("\n")], n=25)
print()


def get_count2(p, n):
    count = 0
    for k in range(1, len(p) + 1):
        for i in itertools.combinations(p, k):
            if sum(i) == n:
                count += 1
        if count != 0:
            break
    print(count)


get_count2(p=[int(sss.strip()) for sss in s], n=150)
get_count2(p=[int(sss.strip()) for sss in examples.split("\n")], n=25)
print()
