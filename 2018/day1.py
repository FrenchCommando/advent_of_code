from utils.printing import display


examples = [
    "+1, -2, +3, +1",  # 3
    "+1, +1, +1",  # 3
    "+1, +1, -2",  # 0
    "-1, -2, -3",  # -6
]


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    value = 0
    for v in p_internal:
        value += int(v)
    print(value)


get_count(p_internal=parsed(l=s))
print()

for example in examples:
    print(example, end="\t")
    get_count(p_internal=[ll.strip() for ll in example.split(",")])
print()


examples2 = [
    "+1, -2, +3, +1",  # 2
    "+1, -1",  # 0
    "+3, +3, +4, -2, -4",  # 10
    "-6, +3, +8, +5, -6",  # 5
    "+7, +7, -2, -7, -4",  # 14
]


def get_count2(p_internal):
    value = 0
    seen = set()
    while True:
        for v in p_internal:
            value += int(v)
            if value in seen:
                print(value)
                return
            seen.add(value)


get_count2(p_internal=parsed(l=s))
print()

for example in examples2:
    print(example, end="\t")
    get_count2(p_internal=[ll.strip() for ll in example.split(",")])
print()
