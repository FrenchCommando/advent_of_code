from utils.printing import display


with open("day24.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)

for line in lines:
    print(line)

nx = len(lines) - 2
ny = len(lines[0]) - 2
print(nx, ny)
print()


def init_mask(symbol):
    return [[lines[i + 1][j + 1] == symbol for j in range(ny)] for i in range(nx)]


def print_mask(mask, symbol):
    for line in mask:
        print(''.join(symbol if value else '.' for value in line))
    print()


right_mask = init_mask(symbol='>')
print_mask(mask=right_mask, symbol='>')
left_mask = init_mask(symbol='<')
print_mask(mask=left_mask, symbol='<')
down_mask = init_mask(symbol='v')
print_mask(mask=down_mask, symbol='v')
up_mask = init_mask(symbol='^')
print_mask(mask=up_mask, symbol='^')


def init_mask_list(symbol):
    mask_list_out = []
    for i in range(nx):
        for j in range(ny):
            if lines[i + 1][j + 1] == symbol:
                mask_list_out.append((i, j))
    return mask_list_out


right_mask_list = init_mask_list(symbol='>')
print(right_mask_list)
left_mask_list = init_mask_list(symbol='<')
print(left_mask_list)
down_mask_list = init_mask_list(symbol='v')
print(down_mask_list)
up_mask_list = init_mask_list(symbol='^')
print(up_mask_list)
print()


def build_mask(period_value):
    occupied = [[False for j in range(ny)] for i in range(nx)]
    for i, j in right_mask_list:
        occupied[i][(j + period_value) % ny] = True
    for i, j in left_mask_list:
        occupied[i][(j - period_value) % ny] = True
    for i, j in down_mask_list:
        occupied[(i + period_value) % nx][j] = True
    for i, j in up_mask_list:
        occupied[(i - period_value) % nx][j] = True
    return occupied


def solve(period_value, start_value, exit_value):
    positions = []
    while True:
        covered = build_mask(period_value=period_value)
        # print_mask(mask=covered, symbol='#')
        positions_candidates = [start_value]
        for position in positions:
            if position[0] != 0:
                positions_candidates.append((position[0] - 1, position[1]))
            if position[0] != nx - 1:
                positions_candidates.append((position[0] + 1, position[1]))
            if position[1] != 0:
                positions_candidates.append((position[0], position[1] - 1))
            if position[1] != ny - 1:
                positions_candidates.append((position[0], position[1] + 1))
            positions_candidates.append(position)
        positions_end = [
            position for position in positions_candidates
            if not covered[position[0]][position[1]]
        ]
        positions = list(set(positions_end))
        # print(period_value, positions)
        period_value += 1
        if exit_value in positions:
            return period_value


start_position = (0, 0)
exit_position = (nx - 1, ny - 1)
period = 0
period = solve(period_value=period, start_value=start_position, exit_value=exit_position)
print(period)
print()
period = solve(period_value=period, start_value=exit_position, exit_value=start_position)
print(period)
print()
period = solve(period_value=period, start_value=start_position, exit_value=exit_position)
print(period)
print()
