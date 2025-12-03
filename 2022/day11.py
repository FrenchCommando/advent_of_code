import re
from functools import reduce
from operator import mul, add
from utils.printing import display


with open("day11.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


class Monkey:
    def __init__(self, items, operation, test, monkey_true, monkey_false):
        self.items = items
        self.operation = operation
        self.test = test
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        # self.next_items = []
        self.count = 0

    def receive(self):
        pass
        # self.items = self.next_items
        # self.next_items = []

    def reduce(self, factor):
        self.items = [item % factor for item in self.items]

    def inspect(self):
        for item in self.items:
            self.count += 1
            item = self.operation(item)
            # item = item // 3
            d_monkey[
                self.monkey_true
                if self.test(item)
                else self.monkey_false
            ].items.append(item)
        self.items = []


def parse_monkey_name(line):
    d_group = re.match(
        pattern=r"Monkey (?P<number>.*):",
        string=line,
    ).groupdict()
    return int(d_group['number'])


def parse_monkey_items(line):
    d_group = re.match(
        pattern=r"Starting items: (?P<items>.*)",
        string=line,
    ).groupdict()
    items_str = d_group['items']
    return list(map(int, items_str.split(", ")))


def parse_monkey_operation(line):
    d_group = re.match(
        pattern=r"Operation: new = old (?P<operation>.*) (?P<number>.*)",
        string=line,
    ).groupdict()
    operation_str = d_group['operation']
    number_str = d_group['number']
    operation_object = add if operation_str == "+" else mul
    if number_str == "old":
        return lambda x: operation_object(x, x)
    number_int = int(number_str)
    return lambda x: operation_object(x, number_int)


def parse_monkey_test(line):
    d_group = re.match(
        pattern=r"Test: divisible by (?P<number>.*)",
        string=line,
    ).groupdict()
    number = int(d_group['number'])
    return lambda x: x % number == 0, number


def parse_monkey_true(line):
    d_group = re.match(
        pattern=r"If true: throw to monkey (?P<number>.*)",
        string=line,
    ).groupdict()
    return int(d_group['number'])


def parse_monkey_false(line):
    d_group = re.match(
        pattern=r"If false: throw to monkey (?P<number>.*)",
        string=line,
    ).groupdict()
    return int(d_group['number'])


d_monkey = dict()
line_iter = iter(lines)
factors = []
try:
    while True:
        name = parse_monkey_name(line=next(line_iter))
        items = parse_monkey_items(line=next(line_iter))
        operation = parse_monkey_operation(line=next(line_iter))
        test, factor = parse_monkey_test(line=next(line_iter))
        factors.append(factor)
        monkey_true = parse_monkey_true(line=next(line_iter))
        monkey_false = parse_monkey_false(line=next(line_iter))
        d_monkey[name] = Monkey(
            items=items, operation=operation,
            test=test, monkey_true=monkey_true, monkey_false=monkey_false
        )
        next(line_iter)
except StopIteration:
    pass


n_rounds = 10001
big_factor = reduce(mul, factors)

for one_round in range(n_rounds):
    print(one_round)
    counts = {key: monkey.count for key, monkey in d_monkey.items()}
    items = {key: monkey.items for key, monkey in d_monkey.items()}
    display(counts)
    # display(items)
    display(reduce(mul, sorted(counts.values())[-2:], 1))
    for monkey in d_monkey.values():
        monkey.inspect()
    for monkey in d_monkey.values():
        monkey.receive()
    for monkey in d_monkey.values():
        monkey.reduce(factor=big_factor)
