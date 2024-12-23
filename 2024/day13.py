import re
from utils.printing import display

example = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""



with open("day13.txt", "r") as f:
    s = f.readlines()
    display(s)


def bezout(a, b):
    q = []
    i, j = a, b
    while i > 0 and j > 0:
        if i > j:
            q.append(i // j)
            i, j = i % j, j
        else:
            q.append(j // i)
            i, j = i, j % i
        # print(i, j, q)

    if i < j:
        ni, nj = 0, 1
        d = j
    else:
        ni, nj = 1, 0
        d = i

    # print(d, i, j, ni, nj, ni * i + nj * j)

    for qq in reversed(q):
        if i < j:
            i = qq * j + i
            ni, nj = ni, nj - ni * qq
        else:
            j = qq * i + j
            ni, nj = ni - nj * qq, nj
        # print(d, i, j, ni, nj, ni * i + nj * j)

    return d, ni, nj

def solve(a, b, c):
    d, na, nb = bezout(a=a, b=b)
    # print(d, na, nb, a, b)
    if c % d != 0:
        return None, None
    dc = c // d
    r_na = na * dc
    r_nb = nb * dc

    return r_na, r_nb

def count(l):
    problems = []
    for m in re.findall(r"Button A: X\+(\d+), Y\+(\d+)Button B: X\+(\d+), Y\+(\d+)Prize: X=(\d+), Y=(\d+)", l):
        problems.append(tuple(map(int, m)))
    # print(problems)
    result = []
    for problem in problems:
        ax, bx = solve(a=problem[0], b=problem[2], c=problem[4])
        ay, by = solve(a=problem[1], b=problem[3], c=problem[5])
        if ax is None or ay is None:
            continue

        # print(ax, bx)
        # print(ay, by)
        # ax * problem[0] + bx * problem[2] = problem[4]
        # print(ax * problem[0] + bx * problem[2], problem[4])
        # ay * problem[1] + by * problem[3] = problem[5]
        # print(ay * problem[1] + by * problem[3], problem[5])
        # ux, uy:
        # ax -> ax0 + ux * problem[2]
        # bx -> bx0 - ux * problem[0]
        # ay -> ay0 + uy * problem[3]
        # by -> by0 - uy * problem[1]
        # reach: ax = ay, bx = by
        # ax0 + ux * problem[2] = ay0 + uy * problem[3]
        # bx0 - ux * problem[0] = by0 - uy * problem[1]
        # ux * problem[2] - uy * problem[3] = ay0 - ax0
        # - ux * problem[0] + uy * problem[1] = by0 - bx0
        determinant = problem[2] * problem[1] - problem[3] * problem[0]
        if determinant == 0:
            print(problem)
            continue
        # ux = ((ay - ax) * problem[1] + (by - bx) * problem[3]) / determinant
        # uy = ((ay - ax) * problem[0] + (by - bx) * problem[2]) / determinant
        # print(ux, uy)
        # ax += ux * problem[2]
        # bx -= ux * problem[0]
        # ay += uy * problem[3]
        # by -= uy * problem[1]

        # ux = ((ay - ax) * problem[1] + (by - bx) * problem[3]) / determinant
        # uy = ((ay - ax) * problem[0] + (by - bx) * problem[2]) / determinant
        # print(ux, uy)
        dax = (problem[2] * ((ay - ax) * problem[1] + (by - bx) * problem[3])) / determinant
        dbx = (problem[0] * ((ay - ax) * problem[1] + (by - bx) * problem[3])) / determinant
        day = (problem[3] * ((ay - ax) * problem[0] + (by - bx) * problem[2])) / determinant
        dby = (problem[1] * ((ay - ax) * problem[0] + (by - bx) * problem[2])) / determinant
        ax += dax
        bx -= dbx
        ay += day
        by -= dby
        # print(problem)
        # print(ax, bx)
        # print(ay, by)
        # ax * problem[0] + bx * problem[2] = problem[4]
        # print(ax * problem[0] + bx * problem[2], problem[4])
        # ay * problem[1] + by * problem[3] = problem[5]
        # print(ay * problem[1] + by * problem[3], problem[5])
        # print()


        # print(nx, ny, dx, dy)
        if ax == ay and bx == by:
            if int(ax) != ax or int(by) != by:
                continue
            # if ax > 100 or bx > 100:
            #     continue
            # if ax < 0 or bx < 0:
            #     continue
            # print(ax, bx, ax * 3 + by)
            result.append(ax * 3 + by)
    print(result)
    return sum(result)


p = count(l=example.replace("\n", ""))
print("count", p)
print()
ps = count(l="".join(s).replace("\n", ""))
print("count", ps)


def count2(l):
    problems = []
    for m in re.findall(r"Button A: X\+(\d+), Y\+(\d+)Button B: X\+(\d+), Y\+(\d+)Prize: X=(\d+), Y=(\d+)", l):
        problems.append(tuple(map(int, m)))
    # print(problems)
    result = []
    for problem in problems:
        d_target = 10000000000000
        ax, bx = solve(a=problem[0], b=problem[2], c=problem[4] + d_target)
        ay, by = solve(a=problem[1], b=problem[3], c=problem[5] + d_target)
        if ax is None or ay is None:
            continue

        # print(ax, bx)
        # print(ay, by)
        # ax * problem[0] + bx * problem[2] = problem[4]
        # print(ax * problem[0] + bx * problem[2], problem[4])
        # ay * problem[1] + by * problem[3] = problem[5]
        # print(ay * problem[1] + by * problem[3], problem[5])
        # ux, uy:
        # ax -> ax0 + ux * problem[2]
        # bx -> bx0 - ux * problem[0]
        # ay -> ay0 + uy * problem[3]
        # by -> by0 - uy * problem[1]
        # reach: ax = ay, bx = by
        # ax0 + ux * problem[2] = ay0 + uy * problem[3]
        # bx0 - ux * problem[0] = by0 - uy * problem[1]
        # ux * problem[2] - uy * problem[3] = ay0 - ax0
        # - ux * problem[0] + uy * problem[1] = by0 - bx0
        determinant = problem[2] * problem[1] - problem[3] * problem[0]
        if determinant == 0:
            print(problem)
            continue
        # ux = ((ay - ax) * problem[1] + (by - bx) * problem[3]) / determinant
        # uy = ((ay - ax) * problem[0] + (by - bx) * problem[2]) / determinant
        # print(ux, uy)
        # ax += ux * problem[2]
        # bx -= ux * problem[0]
        # ay += uy * problem[3]
        # by -= uy * problem[1]

        # ux = ((ay - ax) * problem[1] + (by - bx) * problem[3]) / determinant
        # uy = ((ay - ax) * problem[0] + (by - bx) * problem[2]) / determinant
        # print(ux, uy)
        dax = (problem[2] * ((ay - ax) * problem[1] + (by - bx) * problem[3])) / determinant
        dbx = (problem[0] * ((ay - ax) * problem[1] + (by - bx) * problem[3])) / determinant
        day = (problem[3] * ((ay - ax) * problem[0] + (by - bx) * problem[2])) / determinant
        dby = (problem[1] * ((ay - ax) * problem[0] + (by - bx) * problem[2])) / determinant
        ax += dax
        bx -= dbx
        ay += day
        by -= dby
        # print(problem)
        # print(ax, bx)
        # print(ay, by)
        # ax * problem[0] + bx * problem[2] = problem[4]
        # print(ax * problem[0] + bx * problem[2], problem[4])
        # ay * problem[1] + by * problem[3] = problem[5]
        # print(ay * problem[1] + by * problem[3], problem[5])
        # print()


        # print(nx, ny, dx, dy)
        if ax == ay and bx == by:
            if int(ax) != ax or int(by) != by:
                continue
            # if ax > 100 or bx > 100:
            #     continue
            # if ax < 0 or bx < 0:
            #     continue
            # print(ax, bx, ax * 3 + by)
            result.append(ax * 3 + by)
    print(result)
    return sum(result)


p2 = count2(l=example.replace("\n", ""))
print("count2", p2)
print()
ps2 = count2(l="".join(s).replace("\n", ""))
print("count2", ps2)
