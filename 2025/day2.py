from utils.printing import display

example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""


with open("day2.txt", "r") as f:
    s = f.readlines()[0]
    display(s)


def parsed(l):
    return [tuple(map(int, ll.split("-"))) for ll in l.split(",")]


def iter_invalid(start=1):
    value = start
    while True:
        yield int(f"{value}{value}")
        value += 1


def get_invalid_list(left, right):
    l_invalids = []
    for invalid in iter_invalid(start=1):
        if invalid > right:
            break
        if invalid < left:
            continue
        l_invalids.append(invalid)
    return l_invalids


def get_count(p_internal):
    count = 0
    for left, right in p_internal:
        l_invalid = get_invalid_list(left=left, right=right)
        print(left, right, l_invalid)
        count += sum(l_invalid)
    print(count)


p = parsed(l=''.join(example.split("\n")))
print(p)
print()
get_count(p_internal=p)
print()
get_count(p_internal=parsed(l=s))
print()


def iter_invalid2(start=1, n=2):
    value = start
    while True:
        yield int(n * f"{value}")
        value += 1


def get_invalid_list2(left, right):
    l_invalids = []
    for n in range(2, len(f"{right}") + 1):
        for invalid in iter_invalid2(start=1, n=n):
            if invalid > right:
                break
            if invalid < left:
                continue
            l_invalids.append(invalid)
    return l_invalids


def get_count2(p_internal):
    full_list = []
    for left, right in p_internal:
        l_invalid = get_invalid_list2(left=left, right=right)
        print(left, right, l_invalid)
        full_list.extend(l_invalid)
    s_full = set(full_list)
    count = sum(s_full)
    print(count)


get_count2(p_internal=p)
print()
get_count2(p_internal=parsed(l=s))
print()
