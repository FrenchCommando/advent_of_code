import re
from functools import reduce

from utils.printing import display

example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """


with open("day6.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip("\n") for ll in l]


def get_count(p_internal):
    contents = []
    operations = []
    for stuff in p_internal:
        if "+" in stuff:
            operations.extend(list(re.findall(r"[+*]", stuff)))
        else:
            contents.append(list(map(int, re.findall(r"\d+", stuff))))
    # print(operations)
    # print(contents)
    results = []
    for i, operation in enumerate(operations):
        if operation == "+":
            results.append(sum(line[i] for line in contents))
        else:
            results.append(reduce(lambda x, y: x * y, (line[i] for line in contents)))

    print(sum(results))


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()


def get_count2(p_internal):
    spaces = []
    operations = []
    for i, c in enumerate(p_internal[-1]):
        if c != " ":
            spaces.append(i)
            operations.append(c)

    contents = []
    for stuff in p_internal[:-1]:
        line = []
        for i, j in zip(spaces, spaces[1:]):
            line.append(stuff[i:j-1])
        line.append(stuff[spaces[-1]:])
        contents.append(line)
    # print(operations)
    # print(contents)
    results = []
    for i, operation in enumerate(operations):
        operands = [
            int(''.join(line[i][k] for line in contents)) for k in range(len(contents[0][i]))
        ]
        if operation == "+":
            results.append(sum(operands))
        else:
            results.append(reduce(lambda x, y: x * y, operands))

    print(sum(results))


get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p)
print()
