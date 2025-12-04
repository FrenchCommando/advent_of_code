from utils.printing import display


examples = [
    "1",
    "11",
    "21",
    "1211",
    "111221",
]

with open("day10.txt", "r") as f:
    s = f.readlines()
    display(s)


def apply(v):
    out = []

    cc = None
    ccc = 0
    for c in v:
        if cc is None:
            cc = c
            ccc = 1
            continue
        if c == cc:
            ccc += 1
            continue
        out.append(f"{ccc}")
        out.append(cc)
        ccc = 1
        cc = c
    out.append(f"{ccc}")
    out.append(cc)

    return ''.join(out)


def get_count(p_internal, n):
    for p in p_internal:
        v = p
        print(v)
        for i in range(n):
            v = apply(v)
            # print(v)

        print(len(v), p)
        print()



get_count(p_internal=[sss.strip() for sss in s], n=40)
print()
get_count(p_internal=[sss.strip() for sss in examples], n=40)
print()

get_count(p_internal=[sss.strip() for sss in s], n=50)
print()
get_count(p_internal=[sss.strip() for sss in examples], n=50)
print()
