import re
from utils.printing import display


with open("day15.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)

positions = [
    {k: int(v) for k, v in re.match(
        pattern=r"Sensor at x=(?P<x_sensor>.*), y=(?P<y_sensor>.*): "
                r"closest beacon is at x=(?P<x_beacon>.*), y=(?P<y_beacon>.*)",
        string=line,
    ).groupdict().items()} for line in lines
]
display(positions)


def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def checked_for_y(y_selected, ignore_beacon=True):
    checked = set()
    for d in positions:
        distance = manhattan(
            x1=d['x_sensor'], y1=d['y_sensor'],
            x2=d['x_beacon'], y2=d['y_beacon'],
        )
        x_projection_distance = manhattan(x1=0, y1=d['y_sensor'], x2=0, y2=y_selected)
        projection_remaining = distance - x_projection_distance
        if projection_remaining >= 0:
            for x_value in range(d['x_sensor'] - projection_remaining, d['x_sensor'] + projection_remaining + 1):
                checked.add(x_value)

    if ignore_beacon:
        for d in positions:
            if d['y_beacon'] == y_selected:
                if d['x_beacon'] in checked:
                    checked.remove(d['x_beacon'])

    return checked


y_checked = checked_for_y(y_selected=2000000, ignore_beacon=True)
display(len(y_checked))
y_checked = checked_for_y(y_selected=10, ignore_beacon=True)
display(len(y_checked))
print()


def checked_range_for_y(y_selected, coord_max):
    checked_range = [False for x in range(0, coord_max + 1)]
    for d in positions:
        distance = manhattan(
            x1=d['x_sensor'], y1=d['y_sensor'],
            x2=d['x_beacon'], y2=d['y_beacon'],
        )
        x_projection_distance = manhattan(x1=0, y1=d['y_sensor'], x2=0, y2=y_selected)
        projection_remaining = distance - x_projection_distance
        if projection_remaining >= 0:
            for x_value in range(max(0, d['x_sensor'] - projection_remaining),
                                 min(coord_max, d['x_sensor'] + projection_remaining) + 1):
                checked_range[x_value] = True
    return checked_range


def find_beacon(coord_max):
    # check the outside border of each diamond
    for d in positions:
        print(d)
        distance = manhattan(
            x1=d['x_sensor'], y1=d['y_sensor'],
            x2=d['x_beacon'], y2=d['y_beacon'],
        )
        x_sensor = d['x_sensor']
        y_sensor = d['y_sensor']
        distance_plus_one = distance + 1
        border = [
            (x_sensor + i, y_sensor + (distance_plus_one - i)) for i in range(distance_plus_one + 1)
        ] + [
            (x_sensor - i, y_sensor + (distance_plus_one - i)) for i in range(distance_plus_one + 1)
        ] + [
            (x_sensor + i, y_sensor - (distance_plus_one - i)) for i in range(distance_plus_one + 1)
        ] + [
            (x_sensor - i, y_sensor - (distance_plus_one - i)) for i in range(distance_plus_one + 1)
        ]
        for x, y in border:
            if (x >= 0) and (y >= 0) and (x <= coord_max) and (y <= coord_max):
                valid = True
                for pos in positions:
                    pos_distance = manhattan(
                        x1=pos['x_sensor'], y1=pos['y_sensor'],
                        x2=pos['x_beacon'], y2=pos['y_beacon'],
                    )
                    current_distance = manhattan(
                        x1=pos['x_sensor'], y1=pos['y_sensor'],
                        x2=x, y2=y,
                    )
                    if pos_distance >= current_distance:
                        valid = False
                        break
                if valid:
                    return x, y
    return -1, -1


beacon_x, beacon_y = find_beacon(coord_max=4000000)
display(beacon_x)
display(beacon_y)
display(beacon_y + 4000000 * beacon_x)
print()

beacon_x, beacon_y = find_beacon(coord_max=20)
display(beacon_x)
display(beacon_y)
display(beacon_y + 4000000 * beacon_x)
