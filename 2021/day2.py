from utils.printing import display

example = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


with open("day2.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_move(stuff):
    direction, value = stuff.split(" ")
    if direction == "forward":
        return int(value), 0
    elif direction == "up":
        return 0, - int(value)
    elif direction == "down":
        return 0, + int(value)
    return None


def get_count(p_internal):
    x, y = 0, 0
    for stuff in p_internal:
        dx, dy = get_move(stuff=stuff)
        x += dx
        y += dy
        # print(stuff, dx, dy)
    print(x, y, x * y)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()


def get_move2(stuff):
    direction, value = stuff.split(" ")
    if direction == "forward":
        return int(value), 0, 0, int(value)
    elif direction == "up":
        return 0, 0, - int(value), 0
    elif direction == "down":
        return 0, 0, int(value), 0
    return None


def get_count2(p_internal):
    x, y = 0, 0
    a = 0
    for stuff in p_internal:
        dx, dy, da, my = get_move2(stuff=stuff)
        x += dx
        y += dy
        a += da
        y += my * a
        # print(x, y, a, stuff, dx, dy, da, my)
    print(x, y, x * y)


get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p)
print()
