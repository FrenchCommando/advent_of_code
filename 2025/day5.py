from utils.printing import display

example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


with open("day5.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    ranges = []
    stuffs = []
    for line in p_internal:
        if "-" in line:
            ranges.append(list(map(int, line.split("-"))))
        if line.isnumeric():
            stuffs.append(int(line))

    count = 0
    for stuff in stuffs:
        for left, right in ranges:
            if left <= stuff <= right:
                count += 1
                break

    print(count)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()


def get_count2(p_internal):
    ranges = []
    for line in p_internal:
        if "-" in line:
            ranges.append(list(map(int, line.split("-"))))

    has_overlaps = True
    while has_overlaps:
        has_overlaps = False
        for i1, (left, right) in enumerate(ranges):
            for i2, (left2, right2) in enumerate(ranges):
                if i1 == i2:
                    continue
                if left2 <= left <= right2:
                    has_overlaps = True
                    if left2 <= right <= right2:
                        ranges.pop(i1)
                    else:
                        ranges[i1] = right2 + 1, right
                    break
            if has_overlaps:
                break

    count = 0
    for left, right in ranges:
        count += right - left + 1

    print(count)


get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p)
print()
