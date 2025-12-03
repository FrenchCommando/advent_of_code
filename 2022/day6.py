from utils.printing import display


with open("day6.txt", "r") as f:
    lines = f.readlines()


display(lines)
line = lines[0]
display(line)


def check(subset):
    s = sorted(subset)
    for ii in range(len(s) - 1):
        if s[ii] == s[ii + 1]:
            return False
    return True


marker_length = 4
i = marker_length
while i < len(line):
    subset_value = line[i - marker_length: i]
    # print(subset_value)
    if check(subset_value):
        print(i)
        break
    i += 1

marker_length2 = 14
i = marker_length2
while i < len(line):
    subset_value = line[i - marker_length2: i]
    # print(subset_value)
    if check(subset_value):
        print(i)
        break
    i += 1
