import re
from utils.printing import display

with open("day10.txt", "r") as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]
display(lines)

cycle = 0
register = 1
cycle_to_register = dict()

for line in lines:
    if line == "noop":
        cycle += 1
    else:
        d_group = re.match(
            pattern=r"addx (?P<value>.*)",
            string=line,
        ).groupdict()
        value = int(d_group['value'])
        cycle += 2
        register += value
        cycle_to_register[cycle] = register

display(cycle_to_register)


def register_at(cycle_value):
    # should use bisect
    left_value = 1
    for k, v in cycle_to_register.items():
        if k < cycle_value:
            left_value = v
        else:
            return left_value
    return left_value


signal_map = {
    cycle_value: register_at(cycle_value) for cycle_value in [20, 60, 100, 140, 180, 220]
}
display(signal_map)
display(sum(c * v for c, v in signal_map.items()))
