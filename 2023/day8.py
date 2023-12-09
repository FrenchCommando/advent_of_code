import itertools
import math
import re
from utils.printing import display

example = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""


example2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


example3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


with open("day8.txt", "r") as f:
    s = f.readlines()
    display(s)


def parse(text):
    lr = text[0].strip()

    maps = {}

    for line in text[2:]:
        d = re.fullmatch(
            pattern=r"(?P<node>[A-Z0-9]+) = \((?P<left>[A-Z0-9]+), (?P<right>[A-Z0-9]+)\)",
            string=line.strip(),
        ).groupdict()
        maps[d['node']] = dict(L=d['left'], R=d['right'])

    return lr, maps


l_lr, l_maps = parse(text=example.split("\n"))
# l_lr, l_maps = parse(text=example2.split("\n"))
# l_lr, l_maps = parse(text=s)
display(x=l_lr)
display(x=l_maps)


def solve1(lr, maps):
    start = "AAA"
    end = "ZZZ"

    current = start
    i = 0
    it = itertools.cycle(lr)
    while current != end:
        direction = next(it)
        current = maps[current][direction]
        i += 1
        # print(i, l_current)

    return i


display(x=solve1(lr=l_lr, maps=l_maps))


# part2
l_lr, l_maps = parse(text=example3.split("\n"))
# l_lr, l_maps = parse(text=s)


def solve2(lr, maps):
    starts = list(filter(lambda x: x[-1] == 'A', maps.keys()))
    currents = starts

    i2 = 0
    it = itertools.cycle(lr)
    while not all(map(lambda x: x[-1] == "Z", currents)):
        direction = next(it)
        currents = list(map(lambda current: maps[current][direction], currents))
        i2 += 1
        if i2 % 1000000 == 0:
            print(i2, currents)
    return i2


def solve2short(lr, maps):
    starts = list(filter(lambda x: x[-1] == 'A', maps.keys()))
    currents = starts
    periods = [0 for x in starts]
    indices = [0 for x in starts]
    remainder = [0 for x in starts]

    def finished(x):
        return x[-1] == "Z"

    i2 = 0
    it = itertools.cycle(lr)
    while not all(map(finished, currents)):
        direction = next(it)
        currents = list(map(lambda i_current: maps[i_current][direction], currents))
        i2 += 1
        if any(map(finished, currents)):
            for c, current in enumerate(currents):
                if finished(x=current):
                    periods[c] = i2 - indices[c]
                    indices[c] = i2
                    remainder[c] = indices[c] % periods[c]
            print(i2, currents, periods, remainder)
        if all(map(lambda x: x > 0, periods)):
            # remainders are zero
            return math.lcm(*periods)


# display(x=solve2(lr=l_lr, maps=l_maps))
display(x=solve2short(lr=l_lr, maps=l_maps))
