from functools import reduce
from utils.printing import display

example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


with open("day9.txt", "r") as f:
    s = f.readlines()
    display(s)


def parse(text):
    return [
        list(map(int, filter(None, line.strip().split(" ")))) for line in text
    ]


l_list = parse(text=example.split("\n"))
# l_list = parse(text=s)
display(x=l_list)


def compute(item):
    last = []
    while not all(map(lambda x: x == 0, item)):
        last.append(item[-1])
        item = [a - b for a, b in zip(item[1:], item)]
    return sum(last)


computed = [compute(item=l_item) for l_item in l_list]

display(x=computed)
display(x=sum(computed))


def compute_left(item):
    first = []
    while not all(map(lambda x: x == 0, item)):
        first.append(item[0])
        item = [a - b for a, b in zip(item[1:], item)]
    return reduce(lambda a, b: b - a, first[::-1], 0)


computed_left = [compute_left(item=l_item) for l_item in l_list]

display(x=computed_left)
display(x=sum(computed_left))

# high 634822867
