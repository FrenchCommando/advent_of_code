import hashlib

from utils.printing import display


examples = [
    "abcdef",
    "pqrstuv",
]


with open("day4.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p_internal):
    i = 0
    while True:
        sss = f"{p_internal}{i}"
        res = hashlib.md5(sss.encode()).hexdigest()
        # print(res, sss)
        if res[:5] == "00000":
            print(res, sss, i)
            break
        i += 1


get_count(p_internal=s[0].strip())
print()

for example in examples:
    print(example, end="\t")
    get_count(p_internal=example)
print()


def get_count2(p_internal):
    i = 0
    while True:
        sss = f"{p_internal}{i}"
        res = hashlib.md5(sss.encode()).hexdigest()
        # print(res, sss)
        if res[:6] == "000000":
            print(res, sss, i)
            break
        i += 1


get_count2(p_internal=s[0].strip())
print()

for example in examples:
    print(example, end="\t")
    get_count2(p_internal=example)
print()