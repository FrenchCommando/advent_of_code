from utils.printing import display


examples = [
    ">",
    "^v",
    "^>v<",
    "^v^v^v^v^v",
]


with open("day3.txt", "r") as f:
    s = f.readlines()
    display(s)


d_direction = {
    "^": (0, 1),
    "v": (0, -1),
    ">": (1, 0),
    "<": (-1, 0),
}


def get_count(p_internal):
    d = set()
    x, y = 0, 0
    d.add((x, y))
    for c in p_internal:
        dx, dy = d_direction[c]
        x += dx
        y += dy
        d.add((x, y))
    print(len(d))


get_count(p_internal=s[0].strip())
print()

for example in examples:
    print(example, end="\t")
    get_count(p_internal=example)
print()


def get_count2(p_internal):
    d = set()
    x, y = 0, 0
    x2, y2 = 0, 0
    d.add((x, y))
    is_robot = False
    for c in p_internal:
        dx, dy = d_direction[c]
        if is_robot:
            x2 += dx
            y2 += dy
            d.add((x2, y2))
        else:
            x += dx
            y += dy
            d.add((x, y))
        is_robot = not is_robot
    print(len(d))


get_count2(p_internal=s[0].strip())
print()

for example in examples:
    print(example, end="\t")
    get_count2(p_internal=example)
print()