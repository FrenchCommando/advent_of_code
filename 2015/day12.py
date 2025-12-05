import json
import re

from utils.printing import display


examples = [
    "[1,2,3]", """{"a":2,"b":4}""",
    "[[[3]]]", """{"a":{"b":4},"c":-1}""",
    """{"a":[-1,1]}""", """[-1,{"a":1}]""",
    "[]", "{}",
]


with open("day12.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p_internal):
    count = 0
    for p in p_internal:
        n = re.findall(r"([-\d]+)", p)
        value = sum(map(int, n))
        print(n, value)
        count += value
    print(count)


get_count(p_internal=[sss.strip() for sss in s])
print()
get_count(p_internal=[sss.strip() for sss in examples])
print()


bad_value = "red"


def compute(n):
    if isinstance(n, list):
        count = 0
        for p in n:
            count += compute(p)
        return count
    if isinstance(n, dict):
        count = 0
        for k, v in n.items():
            count += compute(v)
            if isinstance(v, str) and v == "red":
                return 0
        return count
    if isinstance(n, int):
        return n
    if isinstance(n, str):
        return 0
    raise TypeError(n)


def get_count2(p_internal):
    count = 0
    for p in p_internal:
        n = json.loads(p)
        value = compute(n)
        print(n, value)
        count += value
    print(count)


examples2 = [
    "[1,2,3]",
    """[1,{"c":"red","b":2},3]""",
    """{"d":"red","e":[1,2,3,4],"f":5}""",
    """[1,"red",5]""",
]


get_count2(p_internal=[sss.strip() for sss in s])
print()
get_count2(p_internal=[sss.strip() for sss in examples2])
print()
