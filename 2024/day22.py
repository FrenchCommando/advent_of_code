import re
from utils.printing import display

example = """1
10
100
2024"""



with open("day22.txt", "r") as f:
    s = f.readlines()
    display(s)


def generate(number, skip):
    for turn in range(skip):
        v = number * 64
        number = number ^ v
        number = number % 16777216
        v = number // 32
        number = number ^ v
        number = number % 16777216
        v = number * 2048
        number = number ^ v
        number = number % 16777216
    return number

def count(l):
    c = []
    for line in l:
        number = int(line)
        generated = generate(number=number, skip=2000)
        c.append(generated)
    print(c)
    return sum(c)


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def bananas(index, number, skip, container):
    last_number = number % 10
    increments = []
    for turn in range(skip):
        v = number * 64
        number = number ^ v
        number = number % 16777216
        v = number // 32
        number = number ^ v
        number = number % 16777216
        v = number * 2048
        number = number ^ v
        number = number % 16777216
        if last_number is not None:
            number_trim = number % 10
            increments.append(number_trim - last_number)
            if len(increments) >= 4:
                sequence = tuple(increments[-4:])
                # print(sequence)
                if sequence not in container:
                    container[sequence] = dict()
                if index not in container[sequence]:
                    container[sequence][index] = number_trim
        last_number = number_trim


def count2(l):
    print(l)
    container = dict()

    for index, line in enumerate(l):
        number = int(line)
        bananas(index=index, number=number, skip=2000, container=container)

    n_bananas = {b: sum(v.values()) for b, v in container.items()}

    # print(container)
    print(container.get((-2,1,-1,3), None))
    # print(n_bananas)
    return max(n_bananas.values())


p200 = count2(l=['123'])
p20 = count2(l=['1', '2', '3', '2024'])
print("count2", p200, p20)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
