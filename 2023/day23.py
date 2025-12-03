import queue

from utils.printing import display

example = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""


with open("day23.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def solve(text):
    n = len(text)
    m = len(text[0])
    print(n, m)
    n_grid = [[0 if text[i][j] != "#" else "#" for j in range(m)] for i in range(n)]

    source = 0, 1
    target = n - 1, m - 2

    print("Source", source, text[source[0]][source[1]], n_grid[source[0]][source[1]])
    print("Target", target, text[target[0]][target[1]], n_grid[target[0]][target[1]])

    q = queue.Queue()
    q.put((target, "v"))
    # n_grid[target[0]][target[1]] = 0

    def update(x0, y0, x1, y1, orientation0):
        if text[x1][y1] != "#":
            if text[x1][y1] in [".", orientation0]:
                if n_grid[x1][y1] < n_grid[x0][y0] + 1:
                    n_grid[x1][y1] = n_grid[x0][y0] + 1
                    q.put(((x1, y1), orientation0))

    while not q.empty():
        cell, orientation = q.get()
        # print(cell, orientation)
        x, y = cell
        if orientation != "^":
            update(x0=x, y0=y, x1=x - 1, y1=y, orientation0="v")
        if orientation != "v":
            update(x0=x, y0=y, x1=x + 1, y1=y, orientation0="^")
        if orientation != "<":
            update(x0=x, y0=y, x1=x, y1=y - 1, orientation0=">")
        if orientation != ">":
            update(x0=x, y0=y, x1=x, y1=y + 1, orientation0="<")

    for line in n_grid:
        print(line)

    return n_grid[source[0]][source[1]]


def solve2(text):
    n = len(text)
    m = len(text[0])
    print(n, m)
    n_grid = [[False for j in range(m)] for i in range(n)]

    source = 0, 1
    target = n - 1, m - 2

    print("Source", source, text[source[0]][source[1]], n_grid[source[0]][source[1]])
    print("Target", target, text[target[0]][target[1]], n_grid[target[0]][target[1]])

    q = queue.LifoQueue()
    q.put((source, source, 0))
    nodes = [source, target]
    distances = {
        source: dict(),
        target: dict(),
    }
    n_grid[source[0]][source[1]] = True

    def update(x0, y0, origin0, count0):
        if text[x0][y0] != "#":
            if (x0, y0) in nodes:
                if (x0, y0) == origin0:
                    return
                else:
                    q.put(((x0, y0), origin0, count0 + 1))
            else:
                if not n_grid[x0][y0]:
                    q.put(((x0, y0), origin0, count0 + 1))

    def is_node(cell0):
        x0, y0 = cell0
        count0 = 0
        if text[x0 - 1][y0] != "#":
            count0 += 1
        if text[x0 + 1][y0] != "#":
            count0 += 1
        if text[x0][y0 - 1] != "#":
            count0 += 1
        if text[x0][y0 + 1] != "#":
            count0 += 1
        return count0 >= 3

    while not q.empty():
        cell, origin, count = q.get()
        x, y = cell
        n_grid[x][y] = True
        if cell == source:
            update(x0=x + 1, y0=y, origin0=source, count0=0)
            continue
        if cell == target:
            distances[target][origin] = count
            distances[origin][target] = count
            continue
        if is_node(cell0=cell):
            if cell not in nodes:
                nodes.append(cell)
                distances[cell] = dict()
            distances[cell][origin] = count
            distances[origin][cell] = count
            count = 0
            origin = cell
        update(x0=x - 1, y0=y, origin0=origin, count0=count)
        update(x0=x + 1, y0=y, origin0=origin, count0=count)
        update(x0=x, y0=y - 1, origin0=origin, count0=count)
        update(x0=x, y0=y + 1, origin0=origin, count0=count)

    return nodes, distances


def solve2distance(nodes, distances):
    source = nodes[0]
    target = nodes[1]
    print(nodes)
    print("Source", source)
    print("Target", target)
    print()
    for k, v in distances.items():
        print(k, v)
    print()

    largest_count = 0
    q = queue.LifoQueue()
    q.put((0, [source]))
    n_count = 0
    while not q.empty():
        n_count += 1
        count, path = q.get()
        if n_count % 10000 == 0:
            print(q.qsize(), n_count, largest_count, count, path)
        if path[-1] == target:
            # print(count, path)
            largest_count = max(largest_count, count)
            continue
        bound = sum(max(
            distances[n][k] for k in distances[n] if k not in path or k == path[-1]
        ) if len([k for k in distances[n] if k not in path or k == path[-1]]) != 0 else 0
            for n in nodes if n not in path)
        if largest_count > count + bound:
            # print("Bounded", largest_count, count + bound)
            continue
        # else:
        #     print("Not Bounded", largest_count, count + bound)

        current_position = path[-1]
        for k, v in distances[current_position].items():
            if k not in path:
                path0 = [*path, k]
                count0 = count + v
                q.put((count0, path0))
    print(q.qsize(), n_count, largest_count)
    return largest_count


grid_value = example.split("\n")
# grid_value = s
l_solved = solve(text=grid_value)
display(x=l_solved)
l_nodes, l_distances = solve2(text=grid_value)
l_solved2 = solve2distance(nodes=l_nodes, distances=l_distances)
display(x=l_nodes)
display(x=l_distances)
display(x=l_solved2)

# 5630 too low
# 0 1892331 6522
