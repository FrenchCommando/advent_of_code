from utils.printing import display

example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


with open("day24.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def parse(text):
    blocks = []
    for line in text:
        position, velocity = line.split("@")
        x, y, z = map(int, position.strip().split(","))
        vx, vy, vz = map(int, velocity.strip().split(","))
        blocks.append(dict(x=x, y=y, z=z, vx=vx, vy=vy, vz=vz))
    return blocks


def simplify_one(x, y, vx, vy, x_min, x_max, y_min, y_max):
    if x_min <= x <= x_max and y_min <= y <= y_max:
        if vx < 0:
            right = (x, y)
            y_bar = y - vy / vx * (x - x_min)
            if y_min <= y_bar <= y_max:
                left = (x_min, y_bar)
            elif y_bar < y_min:
                x_bar = x - vx / vy * (y - y_min)
                left = (x_bar, y_min)
            else:
                x_bar = x - vx / vy * (y - y_max)
                left = (x_bar, y_max)
        else:
            left = (x, y)
            y_bar = y - vy / vx * (x - x_max)
            if y_min <= y_bar <= y_max:
                right = (x_max, y_bar)
            elif y_bar < y_min:
                x_bar = x - vx / vy * (y - y_min)
                right = (x_bar, y_min)
            else:
                x_bar = x - vx / vy * (y - y_max)
                right = (x_bar, y_max)
        return left, right
    elif x > x_max:
        if vx > 0:
            return None
        else:
            y_bar = y - vy / vx * (x - x_max)
            if y_min <= y_bar <= y_max:
                return simplify_one(
                    x=x_max, y=y_bar, vx=vx, vy=vy,
                    x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                )
            elif y_bar < y_min:
                x_bar = x - vx / vy * (y - y_min)
                if x_min <= x_bar <= x_max:
                    return simplify_one(
                        x=x_bar, y=y_min, vx=vx, vy=vy,
                        x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                    )
            else:
                x_bar = x - vx / vy * (y - y_max)
                if x_min <= x_bar <= x_max:
                    return simplify_one(
                        x=x_bar, y=y_max, vx=vx, vy=vy,
                        x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                    )
    elif x < x_min:
        if vx < 0:
            return None
        else:
            y_bar = y - vy / vx * (x - x_min)
            if y_min <= y_bar <= y_max:
                return simplify_one(
                    x=x_min, y=y_bar, vx=vx, vy=vy,
                    x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                )
            elif y_bar < y_min:
                x_bar = x - vx / vy * (y - y_min)
                if x_min <= x_bar <= x_max:
                    return simplify_one(
                        x=x_bar, y=y_min, vx=vx, vy=vy,
                        x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                    )
            else:
                x_bar = x - vx / vy * (y - y_max)
                if x_min <= x_bar <= x_max:
                    return simplify_one(
                        x=x_bar, y=y_max, vx=vx, vy=vy,
                        x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                    )
    else:
        out = simplify_one(
            x=y, y=x, vx=vy, vy=vx,
            x_min=y_min, x_max=y_max, y_min=x_min, y_max=x_max,
        )
        if out is None:
            return None
        left, right = out
        if left[-1] <= right[-1]:
            return (left[-1], left[0]), (right[-1], right[0])
        return (right[-1], right[0]), (left[-1], left[0])


def simplify(blocks, x_min, x_max, y_min, y_max):
    simplified = []
    for block in blocks:
        x = block['x']
        y = block['y']
        vx = block['vx']
        vy = block['vy']
        simplified.append(simplify_one(
            x=x, y=y, vx=vx, vy=vy,
            x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
        ))
    return simplified


def has_collision(block0, block1):
    if block0 is None or block1 is None:
        return False
    if block0[0][0] > block1[1][0] or block1[0][0] > block0[1][0]:
        return False
    slope0 = (block0[1][1] - block0[0][1]) / (block0[1][0] - block0[0][0])
    slope1 = (block1[1][1] - block1[0][1]) / (block1[1][0] - block1[0][0])
    left_y0 = block0[0][1]
    left_y1 = block1[0][1]
    if block0[0][0] <= block1[0][0]:
        left_y0 += (block1[0][0] - block0[0][0]) * slope0
    else:
        left_y1 += (block0[0][0] - block1[0][0]) * slope1
    right_y0 = block0[1][1]
    right_y1 = block1[1][1]
    if block0[1][0] > block1[1][0]:
        right_y0 += (block1[1][0] - block0[1][0]) * slope0
    else:
        right_y1 += (block0[1][0] - block1[1][0]) * slope1
    if (right_y1 - right_y0) * (left_y1 - left_y0) >= 0:
        return False
    return True


def collide(simplified):
    count = 0
    for i, block0 in enumerate(simplified):
        for block1 in simplified[i + 1:]:
            # print(block0, block1)
            # print(has_collision(block0, block1))
            if has_collision(block0, block1):
                count += 1
    return count


grid_value, min_value, max_value = example.split("\n"), 7, 27
# grid_value, min_value, max_value = s, 200000000000000, 400000000000000
l_blocks = parse(text=grid_value)
l_simplify = simplify(
    blocks=l_blocks, x_min=min_value, x_max=max_value, y_min=min_value, y_max=max_value,
)
l_collision = collide(simplified=l_simplify)
display(x=l_blocks)
display(x=l_simplify)
display(x=l_collision)
print()


def collide3(block0, block1):
    x0 = block0['x']
    y0 = block0['y']
    z0 = block0['z']
    vx0 = block0['vx']
    vy0 = block0['vy']
    vz0 = block0['vz']
    x1 = block1['x']
    y1 = block1['y']
    z1 = block1['z']
    vx1 = block1['vx']
    vy1 = block1['vy']
    vz1 = block1['vz']


def vector_product(vx0, vy0, vz0, vx1, vy1, vz1):
    z = vx0 * vy1 - vx1 * vy0
    x = vy0 * vz1 - vy1 * vz0
    y = vz0 * vx1 - vz1 * vx0
    return x, y, z


def scalar_product(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]


def is_colinear(vx0, vy0, vz0, vx1, vy1, vz1):
    x, y, z = vector_product(vx0=vx0, vy0=vy0, vz0=vz0, vx1=vx1, vy1=vy1, vz1=vz1)
    print(x, y, z)
    return (x, y, z) == (0, 0, 0)


def find_parallel(blocks):
    for i, block0 in enumerate(blocks):
        vx0 = block0['vx']
        vy0 = block0['vy']
        vz0 = block0['vz']
        for j, block1 in enumerate(blocks):
            if j <= i:
                continue

            vx1 = block1['vx']
            vy1 = block1['vy']
            vz1 = block1['vz']

            if is_colinear(vx0=vx0, vy0=vy0, vz0=vz0, vx1=vx1, vy1=vy1, vz1=vz1):
                # print(i, j, block0, block1)
                return i, j


def solve(blocks):
    # find 2 parallel blocks to define a hyperplane
    # use it to find the time of intersection of other blocks
    # 2 blocks must suffice
    # 3 blocks only should be enough to define the trajectory

    # try:
    #     i, j = find_parallel(blocks=blocks)
    #     print("Found parallel vectors, but still using another method", i, j)
    # except TypeError:
    #     print("No Parallel vectors - try something else")
    # print()

    value = 500000000
    block_index = 78
    block_index_ref = 0

    d_projection2v = dict()
    d_projection1 = dict()
    d_projection2 = dict()
    d_value2 = dict()
    d_value2r = dict()

    # polynomial in 'value'
    # f(x, order 1) | g(x, order 2)
    # for each block

    while True:
        # collision at time 'value' with block0
        block0 = blocks[block_index]
        position0 = (
            block0['x'] + value * block0['vx'],
            block0['y'] + value * block0['vy'],
            block0['z'] + value * block0['vz'],
        )
        if value % 1000000 == 0:
            print("Index Value position", block_index, value, position0)
        # find equation of hyperplane for 2 blocks
        block1 = blocks[block_index_ref]
        position11 = block1['x'], block1['y'], block1['z']
        position12 = (
            block1['x'] + block1['vx'],
            block1['y'] + block1['vy'],
            block1['z'] + block1['vz'],
        )

        tangent1 = vector_product(
            vx0=position0[0] - position11[0],
            vy0=position0[1] - position11[1],
            vz0=position0[2] - position11[2],
            vx1=position11[0] - position12[0],
            vy1=position11[1] - position12[1],
            vz1=position11[2] - position12[2],
        )
        projection1 = scalar_product(v0=tangent1, v1=position11)

        success = True
        for i_block, block2 in enumerate(blocks):
            if i_block == block_index or i_block == block_index_ref:
                continue
            success = False
            position2 = block2['x'], block2['y'], block2['z']
            velocity2 = block2['vx'], block2['vy'], block2['vz']
            projection2 = scalar_product(v0=tangent1, v1=position2)
            projection2v = scalar_product(v0=tangent1, v1=velocity2)
            value2 = (projection1 - projection2) / projection2v
            value2r = (projection1 - projection2) % projection2v
            # print(projection1, projection2, projection2v)
            # print("\t\ti, value2, value2r", i_block, value2, value2r)
            # print("\t\t\tprojection2v", i_block, d_projection2v.get(i_block, 0), projection2v)
            # print("\t\t\tprojection2", i_block, d_projection2.get(i_block, 0), projection2)
            # print("\t\t\tprojection1", i_block, d_projection1.get(i_block, 0), projection1)
            # print("\t\t\t\t\t", i_block, projection2v - d_projection2v.get(i_block, 0))
            # print("\t\t\t\t\t", i_block, projection2 - d_projection2.get(i_block, 0))
            # print("\t\t\t\t\t", i_block, projection1 - d_projection1.get(i_block, 0))
            # print("\t\t\t\t\t", i_block, value2 - d_value2.get(i_block, 0))
            # print("\t\t\t\t\t", i_block, value2r - d_value2r.get(i_block, 0))
            d_projection2v[i_block] = projection2v
            d_projection1[i_block] = projection1
            d_projection2[i_block] = projection2
            d_value2[i_block] = value2
            d_value2r[i_block] = value2r
            # print("\t\t\tposition", position2)
            # print("\t\t\tvelocity", velocity2)
            if value2 <= 0:
                block_index = i_block
                value = 0
                break
                # tangent2 = vector_product(
                #     vx0=position2[0] - position11[0],
                #     vy0=position2[1] - position11[1],
                #     vz0=position2[2] - position11[2],
                #     vx1=position2[0] - position12[0],
                #     vy1=position2[1] - position12[1],
                #     vz1=position2[2] - position12[2],
                # )
                # projection22 = scalar_product(v0=tangent2, v1=position2)
                # projection02 = scalar_product(v0=tangent2, v1=position0)
                # velocity0 = block0['vx'], block0['vy'], block0['vz']
                # projection02v = scalar_product(v0=tangent2, v1=velocity0)
                # value_increment = (projection22 - projection02) / projection02v
                # print("Increment", value, value2, value_increment, projection22, projection02, projection02v)
                # # increment value enough for value2 to be positive
                # if value_increment < -10:
                #     # continue
                #     raise ValueError("ValueIncrement should not be negative")
                # else:
                #     value += int(value_increment)
                #     break
            if value2r != 0:
                break
            success = True
            print(value2, block2)
        if success:
            return block_index, value
        value += 1


# grid_value2 = example.split("\n")
grid_value2 = s
l_blocks2 = parse(text=grid_value2)
l_coordinates = solve(blocks=l_blocks2)
display(x=l_coordinates)
# display(x=sum(l_coordinates[k] for k in ['x', 'y', 'z']))
