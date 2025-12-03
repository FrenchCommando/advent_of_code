from utils.printing import display


examples = [
    "(())", "()()",
    "(((", "(()(()(",
    "))(((((",
    "())", "))(",
    ")))", ")())())",
]


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    l = p_internal.count("(")
    r = p_internal.count(")")
    count = l - r
    print(count)


get_count(p_internal=parsed(l=s)[0])
print()

for example in examples:
    print(example, end="\t")
    get_count(p_internal=example)
print()


examples2 = [
    ")",
    "()())",
]


def get_count2(p_internal):
    value = 0
    for i, c in enumerate(p_internal, 1):
        if c == "(":
            value += 1
        if c == ")":
            value -= 1
        if value < 0:
            print(i)
            break


get_count2(p_internal=parsed(l=s)[0])
print()

for example in examples2:
    print(example, end="\t")
    get_count2(p_internal=example)
print()
