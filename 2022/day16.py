import re
from collections import defaultdict
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


d_flow = {name: valve.flow for name, valve in d_valves.items()}
d_tunnel = {name: valve.valves for name, valve in d_valves.items()}

display(d_flow)
display(d_tunnel)

d_full_flow = {tuple(): 0}  # tuple open valves : flow per period


def advance(d_state):
    max_result = 0
    d_out = defaultdict(
        lambda: defaultdict(lambda: defaultdict(int))
    )
    for position, ddd in d_state.items():
        tunnel = d_tunnel[position]
        for turning, dddd in ddd.items():
            for open_valves, full_flow in dddd.items():
                flow_increment = d_full_flow[open_valves]
                full_flow_post = full_flow + flow_increment
                open_valves_with_addition = open_valves
                if (position not in open_valves) and turning:
                    open_valves_with_addition = tuple(sorted(list(open_valves) + [position]))
                    if open_valves_with_addition not in d_full_flow:
                        d_full_flow[open_valves_with_addition] = flow_increment + d_flow[position]
                if d_flow[position] != 0 and not turning:
                    d_out[position][True][open_valves] = full_flow_post
                for destination in tunnel:
                    d_out[destination][False][open_valves_with_addition] = \
                        max(full_flow_post, d_out[destination][False][open_valves_with_addition])
                    max_result = max(max_result, d_out[destination][False][open_valves_with_addition])
    return max_result, d_out


state_start = {
    "AA": {
        False: {
            tuple(): 0
        }
    }
}
print(state_start)

n_minutes = 30
state = state_start


for period in range(n_minutes + 1):
    max_value, state = advance(state)
    print(period, max_value)


print("End Part 1")
print()


def advance2(d_state, remaining_periods, max_result_estimate):
    max_result = 0
    max_theo_estimate = 0
    node_count = 0
    d_out = defaultdict(
        lambda: defaultdict(int)
    )
    for open_valves, ddd in d_state.items():
        flow_increment = d_full_flow[open_valves]
        unopen_valves_flow = sum(sorted(
            (d_flow[valve] for valve in d_valves if valve not in open_valves),
            reverse=True,
        )[:(remaining_periods // 2 + 1)])
        for (position, turning, position2, turning2), full_flow in ddd.items():
            node_count += 1
            full_flow_post = full_flow + flow_increment

            tunnel = d_tunnel[position]
            tunnel2 = d_tunnel[position2]

            theo_estimate = full_flow_post + (flow_increment + unopen_valves_flow) * remaining_periods

            if theo_estimate < max_result_estimate:
                continue

            max_theo_estimate = max(max_theo_estimate, theo_estimate)
            max_result_estimate = max(
                max_result_estimate, full_flow_post + flow_increment * remaining_periods,
            )
            max_result = max(max_result, full_flow_post)
            open_valves_with_addition = open_valves
            if ((position not in open_valves) and turning) or ((position2 not in open_valves) and turning2):
                list_valves = list(open_valves)
                flow_increment_with_addition = flow_increment
                if turning and position not in list_valves:
                    list_valves.append(position)
                    flow_increment_with_addition += d_flow[position]
                if turning2 and position2 not in list_valves:
                    list_valves.append(position2)
                    flow_increment_with_addition += d_flow[position2]
                open_valves_with_addition = tuple(sorted(list_valves))
                if open_valves_with_addition not in d_full_flow:
                    d_full_flow[open_valves_with_addition] = flow_increment_with_addition
            if d_flow[position] != 0 and not turning and position not in open_valves_with_addition:
                if d_flow[position2] != 0 and not turning2 and position2 not in open_valves_with_addition:
                    if position != position2:
                        position_min, position_max = min(position, position2), max(position, position2)
                        d_out[open_valves_with_addition][(position_min, True, position_max, True)] = max(
                            full_flow_post,
                            d_out[open_valves_with_addition][(position, True, position2, True)],
                            d_out[open_valves_with_addition][(position2, True, position, True)]
                        )
                for destination2 in tunnel2:
                    d_out[open_valves_with_addition][(position, True, destination2, False)] = \
                        max(
                            full_flow_post,
                            d_out[open_valves_with_addition][(position, True, destination2, False)]
                        )
            for destination in tunnel:
                if d_flow[position2] != 0 and not turning2 and position2 not in open_valves_with_addition:
                    d_out[open_valves_with_addition][(position2, True, destination, False)] = max(
                        full_flow_post,
                        d_out[open_valves_with_addition][(destination, False, position2, True)],
                        d_out[open_valves_with_addition][(position2, True, destination, False)],
                    )
                for destination2 in tunnel2:
                    destination_min, destination_max = \
                        min(destination, destination2), max(destination, destination2)
                    d_out[open_valves_with_addition][(destination_min, False, destination_max, False)] = \
                        max(
                            full_flow_post,
                            d_out[open_valves_with_addition][(destination, False, destination2, False)],
                            d_out[open_valves_with_addition][(destination2, False, destination, False)],
                        )
    return max_result, max_result_estimate, max_theo_estimate, node_count, d_out


state_start2 = {
    tuple(): {("AA", False, "AA", False): 0}
}
print(state_start2)

n_minutes2 = 26
state2 = state_start2
max_estimate = 0

for period in range(n_minutes2 + 1):
    period_remaining = n_minutes2 - period
    max_value, max_estimate, max_th, number_node, state2 = advance2(
        d_state=state2, remaining_periods=period_remaining, max_result_estimate=max_estimate,
    )
    print(f"{period}\t{period_remaining}\t{number_node}\t{max_value}\t{max_estimate}\t{max_th}")


print("The End")
