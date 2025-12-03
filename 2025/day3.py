from utils.printing import display

example = """987654321111111
811111111111119
234234234234278
818181911112111"""


with open("day3.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_best_joltage(batteries):
    d_max = max(batteries)
    i_max = batteries.index(d_max)
    if i_max == len(batteries) - 1:
        dd_max = max(batteries[:-1])
        return f"{dd_max}{d_max}"
    dd_max = max(batteries[i_max + 1:])
    return f"{d_max}{dd_max}"


def get_count(p_internal):
    joltages = []
    for batteries in p_internal:
        best_joltage = get_best_joltage(batteries=batteries)
        joltages.append(best_joltage)
        print(batteries, best_joltage)
    count = sum(map(int, joltages))
    print(count)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=p)
print()
get_count(p_internal=parsed(l=s))
print()


def get_best_joltage2(batteries, n):
    d_max = max(batteries)
    if n == 1:
        return f"{d_max}"
    i_max = batteries.index(d_max)
    # print(f"zero {i_max} {d_max} {len(batteries)}")
    while i_max > len(batteries) - n:
        d_max = max(batteries[:i_max])
        i_max = batteries.index(d_max)
        # print(f"not zero {i_max} {d_max} {len(batteries)}")
    bb = get_best_joltage2(batteries[i_max + 1:], n - 1)
    return f"{d_max}{bb}"


def get_count2(p_internal):
    joltages = []
    for batteries in p_internal:
        best_joltage = get_best_joltage2(batteries=batteries, n=12)
        joltages.append(best_joltage)
        print(batteries, best_joltage)
    count = sum(map(int, joltages))
    print(count)


get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p)
print()
