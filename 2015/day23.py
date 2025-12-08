from utils.printing import display


example = """inc a
jio a, +2
tpl a
inc a"""


with open("day23.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p, a0):
    data = dict(a=a0, b=0)
    i = 0

    while i < len(p):
        line = p[i]
        # print(line, data)
        left, right = line.split(" ", 1)
        if left == "hlf":
            data[right] = data[right] // 2
            i += 1
            continue
        if left == "tpl":
            data[right] = data[right] * 3
            i += 1
            continue
        if left == "inc":
            data[right] += 1
            i += 1
            continue
        if left == "jmp":
            ii = int(right)
            i += ii
            continue
        if left == "jie":
            rr, rrr = right.split(", ", 1)
            r0 = int(rrr)
            v = data[rr]
            if v % 2 == 0:
                i += r0
                continue
            i += 1
            continue
        if left == "jio":
            rr, rrr = right.split(", ", 1)
            r0 = int(rrr)
            v = data[rr]
            if v == 1:
                i += r0
                continue
            i += 1
            continue

    print(data)
    print(data['b'])
    print()


get_count(p=[sss.strip() for sss in s], a0=0)
print()
get_count(p=[sss.strip() for sss in example.split("\n")], a0=0)
print()
get_count(p=[sss.strip() for sss in s], a0=1)
print()


