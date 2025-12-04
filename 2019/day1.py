from utils.printing import display


examples = [
    "12",  # 2
    "14",  # 2
    "1969",  # 654
    "100756",  # 33583
]


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    count = 0
    for v in p_internal:
        i = int(v)
        d = i // 3
        dd = d - 2
        count += dd
    print(count)


get_count(p_internal=parsed(l=s))
print()

for example in examples:
    print(example, end="\t")
    get_count(p_internal=[example.strip()])
print()


def get_count2(p_internal):
    count = 0
    for v in p_internal:
        i = int(v)

        dd = i
        while dd > 0:
            d = dd // 3
            dd = d - 2
            if dd <= 0:
                break
            count += dd
    print(count)


get_count2(p_internal=parsed(l=s))
print()

for example in examples:
    print(example, end="\t")
    get_count2(p_internal=[example.strip()])
print()
