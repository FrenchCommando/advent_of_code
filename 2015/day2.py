from utils.printing import display


examples = [
    "2x3x4",
    "1x1x10",
]


with open("day2.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    count = 0
    for line in p_internal:
        l, w, h = map(int, line.split("x"))
        sides = l * w, l * h, h * w
        surface = 2 * sum(sides)
        smallest = min(sides)
        dimension = surface + smallest
        # print(dimension, line)
        count += dimension
    print(count)


get_count(p_internal=parsed(l=s))
print()

get_count(p_internal=examples)
print()


def get_count2(p_internal):
    count = 0
    for line in p_internal:
        l, w, h = map(int, line.split("x"))
        sides = l + w, l + h, h + w
        perimeter = 2 * min(sides)
        volume = l * h * w
        dimension = perimeter + volume
        # print(perimeter, volume, dimension, line)
        count += dimension
    print(count)


get_count2(p_internal=parsed(l=s))
print()

get_count2(p_internal=examples)
print()
