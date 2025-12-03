import copy
import queue

from utils.printing import display

example = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


with open("day22.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def parse(text):
    return [
        tuple(map(lambda x: list(map(int, x.split(","))), line.split("~")))
        for line in text
    ]


def solve(blocks):
    # find my how much in z-dimension each block can fall
    obstacle = dict()  # maps x,y-coordinate to block index
    z_diff = [None for i_block in blocks]
    min_fall_index = dict()
    for i, block in enumerate(blocks):
        z_min = min(block[0][-1], block[1][-1])
        xy_range = [
            (x, y)
            for x in range(min(block[0][0], block[1][0]), max(block[0][0], block[1][0]) + 1)
            for y in range(min(block[0][1], block[1][1]), max(block[0][1], block[1][1]) + 1)
        ]
        min_fall = None
        for xy in xy_range:
            if xy in obstacle:
                obstacle_index_set = obstacle[xy]
                selected_z = None
                obstacle_index = None
                for i_block in obstacle_index_set:
                    z_obstacle = max(blocks[i_block][0][-1], blocks[i_block][1][-1]) - z_diff[i_block]
                    if z_obstacle <= z_min:
                        if z_min == z_obstacle:
                            print(i, block, z_min, z_obstacle, xy, obstacle_index_set, blocks[i_block], z_diff[i_block])
                        if selected_z is None or selected_z < z_obstacle:
                            selected_z = z_obstacle
                            obstacle_index = i_block
                if selected_z is not None:
                    min_fall_candidate = z_min - selected_z - 1
                    if min_fall is None or min_fall_candidate < min_fall:
                        min_fall = min_fall_candidate
                        min_fall_index[i] = {obstacle_index}
                    elif min_fall_candidate == min_fall:
                        min_fall_index[i].add(obstacle_index)
        if min_fall is None:
            min_fall = z_min - 1
        for xy in xy_range:
            if xy not in obstacle:
                obstacle[xy] = {i}
            else:
                obstacle[xy].add(i)
        z_diff[i] = min_fall
    return obstacle, z_diff, min_fall_index


def obstacle_to_support(n, obstacle):
    support = []
    for i in range(n):
        clear = True
        for k, lll in obstacle.items():
            if i in lll:
                if len(lll) == 1:
                    clear = False
        if clear:
            support.append(i)
    return support


def failure(n, obstacle):
    count_failure = []
    for i in range(n):
        dependency = copy.deepcopy(obstacle)
        count = 0
        q = queue.Queue()
        q.put(i)
        while not q.empty():
            index = q.get()
            for j, val in dependency.items():
                if index in val:
                    val.remove(index)
                    if len(val) == 0:
                        count += 1
                        q.put(j)
        count_failure.append(count)
    return count_failure


# grid_value = example.split("\n")
grid_value = s
l_blocks = parse(text=grid_value)
# it's not in sequence - reorder roughly first
l_ordered_blocks_raw = list(sorted(l_blocks, key=lambda x: x[0][-1]))
l_obstacle, l_z_diff, l_min_fall_index = solve(blocks=l_ordered_blocks_raw)
l_support = obstacle_to_support(n=len(l_blocks), obstacle=l_min_fall_index)
l_fail = failure(n=len(l_blocks), obstacle=l_min_fall_index)
display(x=l_blocks)
display(x=l_obstacle)
display(x=l_z_diff)
display(x=l_min_fall_index)
display(x=l_support)
display(x=l_fail)
display(x=sum(l_fail))

# 977 high
# 735 high
# 517 high
# 514 wrong (5 minutes)
# y were not in increasing order
# right answer when putting no range for y - weird - how do I get 509

# 27533 low
# 39077 low
