from utils.printing import display


examples = [
    "R2, L3",
    "R2, R2, R2",
    "R5, L5, R5, R3",
]


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l.split(",")]


l_dirs = {
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (0, -1): (1, 0),
    (-1, 0): (0, -1),
}
r_dirs = {
    (1, 0): (0, -1),
    (0, 1): (1, 0),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1),
}


def get_count(p_internal):
    x, y = 0, 0
    dx, dy = 1, 0
    for c in p_internal:
        v = int(c[1:])
        if c[0] == "L":
            dx, dy = l_dirs[(dx, dy)]
        if c[0] == "R":
            dx, dy = r_dirs[(dx, dy)]
        x += dx * v
        y += dy * v
    count = abs(x) + abs(y)
    print(x, y, '\t', count)


get_count(p_internal=parsed(l=s[0]))
print()

for example in examples:
    print(example, end="\t")
    get_count(p_internal=[ll.strip() for ll in example.split(",")])
print()


examples2 = [
    "R8, R4, R4, R8",
]


def get_count2(p_internal):
    x, y = 0, 0
    dx, dy = 1, 0
    seen = set()
    for c in p_internal:
        v = int(c[1:])
        if c[0] == "L":
            dx, dy = l_dirs[(dx, dy)]
        if c[0] == "R":
            dx, dy = r_dirs[(dx, dy)]
        alive = True
        for i in range(v):
            x += dx
            y += dy
            if (x, y) in seen:
                # print(x, y)
                alive = False
                break
            seen.add((x, y))
        if not alive:
            break
    count = abs(x) + abs(y)
    print(x, y, '\t', count)


get_count2(p_internal=parsed(l=s[0]))
print()

for example in examples2:
    print(example, end="\t")
    get_count2(p_internal=[ll.strip() for ll in example.split(",")])
print()
