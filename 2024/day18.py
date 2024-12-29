import queue
import re
from utils.printing import display

example = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""



with open("day18.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l, n, k=None):
    failing = []
    for i_line, line in enumerate(l):
        if k is not None:
            if i_line >= k:
                break
        x, y = map(int, line.split(","))
        failing.append((x, y))
    print(len(failing), failing)

    grid = [["." for j in range(n+1)] for i in range(n+1)]

    for x, y in failing:
        grid[x][y] = "#"

    # for l_grid in grid:
    #     print("".join(l_grid))
    # print()

    n_sentinel = 1e50
    c = [[n_sentinel for j in range(n+1)] for i in range(n+1)]
    c[0][0] = 0
    q = queue.Queue()
    q.put((0,0))
    while not q.empty():
        x, y = q.get()
        for xx, yy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if 0 <= xx <= n and 0 <= yy <= n:
                ccc = c[x][y]
                cc = c[xx][yy]
                # print(x,y, xx, yy, cc, ccc)
                if grid[xx][yy] == "#":
                    continue
                if cc > ccc + 1:
                    c[xx][yy] = ccc + 1
                    q.put((xx, yy))

    # for l_c in c:
    #     for l_cc in l_c:
    #         print(l_cc, end="\t")
    #     print()
    # print()

    return c[n][n]


p = count(l=example.split("\n"), n=6, k=12)
print("count", p)
ps = count(l=[line.strip() for line in s], n=70, k=1024)
print("count", ps)


def count2(l, n):
    failing = []
    for i_line, line in enumerate(l):
        fx, fy = map(int, line.split(","))
        failing.append((fx, fy))
    print(len(failing), failing)

    grid = [["." for j in range(n+1)] for i in range(n+1)]

    # for gx, gy in failing:
    #     grid[gx][gy] = "#"

    # for l_grid in grid:
    #     print("".join(l_grid))
    # print()

    def get_path():
        n_sentinel = 1e50
        c = [[n_sentinel for j in range(n+1)] for i in range(n+1)]
        path = [[[] for j in range(n+1)] for i in range(n+1)]
        c[0][0] = 0
        q = queue.Queue()
        q.put((0,0))
        path[0][0] = [(0,0)]
        while not q.empty():
            x, y = q.get()
            for xx, yy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if 0 <= xx <= n and 0 <= yy <= n:
                    ccc = c[x][y]
                    cc = c[xx][yy]
                    if grid[xx][yy] == "#":
                        continue
                    if cc > ccc + 1:
                        c[xx][yy] = ccc + 1
                        q.put((xx, yy))
                        path[xx][yy] = [*path[x][y], (xx, yy)]
        return path[n][n]

    failing_block = None
    main_path = None
    for failing_block in failing:
        gx, gy = failing_block
        grid[gx][gy] = "#"
        if main_path is not None:
            if failing_block not in main_path:
                continue
        main_path = get_path()
        if not main_path:
            break
        print(failing_block, main_path)

    # for l_c in c:
    #     for l_cc in l_c:
    #         print(l_cc, end="\t")
    #     print()
    # print()

    return failing_block


p2 = count2(l=example.split("\n"), n=6)
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s], n=70)
print("count2", ps2)
