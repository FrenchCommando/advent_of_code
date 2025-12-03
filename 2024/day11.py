from utils.printing import display

example = """125 17"""



with open("day11.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l, n=25):
    stones = list(map(int, l.split(" ")))
    # print("stones", stones)
    for i in range(n):
        modified = []
        for stone in stones:
            if stone == 0:
                modified.append(1)
            else:
                s_stone = str(stone)
                if len(s_stone) % 2 == 0:
                    modified.append(int(s_stone[:len(s_stone) // 2]))
                    modified.append(int(s_stone[len(s_stone) // 2:]))
                else:
                    modified.append(stone * 2024)
        stones = modified
        # print(i, len(stones))

    return len(stones)



p6 = count(l=example, n=6)
p25 = count(l=example, n=25)
print("count", p6, p25)
ps = count(l=s[0].strip(), n=25)
print("count", ps)
# ps2 = count(l=s[0].strip(), n=75)
# print("count", ps2)


def count2(l, n=25):
    stones = list(map(int, l.split(" ")))
    results = dict()

    def projection(stone, steps):
        if (stone, steps) in results:
            return results[(stone, steps)]
        if steps == 0:
            res = 1
        else:
            if stone == 0:
                res = projection(1, steps-1)
            else:
                s_stone = str(stone)
                if len(s_stone) % 2 == 0:
                    res = projection(int(s_stone[:len(s_stone) // 2]), steps-1) + projection(int(s_stone[len(s_stone) // 2:]), steps-1)
                else:
                    res = projection(stone * 2024, steps-1)
        results[(stone, steps)] = res
        return res
    projected = [projection(stone, n) for stone in stones]
    print(projected)
    return sum(projected)

p6 = count2(l=example, n=6)
p25 = count2(l=example, n=25)
print("count2", p6, p25)
p2 = count2(l=example, n=75)
print("count2", p2)
ps225 = count2(l=s[0].strip(), n=25)
ps275 = count2(l=s[0].strip(), n=75)
print("count2", ps225, ps275)
