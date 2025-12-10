import itertools
from utils.printing import display


example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


with open("day9.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    contents = []
    for stuff in p_internal:
        contents.append(tuple(map(int, stuff.split(','))))
    print(contents)
    best_rectangle = 0
    for left, right in itertools.combinations(contents, 2):
        x_left, y_left = left
        x_right, y_right = right
        value = (abs(x_left - x_right) + 1) * (abs(y_left - y_right) + 1)
        if value > best_rectangle:
            best_rectangle = value

    print(best_rectangle)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()


def get_count2(p_internal):
    contents = []
    for stuff in p_internal:
        contents.append(tuple(map(int, stuff.split(','))))
    print(contents)

    min_x = min(u[0] for u in contents)
    min_y = min(u[1] for u in contents if u[0] == min_x)
    print(min_x, min_y)
    min_index = contents.index((min_x, min_y))
    print(min_index, contents[min_index], len(contents))

    borders = dict()

    orientation = None
    for left, right in zip(
            contents[min_index:] + contents[:min_index],
            contents[min_index + 1:] + contents[:min_index + 1],
    ):
        x_left, y_left = left
        x_right, y_right = right
        if x_left == x_right:
            # print("Same X", left, right)
            if y_left < y_right:
                # print("Y increasing")
                if orientation is None:
                    orientation = "R"
                    # print(f"Orientation set {orientation}")
                x_direction = +1 if orientation == "R" else -1
            else:
                x_direction = -1 if orientation == "R" else +1
            y_min, y_max = min(y_left, y_right), max(y_left, y_right)
            for y in range(y_min, y_max + 1):
                c = (x_left, y)
                if c not in borders:
                    borders[c] = []
                borders[c].append((x_direction, 0))
        elif y_left == y_right:
            # print("Same Y", left, right)

            if x_left < x_right:
                # print("X increasing")
                if orientation is None:
                    orientation = "L"
                    # print(f"Orientation set {orientation}")
                y_direction = +1 if orientation == "L" else -1
            else:
                y_direction = -1 if orientation == "L" else +1
            x_min, x_max = min(x_left, x_right), max(x_left, x_right)
            for x in range(x_min, x_max + 1):
                c = (x, y_left)
                if c not in borders:
                    borders[c] = []
                borders[c].append((0, y_direction))
        else:
            raise ValueError(f"Bad coordinates {left, right}")
    # print(len(borders), borders)

    bad_corners = set()
    for c, d in borders.items():
        if len(d) == 2:
            clear = True
            for x, y in d:
                c_back = c[0] - x, c[1] - y
                if c_back not in borders:
                    clear = False
            if not clear:
                bad_corners.add(c)
    # print(len(bad_corners), bad_corners)

    best_rectangle = 0
    for left, right in itertools.combinations(contents, 2):
    #     print(left, right, borders[left], borders[right], left in bad_corners, right in bad_corners)
        x_left, y_left = left
        x_right, y_right = right

        value = (abs(x_left - x_right) + 1) * (abs(y_left - y_right) + 1)
        if value < best_rectangle:
            continue

        clear = True

        if left in bad_corners:
            for d in borders[left]:
                d_x, d_y = d
                if d_x * (x_right - x_left) < 0:
                    clear = False
                    break
                if d_y * (y_right - y_left) < 0:
                    clear = False
                    break
        if right in bad_corners:
            for d in borders[right]:
                d_x, d_y = d
                if d_x * (x_left - x_right) < 0:
                    clear = False
                    break
                if d_y * (y_left - y_right) < 0:
                    clear = False
                    break
        if not clear:
            continue

        x_min, x_max = min(x_left, x_right), max(x_left, x_right)
        y_min, y_max = min(y_left, y_right), max(y_left, y_right)

        for x in range(x_min + 1, x_max + 1 - 1):
            c_min = (x, y_min)
            c_max = (x, y_max)
            if c_min in bad_corners:
                clear = False
                break
            if c_max in bad_corners:
                clear = False
                break
            if c_min in borders:
                b_c_min = borders[c_min]
                if len(b_c_min) == 1:
                    if (0, 1) not in b_c_min:
                        clear = False
                        break
            if c_max in borders:
                b_c_max = borders[c_max]
                if len(b_c_max) == 1:
                    if (0, -1) not in b_c_max:
                        clear = False
                        break
        if not clear:
            continue
        for y in range(y_min + 1, y_max + 1 - 1):
            c_min = (x_min, y)
            c_max = (x_max, y)

            if c_min in bad_corners:
                clear = False
                break
            if c_max in bad_corners:
                clear = False
                break

            if c_min in borders:
                b_c_min = borders[c_min]
                if len(b_c_min) == 1:
                    if (1, 0) not in b_c_min:
                        clear = False
                        break
            if c_max in borders:
                b_c_max = borders[c_max]
                if len(b_c_max) == 1:
                    if (-1, 0) not in b_c_max:
                        clear = False
                        break
        if not clear:
            continue

        # for c in [(x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)]:
        #     print("List", c, borders.get(c, None), c in bad_corners)
        #
        # for x in range(x_min + 1, x_max + 1 - 1):
        #     c_min = (x, y_min)
        #     if c_min in borders:
        #         print("CMinX", x, borders[c_min], c_min in bad_corners)
        # for x in range(x_min + 1, x_max + 1 - 1):
        #     c_max = (x, y_max)
        #     if c_max in borders:
        #         print("CMaxX", x, borders[c_max], c_max in bad_corners)
        # for y in range(y_min + 1, y_max + 1 - 1):
        #     c_min = (x_min, y)
        #     if c_min in borders:
        #         print("CMinY", y, borders[c_min], c_min in bad_corners)
        # for y in range(y_min + 1, y_max + 1 - 1):
        #     c_max = (x_max, y)
        #     if c_max in borders:
        #         print("CMaxY", y, borders[c_max], c_max in bad_corners)

        print(left, right, value, best_rectangle)
        best_rectangle = value
    print(best_rectangle)


get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p)
print()
