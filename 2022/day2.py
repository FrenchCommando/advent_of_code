from utils.printing import display


with open("day2.txt", "r") as f:
    lines = f.readlines()
    display(lines)


def score(s):
    left, right = s.strip().split(" ")
    if right == "X":
        my_value = 1
        if left == "A":
            my_score = 3
        if left == "B":
            my_score = 0
        if left == "C":
            my_score = 6
    if right == "Y":
        my_value = 2
        if left == "A":
            my_score = 6
        if left == "B":
            my_score = 3
        if left == "C":
            my_score = 0
    if right == "Z":
        my_value = 3
        if left == "A":
            my_score = 0
        if left == "B":
            my_score = 6
        if left == "C":
            my_score = 3
    return my_value + my_score


def score2(s):
    left, right = s.strip().split(" ")
    if right == "X":
        my_value = 0
        if left == "A":
            my_score = 3
        if left == "B":
            my_score = 1
        if left == "C":
            my_score = 2
    if right == "Y":
        my_value = 3
        if left == "A":
            my_score = 1
        if left == "B":
            my_score = 2
        if left == "C":
            my_score = 3
    if right == "Z":
        my_value = 6
        if left == "A":
            my_score = 2
        if left == "B":
            my_score = 3
        if left == "C":
            my_score = 1
    return my_value + my_score


display(lines)
display([score(s=s) for s in lines])
display(sum(score(s=s) for s in lines))
display([score2(s=s) for s in lines])
display(sum(score2(s=s) for s in lines))
