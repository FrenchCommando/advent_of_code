import queue
from utils.printing import display


with open("day12.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


# find S
def find_s():
    for i, line in enumerate(lines):
        if "S" in line:
            j = line.index("S")
            return i, j


i_s, j_s = find_s()
display(i_s)
display(j_s)


def solve(q):
    distance = [[-1 for y in range(len(lines[0]))] for x in range(len(lines))]
    for i_ss, j_ss in q:
        distance[i_ss][j_ss] = 0

    while q:
        print(len(q), q)
        i_e, j_e = q.pop(0)
        count = distance[i_e][j_e]
        value = lines[i_e][j_e]
        candidates_to_add = []
        if i_e > 0:
            candidates_to_add.append((i_e - 1, j_e))
        if j_e > 0:
            candidates_to_add.append((i_e, j_e - 1))
        if i_e + 1 < len(lines):
            candidates_to_add.append((i_e + 1, j_e))
        if j_e + 1 < len(lines[0]):
            candidates_to_add.append((i_e, j_e + 1))
        for i_candidate, j_candidate in candidates_to_add:
            if distance[i_candidate][j_candidate] == -1:
                value_candidate = lines[i_candidate][j_candidate]
                if value_candidate == "E":
                    if (value == "z") or (value == "y"):
                        return count + 1
                    else:
                        continue
                if (value == "S" and (value_candidate in ["a", "b"])) or\
                        ((value != "S") and (ord(value) + 1 >= ord(value_candidate))):
                    distance[i_candidate][j_candidate] = count + 1
                    q.append((i_candidate, j_candidate))


def count_e():
    q = [(i_s, j_s)]
    return solve(q=q)


count_for_e = count_e()
display(count_for_e)


def count_a():
    q = []
    for i, line in enumerate(lines):
        if "S" in line:
            j = line.index("S")
            q.append((i, j))
        if 'a' in line:
            for j, c in enumerate(line):
                if c == 'a':
                    q.append((i, j))
    return solve(q=q)


count_for_a = count_a()
display(count_for_a)
