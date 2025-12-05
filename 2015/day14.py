import itertools
import json
import re

from utils.printing import display


examples = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""


with open("day14.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p_internal, n):
    data = dict()
    for p in p_internal:
        name, p1 = p.split(" can fly ")
        speed, p2 = p1.split(" km/s for ")
        duration, p3 = p2.split(" seconds, but then must rest for ")
        rest, stuff = p3.split(" ")
        data[name] = tuple(map(int, (speed, duration, rest)))

    print(data)

    def evaluate(stats):
        speed, duration, rest = stats
        cycle = duration + rest
        a, b = divmod(n, cycle)
        d = (a * duration + min(b, duration)) * speed
        print(d, cycle, a, b, stats)
        return d

    # largest = max((name for name in data), key=lambda x: evaluate(data[x]))
    largest = max(evaluate(u) for u in data.values())
    print(largest)


get_count(p_internal=[sss.strip() for sss in s], n=2503)
print()
get_count(p_internal=[sss.strip() for sss in examples.split("\n")], n=1000)
print()


def get_count2(p_internal, n):
    data = dict()
    for p in p_internal:
        name, p1 = p.split(" can fly ")
        speed, p2 = p1.split(" km/s for ")
        duration, p3 = p2.split(" seconds, but then must rest for ")
        rest, stuff = p3.split(" ")
        data[name] = tuple(map(int, (speed, duration, rest)))

    print(data)

    positions = {name: [0 for _ in range(n)] for name in data.keys()}

    for name, stats in data.items():
        speed, duration, rest = stats
        pos = 0
        i = 0
        r_running = duration
        r_rest = rest
        while i < n:
            if r_running > 0:
                pos += speed
                r_running -= 1
            elif r_rest > 1:
                r_rest -= 1
            else:
                r_running = duration
                r_rest = rest
            positions[name][i] = pos
            i += 1

    # print(positions)

    points = {name: 0 for name in data.keys()}
    for name, position in positions.items():
        for i in range(n):
            v = position[i]
            if max(positions[name_i][i] for name_i in data.keys()) == v:
                points[name] += 1

    print(points)

    largest = max(u for u in points.values())
    print(largest)


get_count2(p_internal=[sss.strip() for sss in s], n=2503)
print()
get_count2(p_internal=[sss.strip() for sss in examples.split("\n")], n=1000)
print()

