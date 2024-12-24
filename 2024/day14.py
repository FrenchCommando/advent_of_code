import re
import time

from utils.printing import display

example = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""



with open("day14.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l, n, a, b):
    problems = []
    for m in re.findall(r"p=(\-?\d+),(\-?\d+) v=(\-?\d+),(\-?\d+)", l):
        problems.append(tuple(map(int, m)))
    # print(problems)
    destination = []
    for problem in problems:
        x = (problem[0] + n * problem[2]) % a
        y = (problem[1] + n * problem[3]) % b
        # print(problem)
        destination.append((x, y))
    counts = [[0, 0], [0, 0]]
    for x, y in destination:
        if x == a // 2 or y == b // 2:
            continue

        qx = (x - 1) // (a // 2) if x != 0 else 0
        qy = (y - 1) // (b // 2) if y != 0 else 0
        # print(qx, qy, x, y, a, b)
        counts[qx][qy] +=1
    print(counts)
    return counts[0][0] * counts[0][1] * counts[1][0] * counts[1][1]


p = count(l=example.replace("\n", ""), n=100, a=11, b=7)
print("count", p)
print()
ps = count(l="".join(s).replace("\n", ""), n=100, a=101, b=103)
print("count", ps)


def count2(l, n, a, b):
    problems = []
    for m in re.findall(r"p=(\-?\d+),(\-?\d+) v=(\-?\d+),(\-?\d+)", l):
        problems.append(tuple(map(int, m)))
    # print(problems)
    while True:
        if n % 10000 == 0:
            print(n)
        destination = []
        for problem in problems:
            x = (problem[0] + n * problem[2]) % a
            y = (problem[1] + n * problem[3]) % b
            # print(problem)
            destination.append((x, y))

        grid = [[0 for j in range(b)] for i in range(a)]
        for x, y in destination:
            grid[x][y] += 1
        k = 34
        cc = [sum(u) for u in grid]
        if any(u > k for u in cc):
            for line in grid[15:53]:  # [-38:]:
                print("".join(map(str, line)).replace("0", " "))
            print(n)
            time.sleep(0.5)
        n += 1


count2(l="".join(s).replace("\n", ""), n=0, a=101, b=103)
