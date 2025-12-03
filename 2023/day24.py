import math

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


def vector_norm(vx0, vy0, vz0):
    return math.sqrt(vx0 * vx0 + vy0 * vy0 + vz0 * vz0)


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

    value = 69809585182
    block_index = 78
    block_index_ref = 0

    while True:
        # collision at time 'value' with block0
        block0 = blocks[block_index]
        position0 = (
            block0['x'] + value * block0['vx'],
            block0['y'] + value * block0['vy'],
            block0['z'] + value * block0['vz'],
        )
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

        if value % 1 == 0:
            print("Index Value position", block_index, value, position0)
        if value > 100:
            break  # use next method

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
            print("\t\t\tvalue", i_block, value2, value2r)
            # print("\t\t\tposition", position2)
            # print("\t\t\tvelocity", velocity2)
            if value2 <= 0:
                block_index = i_block
                value = 0
                break
            if value2r != 0:
                break
            success = True
            print(value2, block2)
        if success:
            return block_index, value
        value += 1

    def alignment(value):
        block0 = blocks[block_index]
        position0 = (
            block0['x'] + value * block0['vx'],
            block0['y'] + value * block0['vy'],
            block0['z'] + value * block0['vz'],
        )
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

        location2_i = None
        location2_align = None
        location3_align = None
        for i_block_align, block2_align in enumerate(blocks):
            if i_block_align == block_index or i_block_align == block_index_ref:
                continue
            position2_align = block2_align['x'], block2_align['y'], block2_align['z']
            velocity2_align = block2_align['vx'], block2_align['vy'], block2_align['vz']
            projection2_align = scalar_product(v0=tangent1, v1=position2_align)
            projection2v_align = scalar_product(v0=tangent1, v1=velocity2_align)
            value2_align = (projection1 - projection2_align) / projection2v_align
            location2_align = (
                block2_align['x'] + value2_align * block2_align['vx'] - position0[0],
                block2_align['y'] + value2_align * block2_align['vy'] - position0[1],
                block2_align['z'] + value2_align * block2_align['vz'] - position0[2],
            )
            location2_i = i_block_align
            break
        for i_block_align, block3_align in enumerate(blocks[location2_i + 1:]):
            if i_block_align == block_index or i_block_align == block_index_ref:
                continue
            position3_align = block3_align['x'], block3_align['y'], block3_align['z']
            velocity3_align = block3_align['vx'], block3_align['vy'], block3_align['vz']
            projection3_align = scalar_product(v0=tangent1, v1=position3_align)
            projection3v_align = scalar_product(v0=tangent1, v1=velocity3_align)
            value3_align = (projection1 - projection3_align) / projection3v_align
            location3_align = (
                block3_align['x'] + value3_align * block3_align['vx'] - position0[0],
                block3_align['y'] + value3_align * block3_align['vy'] - position0[1],
                block3_align['z'] + value3_align * block3_align['vz'] - position0[2],
            )
            break

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
            print("\t\t\tvalue", value2, value2r)
            # print("\t\t\tposition", position2)
            # print("\t\t\tvelocity", velocity2)
            if value2 <= 0:
                break
            if value2r != 0:
                break
            success = True
            print(value2, block2)
        if success:
            print("Success", block_index, value)
            raise ValueError(f"{value}")

        alignment_score = scalar_product(v0=vector_product(
            vx0=location2_align[0], vy0=location2_align[1], vz0=location2_align[2],
            vx1=location3_align[0], vy1=location3_align[1], vz1=location3_align[2],
        ), v1=tangent1) / (vector_norm(
            vx0=location2_align[0], vy0=location2_align[1], vz0=location2_align[2],
        ) * vector_norm(
            vx0=location3_align[0], vy0=location3_align[1], vz0=location3_align[2],
        ))
        return abs(alignment_score)

    try:
        low_value = 2
        low_score = alignment(value=low_value)
        high_value = 10000
        high_score = alignment(value=high_value)
        while high_score < low_score:
            low_score = high_score
            high_value *= 2
            high_score = alignment(value=high_value)
        print(low_value, high_value)
        print(low_score, high_score)

        value_count = 1
        while low_value != high_value:
            value_count += 1
            if value_count > 100:
                break
            mid0_value = low_value + (high_value - low_value) // 3
            mid1_value = low_value + (high_value - low_value) * 2 // 3
            mid0_score = alignment(value=mid0_value)
            mid1_score = alignment(value=mid1_value)
            if mid0_score < mid1_score:
                high_value = mid1_value
            else:
                low_value = mid0_value
            print(low_value, mid0_value, mid1_value, high_value)
            print("\t", mid0_score, mid1_score)
        print(low_value, high_value)
        print(mid0_score, mid1_score)
    except ValueError as e:  # raise ValueError for success, bad
        return int(f"{e}")


def solve_value(blocks, value):
    block_index = 78
    block0 = blocks[block_index]
    block0_value = value
    position0 = (
        block0['x'] + value * block0['vx'],
        block0['y'] + value * block0['vy'],
        block0['z'] + value * block0['vz'],
    )
    block1 = blocks[1]
    block1_value = 545820697399
    position1 = (
        block1['x'] + block1_value * block1['vx'],
        block1['y'] + block1_value * block1['vy'],
        block1['z'] + block1_value * block1['vz'],
    )

    d = (
        position1[0] - position0[0],
        position1[1] - position0[1],
        position1[2] - position0[2],
    )
    dt = block1_value - value
    dd = (
        d[0] / dt,
        d[1] / dt,
        d[2] / dt,
    )
    p0 = (
        position0[0] - value * dd[0],
        position0[1] - value * dd[1],
        position0[2] - value * dd[2],
    )
    return dict(
        x=p0[0], y=p0[1], z=p0[2],
    )


# grid_value2 = example.split("\n")
grid_value2 = s
l_blocks2 = parse(text=grid_value2)
l_result_value = solve(blocks=l_blocks2)
l_coordinates = solve_value(blocks=l_blocks2, value=l_result_value)
display(x=l_result_value)
display(x=l_coordinates)
display(x=sum(l_coordinates[k] for k in ['x', 'y', 'z']))
