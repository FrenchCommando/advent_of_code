from utils.printing import display


with open("day18.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


cubes = [tuple(map(int, line.split(","))) for line in lines]


def count_edge(i):
    current_cube = cubes[i]
    count = 0
    for cube in cubes[:i]:
        diff = sum(abs(a - b) for a, b in zip(cube, current_cube))
        if diff == 1:
            count += 1
            if count == 6:
                return count
    return count


edge_count = sum(count_edge(i) for i in range(len(cubes)))
print(edge_count)
print(edge_count * 2)
print(len(cubes) * 6 - edge_count * 2)
