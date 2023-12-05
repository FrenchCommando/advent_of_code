from utils.printing import display

example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


with open("day4.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(val):
    print(val)
    game, content = val.split(":")
    game_id = int(game.split(" ")[-1])
    win, select = content.split("|")
    winning_numbers = list(sorted(filter(None, win.strip().split(" "))))
    selected_numbers = list(sorted(filter(None, select.strip().split(" "))))
    return game_id, winning_numbers, selected_numbers


def check(val):
    game_id, winning_numbers, selected_numbers = val
    n = len(set(winning_numbers) & set(selected_numbers))
    if n == 0:
        return 0
    return 2 ** (n - 1)


def check2(val):
    game_id, winning_numbers, selected_numbers = val
    n = len(set(winning_numbers) & set(selected_numbers))
    return n


l_list = []
powers = []
wins = []

# for x in s:
for x in example.split("\n"):
    out = parsed(val=x.strip())
    display(x=out)
    l_list.append(out)
    powers.append(check(val=out))
    wins.append(check2(val=out))

display(x=l_list)
display(x=powers)
display(x=sum(powers))
display(x=wins)

r_wins = list(reversed(wins))
for i, num in enumerate(r_wins):
    for x in range(num):
        r_wins[i] += r_wins[i - x - 1]
display(x=r_wins)
display(x=sum(r_wins)+len(r_wins))
