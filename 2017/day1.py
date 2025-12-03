from utils.printing import display


examples = [
    "1122",
    "1111",
    "1234",
    "91212129",
]


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    count = 0
    for i, c in enumerate(p_internal):
        if c == p_internal[(i + 1) % len(p_internal)]:
            count += int(c)
    print(count)


get_count(p_internal=parsed(l=s[0]))
print()

for example in examples:
    print(example, end="\t")
    get_count(p_internal=[ll.strip() for ll in example])
print()


examples2 = [
    "1212",
    "1221",
    "123425",
    "123123",
    "12131415",
]


def get_count2(p_internal):
    count = 0
    n = len(p_internal)
    n2 = n // 2
    for i, c in enumerate(p_internal):
        if c == p_internal[(i + n2) % n]:
            count += int(c)
    print(count)


get_count2(p_internal=parsed(l=s[0]))
print()

for example in examples2:
    print(example, end="\t")
    get_count2(p_internal=[ll.strip() for ll in example])
print()
