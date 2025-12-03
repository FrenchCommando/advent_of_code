import re
from functools import reduce
from operator import mul
from utils.printing import display


with open("day19.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


parsed = [
    {
        key: int(value)
        for key, value in re.match(
            pattern=r"Blueprint (?P<number>.*): "
                    r"Each ore robot costs (?P<cost_ore>.*) ore. "
                    r"Each clay robot costs (?P<cost_clay>.*) ore. "
                    r"Each obsidian robot costs (?P<cost_obsidian_ore>.*) ore and (?P<cost_obsidian_clay>.*) clay. "
                    r"Each geode robot costs (?P<cost_geode_ore>.*) ore and (?P<cost_geode_obsidian>.*) obsidian.",
            string=line,
        ).groupdict().items()
    }
    for line in lines
]
display(parsed)


def quality_value(d_blueprint, periods):
    state = [(
        0,  # geode
        0,  # obsidian
        0,  # clay
        0,  # ore
        0,  # geode-robot
        0,  # obsidian-robot
        0,  # clay-robot
        1,  # ore-robot
    )]
    for period in range(periods):
        print("Period", period, '\t', len(state))
        state_added = []
        for selected_state in state:
            if selected_state[3] >= d_blueprint['cost_ore']:
                selected_with_ore = (
                    selected_state[0],
                    selected_state[1],
                    selected_state[2],
                    selected_state[3] - d_blueprint['cost_ore'] - 1,
                    selected_state[4],
                    selected_state[5],
                    selected_state[6],
                    selected_state[7] + 1,
                )
                state_added.append(selected_with_ore)
            if selected_state[3] >= d_blueprint['cost_clay']:
                selected_with_clay = (
                    selected_state[0],
                    selected_state[1],
                    selected_state[2] - 1,
                    selected_state[3] - d_blueprint['cost_clay'],
                    selected_state[4],
                    selected_state[5],
                    selected_state[6] + 1,
                    selected_state[7],
                )
                state_added.append(selected_with_clay)
            if selected_state[3] >= d_blueprint['cost_obsidian_ore'] and \
                    selected_state[2] >= d_blueprint['cost_obsidian_clay']:
                selected_with_obsidian = (
                    selected_state[0],
                    selected_state[1] - 1,
                    selected_state[2] - d_blueprint['cost_obsidian_clay'],
                    selected_state[3] - d_blueprint['cost_obsidian_ore'],
                    selected_state[4],
                    selected_state[5] + 1,
                    selected_state[6],
                    selected_state[7],
                )
                state_added.append(selected_with_obsidian)
            if selected_state[3] >= d_blueprint['cost_geode_ore'] and \
                    selected_state[1] >= d_blueprint['cost_geode_obsidian']:
                selected_with_geode = (
                    selected_state[0] - 1,
                    selected_state[1] - d_blueprint['cost_geode_obsidian'],
                    selected_state[2],
                    selected_state[3] - d_blueprint['cost_geode_ore'],
                    selected_state[4] + 1,
                    selected_state[5],
                    selected_state[6],
                    selected_state[7],
                )
                state_added.append(selected_with_geode)
        state.extend(state_added)

        state_end = []
        for selected_state in state:
            increased_state = (
                    selected_state[0] + selected_state[4],
                    selected_state[1] + selected_state[5],
                    selected_state[2] + selected_state[6],
                    selected_state[3] + selected_state[7],
                    selected_state[4],
                    selected_state[5],
                    selected_state[6],
                    selected_state[7],
            )
            state_end.append(increased_state)

        # mask per period for bounding
        mask = [True] * 8
        if period == periods - 1:
            mask = [
                True, False, False, False,
                False, False, False, False,
            ]  # geode only
        if period == periods - 2:
            mask = [
                True, False, False, False,
                True, False, False, False,
            ]  # geode and geode-robot
        if period == periods - 3:
            mask = [
                True, True, False, True,
                True, False, False, False,
            ]  # geode, geode-robot, material for making geode-robot
        if period == periods - 4:
            mask = [
                True, True, False, True,
                True, True, False, True,
            ]
        if period == periods - 5:
            mask = [
                True, True, True, True,
                True, True, False, True,
            ]  # clay making robot worthless
        state_masked = [
            tuple(value if mask_value else 0 for mask_value, value in zip(mask, item))
            for item in state_end
        ]
        n_remaining = periods - period
        caps = (
            None,
            d_blueprint['cost_geode_obsidian'] * n_remaining,
            d_blueprint['cost_obsidian_clay'] * n_remaining,
            max(
                d_blueprint['cost_ore'], d_blueprint['cost_clay'],
                d_blueprint['cost_obsidian_ore'], d_blueprint['cost_geode_ore']
            ) * n_remaining,
            None, None, None, None,
        )
        state_capped = [
            tuple(
                min(value, cap_value) if cap_value is not None else value
                for cap_value, value in zip(caps, item)
            )
            for item in state_masked
        ]

        state_filtered = []
        for item in sorted(
                state_capped, reverse=True,
                key=lambda x: x[::-1],  # sorting by robot first
        ):
            if len(state_filtered) == 0:
                state_filtered.append(item)
            else:
                last_item = state_filtered[-1]
                diff = tuple(i2 - i1 for i1, i2 in zip(item, last_item))
                if not all(x >= 0 for x in diff):
                    state_filtered.append(item)

        state = state_filtered

        # for item in sorted(state):
        #     print(item)
        # print("End of Period", len(state))
    max_geode = max(x[0] for x in state)
    print("Max Geode", max_geode)
    return max_geode


number_periods = 24
display(sum(
    blueprint['number'] * quality_value(
        d_blueprint=blueprint,
        periods=number_periods,
    )
    for blueprint in parsed
))
print()

number_periods = 32
display(reduce(
    mul,
    (
        quality_value(
            d_blueprint=blueprint,
            periods=number_periods,
        )
        for blueprint in parsed[:3]
    ),
    1,
))
