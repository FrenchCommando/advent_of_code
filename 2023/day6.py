import math
from functools import reduce
from operator import mul
import re
from utils.printing import display

example = """Time:      7  15   30
Distance:  9  40  200"""


with open("day6.txt", "r") as f:
    s = f.readlines()
    display(s)


def parse(text):
    internal_times = list(map(int, re.split(pattern=r"\D+", string=text[0].split(":", maxsplit=1)[-1].strip())))
    internal_distances = list(map(int, re.split(pattern=r"\D+", string=text[-1].split(":", maxsplit=1)[-1].strip())))
    return internal_times, internal_distances


def parse2(text):
    internal_times = int(''.join(re.split(pattern=r"\D+", string=text[0].split(":", maxsplit=1)[-1].strip())))
    internal_distances = int(''.join(re.split(pattern=r"\D+", string=text[-1].split(":", maxsplit=1)[-1].strip())))
    return internal_times, internal_distances


def solve(l_time, l_distance):
    # number of ways to beat l_distance in l_time
    # l_time = time_button + time_travel
    # l_distance = time_travel * speed
    # speed = time_button
    # solve: l_distance = time_travel * time_button and l_time = time_button + time_travel
    # 0 = x2 - x * (a + b) + a * b
    disc = (l_time / 2) ** 2 - l_distance
    delta = math.sqrt(disc)
    left = math.floor(((l_time / 2) - delta))
    right = math.ceil(((l_time / 2) + delta))
    return right - left - 1


times, distances = parse(text=example.split("\n"))
# times, distances = parse(text=s)

display(x=times)
display(x=distances)

ways = []
for time, distance in zip(times, distances):
    way = solve(l_time=time, l_distance=distance)
    ways.append(way)

display(x=ways)
display(x=reduce(mul, ways))

print()
time, distance = parse2(text=example.split("\n"))
# time, distance = parse2(text=s)

display(x=time)
display(x=distance)

way = solve(l_time=time, l_distance=distance)
display(x=way)
