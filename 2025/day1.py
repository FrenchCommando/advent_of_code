from utils.printing import display

example = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [line.strip() for line in l]

def get_count(p_internal):
    direction = [item[0] for item in p_internal]
    number = [int(item[1:]) for item in p_internal]
    count = 0
    value = 50
    for d, n in zip(direction, number):
        if d == "L":
            value -= n
        else:
            value += n
        value %= 100
        if value == 0:
            count += 1
    print(count)


p = parsed(l=example.split("\n"))
print(p)
get_count(p_internal=p)
get_count(p_internal=parsed(l=s))


def get_count2(p_internal):
    direction = [item[0] for item in p_internal]
    number = [int(item[1:]) for item in p_internal]
    count = 0
    value = 50
    for d, n in zip(direction, number):
        if d == "L":
            if value == 0:
                value = 100
            value -= n
            count -= value // 100
            value -= 100 * (value // 100)
            if value == 0:
                count += 1
        else:
            value += n
            count += value // 100
            value -= 100 * (value // 100)
        # print(f"{count}|{value}", end='\t')
    print(count)


get_count2(p_internal=p)
get_count2(p_internal=parsed(l=s))
