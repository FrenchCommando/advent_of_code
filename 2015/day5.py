from utils.printing import display


examples = [
    "ugknbfddgicrmopn",
    "aaa",
    "jchzalrnumimnmhp",
    "haegwjzuvuyypxyu",
    "dvszwmarrgswjxmb",
]


with open("day5.txt", "r") as f:
    s = f.readlines()
    display(s)


def is_nice(p):
    if any(u in p for u in ["ab", "cd", "pq", "xy"]):
        return False
    if sum(p.count(u) for u in "aeiou") <= 2:
        return False
    for a, b in zip(p, p[1:]):
        if a == b:
            return True
    return False


def get_count(p_internal):
    count = 0
    for p in p_internal:
        n = is_nice(p=p)
        # print(n, p)
        if n:
            count += 1
    print(count)


get_count(p_internal=[sss.strip() for sss in s])
print()
get_count(p_internal=examples)
print()


examples2 = [
    "qjhvhtzxzqqjkmpb",
    "xxyxx",
    "uurcxstgmygtbstg",
    "ieodomkazucvgmuy",
]


def is_nice2(p):
    n2 = is_nice22(p=p)
    if not n2:
        return False
    n1 = is_nice21(p=p)
    return n1


def is_nice21(p):
    if len(p) <= 3:
        return False
    if p[:2] in p[2:]:
        return True
    return is_nice21(p=p[1:])


def is_nice22(p):
    for a, b in zip(p, p[2:]):
        if a == b:
            return True
    return False


def get_count2(p_internal):
    count = 0
    for p in p_internal:
        n = is_nice2(p=p)
        # print(n, p)
        if n:
            count += 1
    print(count)


get_count2(p_internal=[sss.strip() for sss in s])
print()
get_count2(p_internal=examples2)
print()
