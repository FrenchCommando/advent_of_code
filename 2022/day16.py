import re
from utils.printing import display


with open("day16.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


class Valve:
    def __init__(self, valves, flow):
        self.valves = valves
        self.flow = flow

    def __repr__(self):
        return f"Valve:\t{self.valves=}\t{self.flow=}"


d_valves = dict()


for line in lines:
    d_group = re.match(
        pattern=r"Valve (?P<name>.*) has flow rate=(?P<flow>.*); "
                r"tunnel(s?) lead(s?) to valve(s?) "
                r"(?P<valves>.*)",
        string=line,
    ).groupdict()
    d_valves[d_group['name']] = Valve(valves=d_group['valves'].split(", "), flow=int(d_group['flow']))

display(d_valves)

n_minutes = 30
print("The End")
