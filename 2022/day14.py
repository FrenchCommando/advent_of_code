from utils.printing import display


with open("day14.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)