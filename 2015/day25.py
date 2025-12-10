import re
from utils.printing import display


with open("day25.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p):
    n_start = 20151125
    n_mult = 252533
    n_mod = 33554393

    row, column = map(int, re.findall(r"(\d+)", p))
    print(row, column)

    line_number = row + column
    line_count = ((line_number - 2) * (line_number - 1)) // 2
    # print(line_count)
    number_index = line_count + column
    print(number_index)

    n = n_start
    for i in range(number_index - 1):
        n *= n_mult
        n %= n_mod
    print(n)


get_count(p=s[0])
print()
get_count(p="1 1")
print()
get_count(p="2 2")
print()
get_count(p="2 4")
print()
