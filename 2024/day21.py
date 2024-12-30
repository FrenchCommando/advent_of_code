import re
from functools import lru_cache

from utils.printing import display

example = """029A
980A
179A
456A
379A"""


with open("day21.txt", "r") as f:
    s = f.readlines()
    display(s)


numpad = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A'],
]
keypad = [
    [None, '^', 'A'],
    ['<', 'v', '>'],
]
pos_num = {
    numpad[i][j]: (i, j)
    for i in range(len(numpad)) for j in range(len(numpad[0]))
    if numpad[i][j] is not None
}
pos_key = {
    keypad[i][j]: (i, j)
    for i in range(len(keypad)) for j in range(len(keypad[0]))
    if keypad[i][j] is not None
}



def convert_key(num0, num1):
    i0, j0 = pos_key[num0]
    i1, j1 = pos_key[num1]

    if j0 == 0 and i1 == 0 or i0 == 0 and j1 == 0:
        intermediate = keypad[max(i0, i1)][max(j0, j1)]
        out = convert_key(num0, intermediate) + convert_key(intermediate, num1)
        # print(num0, num1, out)
        return out

    out = []
    if i0 < i1:
        out.append("v" * (i1 - i0))
    elif i0 > i1:
        out.append("^" * (i0 - i1))

    if j0 < j1:
        out.append(">" * (j1 - j0))
    elif j0 > j1:
        out.append("<" * (j0 - j1))

    if len(out) == 0:
        return ""
    if len(out) == 1:
        return out[0]
    return "".join(out), "".join(out[::-1])


def convert_num(num0, num1):
    i0, j0 = pos_num[num0]
    i1, j1 = pos_num[num1]
    if j0 == 0 and i1 == 3 or i0 == 3 and j1 == 0:
        intermediate = numpad[min(i0, i1)][max(j0, j1)]
        out = convert_num(num0, intermediate) + convert_num(intermediate, num1)
        # print(num0, num1, out)
        return out
    out = []
    if j0 < j1:
        out.append(">" * (j1-j0))
    elif j0 > j1:
        out.append("<" * (j0-j1))
    if i0 < i1:
        out.append("v" * (i1-i0))
    elif i0 > i1:
        out.append("^" * (i0-i1))

    if len(out) == 0:
        return ""
    if len(out) == 1:
        return out[0]
    return "".join(out), "".join(out[::-1])


@lru_cache(maxsize=1_000_000)
def counted(cc, n_robots):
    # print("Counted", cc, n_robots)
    if n_robots == 0:
        return len(cc)

    if cc.index("A") != len(cc) - 1:
        s_cc = cc.split("A")[:-1]
        return sum(counted(s_u + "A", n_robots) for s_u in s_cc)

    c1_list = [[]]
    last1 = "A"
    for v0 in cc:
        cc1 = convert_key(num0=last1, num1=v0)
        if isinstance(cc1, tuple):
            c1_temp = []
            for ccc1 in cc1:
                for c1_element in c1_list:
                    c1_temp.append(c1_element + [ccc1 + "A"])
            c1_list = c1_temp
        else:
            for c1_element in c1_list:
                c1_element.append(cc1 + "A")
        last1 = v0

    return min(counted(''.join(u), n_robots - 1) for u in c1_list)


def command(line, n_robots):
    # wrong track, I need a fancy branch-and-bound
    # choose between going horizontal first or vertical first
    # while avoiding voids
    print("Command", line)
    c0 = [[]]
    last = "A"
    for v in line:
        cc0 = convert_num(num0=last, num1=v)
        # print(last, v, cc0)
        if isinstance(cc0, tuple):
            c0_temp = []
            for ccc0 in cc0:
                for c0_element in c0:
                    # print(c0_element, ccc0)
                    c0_temp.append(c0_element + [ccc0 + "A"])
            c0 = c0_temp
        else:
            for c0_element in c0:
                c0_element.append(cc0 + "A")
        last = v
    print(len(c0), c0)

    c0_joined = [''.join(u) for u in c0]

    results = [counted(cc, n_robots) for cc in c0_joined]
    print(c0_joined)
    print(results)
    return min(results)


def count(l, n_robots):
    print(l)
    c = 0
    for line in l:
        code = command(line=line, n_robots=n_robots)
        num = int(line[:-1])
        print(line, code, num)
        print()
        c += code * num
    return c


p = count(l=example.split("\n"), n_robots=2)
print("count", p)
ps = count(l=[line.strip() for line in s], n_robots=2)
print("count", ps)

# unused anyway
# p2 = count(l=example.split("\n"), n_robots=25)
# print("count2", p2)
ps2 = count(l=[line.strip() for line in s], n_robots=25)
print("count2", ps2)
