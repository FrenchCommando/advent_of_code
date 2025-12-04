from utils.printing import display


example = """1721
979
366
299
675
1456"""


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    seen = set()
    for v in p_internal:
        i = int(v)
        if 2020 - i in seen:
            print(i, 2020 - i, i * (2020 - i))
        else:
            seen.add(i)


get_count(p_internal=parsed(l=s))
print()

get_count(p_internal=[u.strip() for u in example.splitlines()])
print()


def get_count2(p_internal):
    seen = set()
    d = dict()
    for v in p_internal:
        i = int(v)
        if i in d:
            a, b = d[i]
            print(i, a, b, i * a * b)
        else:
            for k in seen:
                c = 2020 - i - k
                if c not in d:
                    d[c] = i, k
            seen.add(i)


get_count2(p_internal=parsed(l=s))
print()

get_count2(p_internal=[u.strip() for u in example.splitlines()])
print()
