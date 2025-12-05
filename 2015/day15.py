import itertools
import json
import re
from functools import reduce

from utils.printing import display


examples = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""


with open("day15.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p_internal, n):
    data = dict()
    for p in p_internal:
        name, p1 = p.split(": ")
        specs = p1.split(", ")
        props = map(lambda x: int(x.split(" ")[-1]), specs)
        data[name] = tuple(props)

    print(data)

    def evaluate(distribution):
        counts = [0 for _ in range(4)]
        for p, specs in zip(distribution, data.values()):
            for i in range(4):
                counts[i] += p * specs[i]
        if any(u <= 0 for u in counts):
            return 0
        return reduce(lambda x, y: x * y, counts)

    def iter_distribution():
        l_names = len(p_internal)
        for q in itertools.product(range(n), repeat=l_names):
            if sum(q) == n:
                yield tuple(q)

    largest = max(evaluate(distribution) for distribution in iter_distribution())
    print(largest)


get_count(p_internal=[sss.strip() for sss in s], n=100)
print()
get_count(p_internal=[sss.strip() for sss in examples.split("\n")], n=100)
print()


def get_count2(p_internal, n, c):
    data = dict()
    for p in p_internal:
        name, p1 = p.split(": ")
        specs = p1.split(", ")
        props = map(lambda x: int(x.split(" ")[-1]), specs)
        data[name] = tuple(props)

    print(data)

    def evaluate(distribution):
        counts = [0 for _ in range(5)]
        for p, specs in zip(distribution, data.values()):
            for i in range(5):
                counts[i] += p * specs[i]
        if any(u <= 0 for u in counts[:-1]):
            return 0
        if counts[-1] != c:
            return 0
        return reduce(lambda x, y: x * y, counts[:-1])

    def iter_distribution():
        l_names = len(p_internal)
        for q in itertools.product(range(n), repeat=l_names):
            if sum(q) == n:
                yield tuple(q)

    largest = max(evaluate(distribution) for distribution in iter_distribution())
    print(largest)


get_count2(p_internal=[sss.strip() for sss in s], n=100, c=500)
print()
get_count2(p_internal=[sss.strip() for sss in examples.split("\n")], n=100, c=500)
print()

