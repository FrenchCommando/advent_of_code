from utils.printing import display


with open("day18.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


cubes = [tuple(map(int, line.split(","))) for line in lines]


def count_edge(i, l_cubes):
    current_cube = l_cubes[i]
    count = 0
    for cube in l_cubes[:i]:
        diff = sum(abs(a - b) for a, b in zip(cube, current_cube))
        if diff == 1:
            count += 1
            if count == 6:
                return count
    return count


edge_count = sum(count_edge(i, cubes) for i in range(len(cubes)))
print(edge_count)
print(edge_count * 2)
print(len(cubes) * 6 - edge_count * 2)


x_min = min(a[0] for a in cubes)
x_max = max(a[0] for a in cubes)
y_min = min(a[1] for a in cubes)
y_max = max(a[1] for a in cubes)
z_min = min(a[2] for a in cubes)
z_max = max(a[2] for a in cubes)

x_size = x_max - x_min + 1
y_size = y_max - y_min + 1
z_size = z_max - z_min + 1

print(f"Dimensions {x_min} {x_max} : {x_size}\t\t{y_min} {y_max} : {y_size}\t\t{z_min} {z_max} : {z_size}")


propagated = [[[False for z in range(z_size)] for y in range(y_size)] for x in range(x_size)]

propagating = set()

pre_other_cubes = [
    (x + x_min, y + y_min, z + z_min) for z in range(z_size) for y in range(y_size) for x in range(x_size) if not propagated[x][y][z]
]
print("pre", pre_other_cubes)

for x in range(x_size):
    for y in range(y_size):
        if (x + x_min, y + y_min, 0 + z_min) not in cubes:
            propagated[x][y][0] = True
            propagating.add((x, y, 0))
        if (x + x_min, y + y_min, z_size - 1 + z_min) not in cubes:
            propagated[x][y][z_size - 1] = True
            propagating.add((x, y, z_size - 1))

pre_other_cubes = [
    (x + x_min, y + y_min, z + z_min) for z in range(z_size) for y in range(y_size) for x in range(x_size) if not propagated[x][y][z]
]
print("pre", pre_other_cubes)

for x in range(x_size):
    for z in range(z_size):
        if (x + x_min, 0 + y_min, z + z_min) not in cubes:
            propagated[x][0][z] = True
            propagating.add((x, 0, z))
        if (x + x_min, y_size - 1 + y_min, z + z_min) not in cubes:
            propagated[x][y_size - 1][z] = True
            propagating.add((x, y_size - 1, z))

pre_other_cubes = [
    (x + x_min, y + y_min, z + z_min) for z in range(z_size) for y in range(y_size) for x in range(x_size) if not propagated[x][y][z]
]
print("pre", pre_other_cubes)

for z in range(z_size):
    for y in range(y_size):
        if (0 + x_min, y + y_min, z + z_min) not in cubes:
            propagated[0][y][z] = True
            propagating.add((0, y, z))
        if (x_size - 1 + x_min, y + y_min, z + z_min) not in cubes:
            propagated[x_size - 1][y][z] = True
            propagating.add((x_size - 1, y, z))

print("cubes", cubes)

pre_other_cubes = [
    (x + x_min, y + y_min, z + z_min) for z in range(z_size) for y in range(y_size) for x in range(x_size) if not propagated[x][y][z]
]
print("pre", pre_other_cubes)

while len(propagating) != 0:
    (x, y, z) = propagating.pop()
    l_propagating = [
        (x, y, z - 1),
        (x, y, z + 1),
        (x, y - 1, z),
        (x, y + 1, z),
        (x - 1, y, z),
        (x + 1, y, z),
    ]
    for (xx, yy, zz) in l_propagating:
        if 0 <= xx < x_size and 0 <= yy < y_size and 0 <= zz < z_size:
            if not propagated[xx][yy][zz]:
                if (xx + x_min, yy + y_min, zz + z_min) not in cubes:
                    propagated[xx][yy][zz] = True
                    if (xx, yy, zz) not in propagating:
                        propagating.add((xx, yy, zz))

other_cubes = [
    (x, y, z) for z in range(z_size) for y in range(y_size) for x in range(x_size) if not propagated[x][y][z]
]
print("post", other_cubes)
edge_other_count = sum(count_edge(i, other_cubes) for i in range(len(other_cubes)))
print(edge_other_count)
print(edge_other_count * 2)
print(len(other_cubes) * 6 - edge_other_count * 2)
