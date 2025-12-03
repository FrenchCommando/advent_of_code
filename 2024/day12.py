import queue
from utils.printing import display

example = """AAAA
BBCD
BBCC
EEEC"""
example2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
example3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

example4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

example5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""



with open("day12.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    n = len(l)
    m = len(l[0])
    seen = [[False for j in range(m)] for i in range(n)]
    sectors = []

    def first_unseen():
        for i in range(n):
            for j in range(m):
                if not seen[i][j]:
                    return i, j
        return -1, -1

    def neighbours(position):
        for direction, positions_near in dict(
            top=(-1, 0), down=(1, 0),
                left=(0, -1), right=(0, 1),
        ).items():
            candidate = position[0] + positions_near[0], position[-1] + positions_near[-1]
            if 0<=candidate[0]<n and 0<=candidate[-1]<m:
                yield candidate, direction
            else:
                yield None, direction

    def count_zone(i, j):
        q = queue.Queue()
        fence = dict()
        c = l[i][j]

        def compute(position_internal):
            seen[position_internal[0]][position_internal[-1]] = True
            perimeter_internal = []
            for neighbour, direction in neighbours(position_internal):
                if neighbour is None:
                    perimeter_internal.append(direction)
                elif l[neighbour[0]][neighbour[-1]] == c:
                    if neighbour not in fence:
                        q.put(neighbour)
                else:
                    perimeter_internal.append(direction)
            fence[position_internal] = perimeter_internal

        compute(position_internal=(i, j))
        while not q.empty():
            position = q.get()
            if position not in fence:
                compute(position_internal=position)
        return len(fence.keys()), sum(len(perimeter_loop) for perimeter_loop in fence.values())

    while not all(all(line) for line in seen):
        i0, j0 = first_unseen()
        if (i0, j0) != (-1, -1):
            # print("Counting", i0, j0)
            area, perimeter = count_zone(i=i0, j=j0)
            sectors.append((area, perimeter))
            # print(sum(sum(line) for line in seen), n * m, sectors)

    print(sectors)
    return sum(area * perimeter for area, perimeter in sectors)


p = count(l=example.split("\n"))
p2 = count(l=example2.split("\n"))
p3 = count(l=example3.split("\n"))
print("count", p, p2, p3)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    n = len(l)
    m = len(l[0])
    seen = [[False for j in range(m)] for i in range(n)]
    sectors = []

    def first_unseen():
        for i in range(n):
            for j in range(m):
                if not seen[i][j]:
                    return i, j
        return -1, -1

    def neighbours(position):
        for direction, positions_near in dict(
            top=(-1, 0), down=(1, 0),
                left=(0, -1), right=(0, 1),
        ).items():
            candidate = position[0] + positions_near[0], position[-1] + positions_near[-1]
            if 0<=candidate[0]<n and 0<=candidate[-1]<m:
                yield candidate, direction
            else:
                yield None, direction

    def count_zone(i, j):
        q = []
        fence = dict()
        exclusion = dict()
        c = l[i][j]

        def compute(position_internal):
            seen[position_internal[0]][position_internal[-1]] = True

            l_directions = set()
            for neighbour, direction in neighbours(position_internal):
                if neighbour is None:
                    l_directions.add(direction)
                elif l[neighbour[0]][neighbour[-1]] == c:
                    if neighbour not in fence:
                        if neighbour not in q:
                            q.append(neighbour)
                else:
                    l_directions.add(direction)
            fence[position_internal] = [direction for direction in l_directions]

        compute(position_internal=(i, j))
        while len(q) > 0:
            position = q.pop(0)
            if position not in fence:
                compute(position_internal=position)

        for position, fences in fence.items():
            for neighbour, direction in neighbours(position):
                if neighbour is None:
                    continue
                if direction in ["top", "left"]:
                    if neighbour in fence:
                        if position not in exclusion:
                            exclusion[position] = set()
                        for item in fence[neighbour]:
                            exclusion[position].add(item)

        # print(fence)
        # print()
        # for i in range(n):
        #     for j in range(m):
        #         print(i, j, fence.get((i,j), ""), end="\t\t")
        #     print()
        #     for j in range(m):
        #         print(i, j, exclusion.get((i,j), ""), end="\t\t")
        #     print()
        # print()
        # print(fence)
        # print(exclusion)

        return len(fence.keys()), sum(len([d for d in perimeter_loop if d not in exclusion.get(pos, [])]) for pos, perimeter_loop in fence.items())

    while not all(all(line) for line in seen):
        i0, j0 = first_unseen()
        if (i0, j0) != (-1, -1):
            # print("Counting", i0, j0)
            area, perimeter = count_zone(i=i0, j=j0)
            sectors.append((area, perimeter))
            # print(sum(sum(line) for line in seen), n * m, sectors)

    print(sectors)
    return sum(area * perimeter for area, perimeter in sectors)


p2 = count2(l=example.split("\n"))  # 80
p22 = count2(l=example2.split("\n"))  # 436
print("count22", p22)  # 436
p24 = count2(l=example4.split("\n"))  # 236
p25 = count2(l=example5.split("\n"))  # 368
p23 = count2(l=example3.split("\n"))  # 1206
print("count2", p2, p22, p24, p25, p23)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
