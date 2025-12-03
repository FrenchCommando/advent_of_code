from utils.printing import display
import queue

example = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

example2 = """111111111111
999999999991
999999999991
999999999991
999999999991"""


with open("day17.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def solve(grid, stride_min, strike_max):
    n = len(grid)
    m = len(grid[0])

    def distance(x_value, y_value):
        return abs(x_value - n + 1) + abs(y_value - m + 1)
    # priority is distance to target

    def is_target(x_value, y_value):
        return distance(x_value=x_value, y_value=y_value) == 0

    def push_item(x_value, y_value, d_value, h_value):
        nonlocal heat_score
        distance_value = distance(x_value=x_value, y_value=y_value)
        if h_value < heat_score:
            if d_value in ["^", "v"]:
                if h_value < heat_score_grid_v[x_value][y_value]:
                    heat_score_grid_v[x_value][y_value] = h_value
                else:
                    return
            else:
                if h_value < heat_score_grid_h[x_value][y_value]:
                    heat_score_grid_h[x_value][y_value] = h_value
                else:
                    return
            if is_target(x_value=x_value, y_value=y_value):
                # print(heat_score, h_value, h)
                heat_score = h_value
                return
            q.put((distance_value, (x_value, y_value, d_value, h_value)))

    def push_next_up(x_value, y_value, h_value):
        for i in range(strike_max):
            x_value -= 1
            if x_value >= 0:
                h_value += int(grid[x_value][y_value])
                if i + 1 >= stride_min:
                    push_item(x_value=x_value, y_value=y_value, d_value="^", h_value=h_value)
            else:
                break

    def push_next_down(x_value, y_value, h_value):
        for i in range(strike_max):
            x_value += 1
            if x_value < n:
                h_value += int(grid[x_value][y_value])
                if i + 1 >= stride_min:
                    push_item(x_value=x_value, y_value=y_value, d_value="v", h_value=h_value)
            else:
                break

    def push_next_left(x_value, y_value, h_value):
        for i in range(strike_max):
            y_value -= 1
            if y_value >= 0:
                h_value += int(grid[x_value][y_value])
                if i + 1 >= stride_min:
                    push_item(x_value=x_value, y_value=y_value, d_value="<", h_value=h_value)
            else:
                break

    def push_next_right(x_value, y_value, h_value):
        for i in range(strike_max):
            y_value += 1
            if y_value < m:
                h_value += int(grid[x_value][y_value])
                if i + 1 >= stride_min:
                    push_item(x_value=x_value, y_value=y_value, d_value=">", h_value=h_value)
            else:
                break

    heat_score = sum(sum(map(int, line)) for line in grid)
    heat_score_grid_v = [[heat_score for j in range(m)] for i in range(n)]
    heat_score_grid_h = [[heat_score for j in range(m)] for i in range(n)]
    q = queue.PriorityQueue()
    push_item(x_value=0, y_value=0, d_value="v", h_value=0)  # only entering costs heat
    push_item(x_value=0, y_value=0, d_value=">", h_value=0)
    index = 0
    while not q.empty():
        score, (x, y, last, h) = q.get()
        if h >= heat_score:
            continue
        if last in ["^", "v"]:
            push_next_left(x_value=x, y_value=y, h_value=h)
            push_next_right(x_value=x, y_value=y, h_value=h)
        else:
            push_next_up(x_value=x, y_value=y, h_value=h)
            push_next_down(x_value=x, y_value=y, h_value=h)
        if index % 1000000 == 0:
            print("Index", index)
            print(score, x, y, last, h, heat_score)
            print("QueueSize", q.qsize())
            # for h_line in heat_score_grid_v:
            #     print(h_line)
            # print()
            # for h_line in heat_score_grid_h:
            #     print(h_line)
            # print()
        index += 1
        # if index == 10000:
        #     raise ValueError()

    return heat_score


# grid_value = example.split("\n")
# grid_value = example2.split("\n")
grid_value = s
l_parsed = solve(grid=grid_value, stride_min=1, strike_max=3)
display(x=l_parsed)
l_parsed2 = solve(grid=grid_value, stride_min=4, strike_max=10)
display(x=l_parsed2)
