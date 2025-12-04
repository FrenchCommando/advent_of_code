from utils.printing import display

example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


with open("day4.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    n = len(p_internal)
    m = len(p_internal[0])

    c = []
    for line in p_internal:
        cc = [
            sum(i == "@" for i in [x0, x1, x2])
            for x0, x1, x2 in zip(line, "." + line[:-1], line[1:] + ".")
        ]
        # print(cc)
        # print(line)
        c.append(cc)

    rolls = []
    for i in range(n):
        for j in range(m):
            r = p_internal[i][j]
            if r == ".":
                continue
            c_top, c_bot, c_mid = 0, 0, 0
            if i > 0:
                c_top = c[i - 1][j]
            if i < n - 1:
                c_bot = c[i + 1][j]
            c_mid = c[i][j]
            c_count = c_top + c_bot + c_mid
            if c_count < 5:
                rolls.append((i, j))
    # print(rolls)
    print(len(rolls))


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()


def get_count2(p_internal):
    n = len(p_internal)
    m = len(p_internal[0])

    full_count = 0

    pp = [ppp for ppp in p_internal]
    while True:
        c = []
        for line in pp:
            cc = [
                sum(i == "@" for i in [x0, x1, x2])
                for x0, x1, x2 in zip(line, "." + line[:-1], line[1:] + ".")
            ]
            # print(cc)
            # print(line)
            c.append(cc)

        pp_new = [[pppp for pppp in ppp] for ppp in pp]
        rolls = []
        for i in range(n):
            for j in range(m):
                r = pp[i][j]
                if r == ".":
                    continue
                c_top, c_bot, c_mid = 0, 0, 0
                if i > 0:
                    c_top = c[i - 1][j]
                if i < n - 1:
                    c_bot = c[i + 1][j]
                c_mid = c[i][j]
                c_count = c_top + c_bot + c_mid
                if c_count < 5:
                    rolls.append((i, j))
                    pp_new[i][j] = "."
        # print(rolls)
        print(len(rolls), end='\t')
        if len(rolls) == 0:
            break
        full_count += len(rolls)
        pp = [''.join(ppp) for ppp in pp_new]
    print(full_count)


get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p)
print()
