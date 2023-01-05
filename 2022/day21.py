import re
from operator import add, sub, mul, truediv
from fractions import Fraction


with open("day21.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
# display(lines)


monkeys = dict()


class Monkey:
    def __init__(self, value, left=None, right=None, op=None):
        self.value = value
        self.left = left
        self.right = right
        self.op = {'+': add, '-': sub, '*': mul, '/': truediv}.get(op, None)

    def eval(self):
        if self.value is not None:
            return self.value
        left_value = monkeys[self.left].eval()
        right_value = monkeys[self.right].eval()
        return self.op(left_value, right_value)

    def solve(self, target_value):
        if self.op is None:
            self.value = target_value
        else:
            try:
                left_value = monkeys[self.left].eval()
                if isinstance(left_value, str):
                    raise TypeError()
            except TypeError:
                target_right = monkeys[self.right].eval()
                invert_op = {sub: add, add: sub, truediv: mul, mul: truediv}[self.op]
                monkeys[self.left].solve(invert_op(target_value, target_right))
                # print("Left", invert_op, self.op, target_value, target_right)
            else:
                invert_op = {sub: sub, add: sub, truediv: truediv, mul: truediv}[self.op]
                if self.op in [sub, truediv]:
                    monkeys[self.right].solve(invert_op(left_value, target_value))
                else:
                    monkeys[self.right].solve(invert_op(target_value, left_value))
                # print("Right", invert_op, self.op, target_value, left_value)

    def __repr__(self):
        return f"value {self.value}" \
               f"\tleft {self.left}" \
               f"\tright {self.right}" \
               f"\top {self.op}"


for line in lines:
    d_group = re.match(
        pattern=r"(?P<name>.*): (?P<content>.*)",
        string=line,
    ).groupdict()
    name = d_group['name']
    long_match = r"(?P<left>.*) (?P<op>.*) (?P<right>.*)"
    if re.match(pattern=long_match, string=d_group['content']):
        monkeys[name] = Monkey(
            value=None,
            **re.match(
                pattern=long_match,
                string=d_group['content']
            ).groupdict(),
        )
    else:
        monkeys[name] = Monkey(
            value=Fraction(int(d_group['content'])),
        )


# for name, monkey in monkeys.items():
#     print(name, monkey)

print(monkeys['root'].eval())
print()
print("Left", monkeys[monkeys['root'].left].eval())
print("Right", monkeys[monkeys['root'].right].eval())

monkeys['humn'].value = "Blah"

try:
    print(monkeys[monkeys['root'].left].eval())
except TypeError:
    print("left Errors")
    target = monkeys[monkeys['root'].right].eval()
    print("Target", target)
    monkeys[monkeys['root'].left].solve(target)
    print(monkeys['humn'].value)
