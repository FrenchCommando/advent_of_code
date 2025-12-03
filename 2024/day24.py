import re
from utils.printing import display

example = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

example2 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


with open("day24.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    i = iter(l)
    rules = []
    try:
        while True:
            line = next(i)
            if not line:
                break
            rules.append(line.strip().split(": "))
    except StopIteration:
        pass
    # print(rules)

    d = dict()
    for left, right in rules:
        d[left] = right == "1"
    # print(d)

    gates = []

    try:
        while True:
            line = next(i)
            pages = line.split(" ")
            gates.append((pages[0], pages[2], pages[1], pages[-1]))
    except StopIteration:
        pass
    # print(gates)

    ops = dict(
        AND= lambda x, y: x and y,
        OR= lambda x, y: x or y,
        XOR= lambda x, y: (x and not y or y and not x),
    )

    while len(gates) > 0:
        for gate in gates:
            x, y, op, z = gate
            if x in d and y in d:
                bx = d[x]
                by = d[y]
                d[z] = ops[op](bx, by)
                gates.remove(gate)
                break
    # print(d)
    c = 0

    for z, v in d.items():
        if v:
            if z.startswith("z"):
                i = int(z[1:])
                c += 2 ** i
                # print(i, c)

    return c


p = count(l=example.split("\n"))
p2 = count(l=example2.split("\n"))
print("count", p, p2)
ps = count(l=[line.strip() for line in s])
print("count", ps)


ops = dict(
    AND=lambda x, y: x and y,
    OR=lambda x, y: x or y,
    XOR=lambda x, y: (x and not y or y and not x),
)

def count2(l):
    i = iter(l)
    rules = []
    try:
        while True:
            line = next(i)
            if not line:
                break
            rules.append(line.strip().split(": "))
    except StopIteration:
        pass
    print(rules)

    gates = []
    try:
        while True:
            line = next(i)
            pages = line.split(" ")
            gates.append((pages[0], pages[2], pages[1], pages[-1]))
    except StopIteration:
        pass
    print(gates)

    d = dict()
    # for left, right in rules:
    #     d[left] = right == "1"
    print(d)
    i = 0

    while len(gates) > 0:
        found = False
        for gate in gates:
            x, y, op, z = gate
            if x in d and y in d:
                bx = d[x]
                by = d[y]
                d[z] = ops[op](bx, by)
                print(x, y, op, z)
                gates.remove(gate)
                found = True
                break
        if not found:
            d[f"x{i:02}"] = True
            d[f"y{i:02}"] = True
            i += 1
        # print in logical order and solve the pattern


count2(l=example.split("\n"))
count2(l=[line.strip() for line in s])
