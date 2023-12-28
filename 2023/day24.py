from utils.printing import display

example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


with open("day24.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


grid_value = example.split("\n")
# grid_value = s
l_blocks = parse(text=grid_value)
display(x=l_blocks)
