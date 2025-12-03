import re
from utils.printing import display

example = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""


with open("day3.txt", "r") as f:
    s = f.readlines()
    display(s)


mul_pattern = r"mul\((\d{1,3})\,(\d{1,3})\)"


def parsed(l):
    print(l)
    return [m for m in re.findall(pattern=mul_pattern, string=l)]


p = parsed(l=example)
print("parsed", p)
ps = parsed(l=" ".join(s))
print("rparsed", ps)


def score(l):
    return sum((int(a) * int(b) for a,b in l))

pp = score(l=p)
print("pp", pp)
pps = score(l=ps)
print("pps", pps)


example2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
do_pattern = r"(do\(\))"
dont_pattern = r"(don't\(\))"
mul_pattern = r"mul\((\d{1,3})\,(\d{1,3})\)"


def parsed2(l):
    result = []
    on = True
    for u in re.findall(pattern=rf"({'|'.join((do_pattern, dont_pattern, mul_pattern))})", string=l):
        if u[0] == 'do()':
            on = True
        elif u[0] == "don't()":
            on = False
        elif on:
            left = u[-2]
            right = u[-1]
            result.append((left, right))
    return result



p2 = parsed2(l=example2)
print("parsed2", p2)
ps2 = parsed2(l=" ".join(s))
print("rparsed2", ps2)

pp2 = score(l=p2)
print("pp2", pp2)
pps2 = score(l=ps2)
print("pps2", pps2)
