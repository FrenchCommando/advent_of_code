from itertools import batched

from utils.printing import display

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


with open("day5.txt", "r") as f:
    s = f.readlines()
    display(s)


def parse(text):
    it = iter(text)
    seeds = list(map(int, filter(None, next(it).split(":")[-1].split(" "))))
    display(x=seeds)
    next(it)
    next(it)

    maps = []
    try:
        while True:
            one_map = []
            while t := next(it).strip():
                table = t.split(" ")
                one_map.append(dict(
                    destination=int(table[0]),
                    source=int(table[1]),
                    range=int(table[2]),
                ))
            maps.append(one_map)
            next(it)
    except StopIteration:
        maps.append(one_map)
    return seeds, maps


def solve(l_seeds, one_map):
    for i, seed in enumerate(l_seeds):
        for one_conversion in one_map:
            if (one_conversion['source'] <= seed
                    < one_conversion['source'] + one_conversion['range']):
                l_seeds[i] += one_conversion['destination'] - one_conversion['source']
                break
    return l_seeds


seeds, maps = parse(text=example.split("\n"))
# seeds, maps = parse(text=s)

display(x=seeds)
display(x=maps)

for single_map in maps:
    seeds = solve(l_seeds=seeds, one_map=single_map)
    display(x=seeds)

display(x=min(seeds))

# part 2
print("Part2")

seeds, maps = parse(text=example.split("\n"))
# seeds, maps = parse(text=s)


def solve_d(d_seeds, one_map):
    d_final = dict()
    for one_conversion in one_map:
        source = one_conversion['source']
        diff = one_conversion['destination'] - one_conversion['source']
        last = one_conversion['source'] + one_conversion['range']

        # split source and last
        def split(item):
            item_value = 0
            for start, size in d_seeds.copy().items():
                offset = item - start
                if offset > 0:
                    remainder = size - offset
                    if remainder > 0:
                        d_seeds[start] = offset
                        item_value = max(item_value, remainder)
            if item_value > 0:
                d_seeds[item] = item_value
        split(item=source)
        split(item=last)
        for l_start, l_size in d_seeds.copy().items():
            if source <= l_start < last:
                destination = l_start + diff
                d_final[destination] = max(d_final.get(destination, 0), l_size)
                del d_seeds[l_start]
    d_seeds.update(d_final)
    return d_seeds


print()
d = {s_start: s_range for s_start, s_range in batched(seeds, 2)}
for single_map in maps:
    d = solve_d(d_seeds=d, one_map=single_map)
    print("Solved one map")
    display(x=min(list(d.keys())))
display(x=d)
m_seeds = list(d.keys())

display(x=m_seeds)
display(x=min(m_seeds))
