from utils.printing import display

example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


with open("day7.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    count = 0
    s_init = p_internal[0].index("S")
    positions = {s_init}
    for line in p_internal[1:]:
        if "^" in line:
            for i, c in enumerate(line):
                if c == "^":
                    if i in positions:
                        count += 1
                        positions.remove(i)
                        positions.add(i - 1)
                        positions.add(i + 1)
    print(positions, len(positions))
    print(count)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()


def get_count2(p_internal):
    s_init = p_internal[0].index("S")
    positions = {s_init: 1}
    for line in p_internal[1:]:
        if "^" in line:
            for i, c in enumerate(line):
                if c == "^":
                    if i in positions:
                        t = positions[i]
                        del positions[i]
                        if i + 1 not in positions:
                            positions[i + 1] = 0
                        if i - 1 not in positions:
                            positions[i - 1] = 0
                        positions[i - 1] += t
                        positions[i + 1] += t
    print(positions, len(positions))
    print(sum(positions.values()))


get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p)
print()
