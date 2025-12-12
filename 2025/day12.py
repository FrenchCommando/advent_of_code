from utils.printing import display

example = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""


with open("day12.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_best_result(stuff):
    return f"{stuff}100"


def get_count(p_internal):
    blocks = []
    for i in range(6):
        lines = p_internal[i * 5:i * 5 + 5]
        # print(lines)
        # name = lines[0].split(":")
        # not using it
        block = lines[1:-1]
        blocks.append(block)
    print(blocks)

    sizes = [sum(sum(u == "#" for u in line) for line in block) for block in blocks]
    print(sizes)

    regions = []
    for line in p_internal:
        if "x" not in line:
            continue
        dims, numbers = line.split(": ")
        left, right = tuple(map(int, dims.split("x")))
        numbers = list(map(int, numbers.split(" ")))
        regions.append([left, right, numbers])
    print(regions)

    count = 0
    for left, right, numbers in regions:
        print("Reading", left, right, numbers, end="\t")

        area = left * right
        block_size = sum(one * n for one, n in zip(sizes, numbers))

        if block_size <= area:
            print("Success")
            count += 1
    print()
    print(count)
    print()


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)  # example is a red herring
print()
