from utils.printing import display


with open("day14.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)

i_init, j_init = 500, 0
i_s = [int(pos.split(',')[0]) for line in lines for pos in line.split(" -> ")]
j_s = [int(pos.split(',')[-1]) for line in lines for pos in line.split(" -> ")]
i_s.append(i_init)
j_s.append(j_init)

# part 2
j_s.append(max(j_s) + 2)
j_range = max(j_s) - min(j_s)
i_s.append(max(i_s) + j_range)
i_s.append(min(i_s) - j_range)

min_i_s = min(i_s)
min_j_s = min(j_s)
max_i_s = max(i_s)
max_j_s = max(j_s)
print(min(i_s), max(i_s))
print(min(j_s), max(j_s))

rocks = [
    [False for j_rock in range(min(j_s), max(j_s) + 1)]
    for i_rock in range(min(i_s), max(i_s) + 1)
]
sands = [
    [False for j_sand in range(min(j_s), max(j_s) + 1)]
    for i_sand in range(min(i_s), max(i_s) + 1)
]


segments = [(left, right) for line in lines for left, right in zip(line.split(" -> "), line.split(" -> ")[1:])]
print(segments)
segments.append((f"{min_i_s},{max_j_s}", f"{max_i_s},{max_j_s}"))
for left, right in segments:
    i_left = int(left.split(',')[0])
    i_right = int(right.split(',')[0])
    j_left = int(left.split(',')[-1])
    j_right = int(right.split(',')[-1])
    if i_left == i_right:
        j_min, j_max = min(j_left, j_right), max(j_left, j_right)
        for index in range(j_min, j_max + 1):
            rocks[i_left - min_i_s][index - min_j_s] = True
    if j_left == j_right:
        i_min, i_max = min(i_left, i_right), max(i_left, i_right)
        for index in range(i_min, i_max + 1):
            rocks[index - min_i_s][j_left - min_j_s] = True

abyss = False
while not abyss:
    i_current, j_current = i_init, j_init
    if sands[i_current - min_i_s][j_current - min_j_s]:
        abyss = True
        break
    falling = True
    while falling:
        if j_current + 1 > max_j_s:
            abyss = True
            break
        i_candidates = [i_current, i_current - 1, i_current + 1]
        falling = False
        for i_candidate in i_candidates:
            if i_candidate < min_i_s or i_candidate > max_i_s:
                abyss = True
                falling = False
                break
            if sands[i_candidate - min_i_s][j_current + 1 - min_j_s] or \
                    rocks[i_candidate - min_i_s][j_current + 1 - min_j_s]:
                continue
            else:
                i_current, j_current = i_candidate, j_current + 1
                falling = True
                break
    if not abyss:
        sands[i_current - min_i_s][j_current - min_j_s] = True

for rock_line in rocks:
    print("".join("#" if b_rock else "." for b_rock in rock_line))
print()
for sand_line in sands:
    print("".join("#" if b_sand else "." for b_sand in sand_line))
display(sum(sum(rock_line) for rock_line in rocks))
display(sum(sum(sand_line) for sand_line in sands))
