import math
from utils.printing import display

example = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


with open("day2.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(val):
    print(val)
    game, content = val.split(":")
    game_id = int(game.split(" ")[1])
    content_parsed = []
    for u in content.split(";"):
        pairs = u.strip().split(",")
        one_set = dict()
        for pair in pairs:
            number, color = pair.strip().split(" ")
            one_set[color] = int(number)
        content_parsed.append(one_set)
    return game_id, content_parsed


ref = dict(red=12, green=13, blue=14)


def check(val):
    game_id, content_parsed = val
    for u in content_parsed:
        for color in ref:
            if u.get(color, 0) > ref[color]:
                return False
    return True


def power(val):
    game_id, content_parsed = val
    count = dict(red=0, green=0, blue=0)
    for u in content_parsed:
        for color in ref:
            if u.get(color, 0) > count[color]:
                count[color] = u.get(color, 0)
    return math.prod(count.values())


l_list = []
selected = []
powers = []
# for x in s:
for x in example.split("\n"):
    out = parsed(val=x.strip())
    display(x=out)
    l_list.append(out)
    if check(val=out):
        selected.append(out[0])
    powers.append(power(val=out))

display(x=l_list)
display(x=selected)
display(x=sum(selected))
display(x=powers)
display(x=sum(powers))
