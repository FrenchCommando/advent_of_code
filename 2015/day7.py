from utils.printing import display


examples = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""


with open("day7.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p_internal):
    pending = dict()
    solved = dict()

    def propagate(right):
        for pk in list(pending.keys()):
            if pk not in pending:
                continue
            if right in pk:
                pv = pending[pk]
                if len(pk) == 1:
                    for i in pv:
                        solve(*i)
                else:
                    a, b = pk
                    ppp = a if right == b else b
                    t_ppp = ppp,
                    if t_ppp in pending:
                        pending[t_ppp].extend(pv)
                    else:
                        pending[t_ppp] = pv
                del pending[pk]

    def solve(f0, a1, a2, right):
        if a1.isnumeric():
            v1 = int(a1)
        elif a1 in solved:
            v1 = solved[a1]
        if a2 is not None:
            if a2.isnumeric():
                v2 = int(a2)
            elif a2 in solved:
                v2 = solved[a2]

        if f0 == 0:
            value = v1
        elif f0 == 1:
            value = ~v1 % 65536
        elif f0 == 2:
            value = v1 & v2
        elif f0 == 3:
            value = v1 | v2
        elif f0 == 4:
            value = v1 << v2
        elif f0 == 5:
            value = v1 >> v2
        solved[right] = value
        propagate(right)

    for p in p_internal:
        left, right = p.split(" -> ")
        # print(left, right)

        f0, a1, a2 = None, None, None
        if left.startswith("NOT "):
            v = left[len("NOT "):]
            f0 = 1
            a1 = v
        elif " AND " in left:
            f0 = 2
            a1, a2 = left.split(" AND ")
        elif " OR " in left:
            f0 = 3
            a1, a2 = left.split(" OR ")
        elif " LSHIFT " in left:
            f0 = 4
            a1, a2 = left.split(" LSHIFT ")
        elif " RSHIFT " in left:
            f0 = 5
            a1, a2 = left.split(" RSHIFT ")
        else:
            f0 = 0
            a1 = left

        deps = []
        if a1.isnumeric():
            v1 = int(a1)
        elif a1 in solved:
            v1 = solved[a1]
        else:
            deps.append(a1)
        if a2 is not None:
            if a2.isnumeric():
                v2 = int(a2)
            elif a2 in solved:
                v2 = solved[a2]
            else:
                deps.append(a2)

        if deps:
            t_deps = tuple(deps)
            if t_deps in pending:
                pending[t_deps].append((f0, a1, a2, right))
            else:
                pending[t_deps] = [(f0, a1, a2, right)]
        else:
            # right is solved
            solve(f0, a1, a2, right)

    print(pending)
    # print(solved)
    if 'a' in solved:
        print(solved['a'])


get_count(p_internal=[sss.strip() for sss in s])
print()
get_count(p_internal=[sss.strip() for sss in examples.split("\n")])
print()


def get_count2(p_internal, override_a, override_v):
    pending = dict()
    solved = dict()

    def propagate(right):
        for pk in list(pending.keys()):
            if pk not in pending:
                continue
            if right in pk:
                pv = pending[pk]
                if len(pk) == 1:
                    for i in pv:
                        solve(*i)
                else:
                    a, b = pk
                    ppp = a if right == b else b
                    t_ppp = ppp,
                    if t_ppp in pending:
                        pending[t_ppp].extend(pv)
                    else:
                        pending[t_ppp] = pv
                del pending[pk]

    def solve(f0, a1, a2, right):
        if a1.isnumeric():
            v1 = int(a1)
        elif a1 in solved:
            v1 = solved[a1]
        if a2 is not None:
            if a2.isnumeric():
                v2 = int(a2)
            elif a2 in solved:
                v2 = solved[a2]

        if f0 == 0:
            value = v1
        elif f0 == 1:
            value = ~v1 % 65536
        elif f0 == 2:
            value = v1 & v2
        elif f0 == 3:
            value = v1 | v2
        elif f0 == 4:
            value = v1 << v2
        elif f0 == 5:
            value = v1 >> v2
        solved[right] = value
        propagate(right)

    for p in p_internal:
        left, right = p.split(" -> ")
        # print(left, right)

        if right == override_a:
            solve(0, override_v, None, override_a)
            continue


        f0, a1, a2 = None, None, None
        if left.startswith("NOT "):
            v = left[len("NOT "):]
            f0 = 1
            a1 = v
        elif " AND " in left:
            f0 = 2
            a1, a2 = left.split(" AND ")
        elif " OR " in left:
            f0 = 3
            a1, a2 = left.split(" OR ")
        elif " LSHIFT " in left:
            f0 = 4
            a1, a2 = left.split(" LSHIFT ")
        elif " RSHIFT " in left:
            f0 = 5
            a1, a2 = left.split(" RSHIFT ")
        else:
            f0 = 0
            a1 = left

        deps = []
        if a1.isnumeric():
            v1 = int(a1)
        elif a1 in solved:
            v1 = solved[a1]
        else:
            deps.append(a1)
        if a2 is not None:
            if a2.isnumeric():
                v2 = int(a2)
            elif a2 in solved:
                v2 = solved[a2]
            else:
                deps.append(a2)

        if deps:
            t_deps = tuple(deps)
            if t_deps in pending:
                pending[t_deps].append((f0, a1, a2, right))
            else:
                pending[t_deps] = [(f0, a1, a2, right)]
        else:
            # right is solved
            solve(f0, a1, a2, right)

    print(pending)
    # print(solved)
    if 'a' in solved:
        print(solved['a'])


get_count2(
    p_internal=[sss.strip() for sss in s],
    override_a='b', override_v='46065',
)
print()
