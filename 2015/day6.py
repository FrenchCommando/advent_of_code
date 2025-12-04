from utils.printing import display


examples = [
    "turn on 0,0 through 999,999",
    "toggle 0,0 through 999,0",
    "turn off 499,499 through 500,500",
]


with open("day6.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p_internal):
    n = 1000
    t = [[False] * n for _ in range(n)]

    for p in p_internal:
        if p.startswith("toggle"):
            sub_p = p[7:]
            fn = 0
        if p.startswith("turn on"):
            sub_p = p[8:]
            fn = 1
        if p.startswith("turn off"):
            sub_p = p[9:]
            fn = 2

        left, right = sub_p.split(" through ")
        # print(p, left, right)
        left_x, left_y = map(int, left.split(","))
        right_x, right_y = map(int, right.split(","))
        a_x, b_x = min(left_x, right_x), max(left_x, right_x)
        a_y, b_y = min(left_y, right_y), max(left_y, right_y)

        for i in range(a_x, b_x + 1):
            for j in range(a_y, b_y + 1):
                if fn == 0:
                    t[i][j] = not t[i][j]
                elif fn == 1:
                    t[i][j] = True
                elif fn == 2:
                    t[i][j] = False

    count = sum(sum(u) for u in t)
    print(count)


get_count(p_internal=[sss.strip() for sss in s])
print()
get_count(p_internal=examples)
print()


examples2 = [
    "turn on 0,0 through 0,0",
    "toggle 0,0 through 999,999",
]

def get_count2(p_internal):
    n = 1000
    t = [[0] * n for _ in range(n)]

    for p in p_internal:
        if p.startswith("toggle"):
            sub_p = p[7:]
            fn = 0
        if p.startswith("turn on"):
            sub_p = p[8:]
            fn = 1
        if p.startswith("turn off"):
            sub_p = p[9:]
            fn = 2

        left, right = sub_p.split(" through ")
        # print(p, left, right)
        left_x, left_y = map(int, left.split(","))
        right_x, right_y = map(int, right.split(","))
        a_x, b_x = min(left_x, right_x), max(left_x, right_x)
        a_y, b_y = min(left_y, right_y), max(left_y, right_y)

        for i in range(a_x, b_x + 1):
            for j in range(a_y, b_y + 1):
                if fn == 0:
                    t[i][j] += 2
                elif fn == 1:
                    t[i][j] += 1
                elif fn == 2:
                    t[i][j] = max(t[i][j] - 1, 0)

    count = sum(sum(u) for u in t)
    print(count)


get_count2(p_internal=[sss.strip() for sss in s])
print()
get_count2(p_internal=examples2)
print()
