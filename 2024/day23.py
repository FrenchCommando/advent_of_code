import re
from utils.printing import display

example = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""



with open("day23.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    connected_to = dict()
    for couple in l:
        left, right = couple.strip().split("-")
        if left not in connected_to:
            connected_to[left] = {right}
        else:
            connected_to[left].add(right)
        if right not in connected_to:
            connected_to[right] = {left}
        else:
            connected_to[right].add(left)

    triple = set()
    for left, connection in connected_to.items():
        for right in connection:
            for node in connected_to[right]:
                if node in connection:
                    triple.add(",".join(sorted((left, right, node))))
    # print(triple)

    triple_with_t = [t for t in triple if any(u.startswith("t") for u in t.split(","))]
    # print(triple_with_t)

    return len(triple_with_t)


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):

    connected_to = dict()
    for couple in l:
        left, right = couple.strip().split("-")
        if left not in connected_to:
            connected_to[left] = {right}
        else:
            connected_to[left].add(right)
        if right not in connected_to:
            connected_to[right] = {left}
        else:
            connected_to[right].add(left)

    connection_count = {k: len(v) for k, v in connected_to.items()}
    print(connection_count)

    count_count = dict()
    for v in connection_count.values():
        if v not in count_count:
            count_count[v] = 1
        else:
            count_count[v] += 1
    print(count_count)
    # looks like it's all the same value
    single_count = list(count_count.keys())[0]
    print("single count", single_count)

    triple = set()
    for left, connection in connected_to.items():
        for right in connection:
            for node in connected_to[right]:
                if node in connection:
                    triple.add(",".join(sorted((left, right, node))))
    big_sets = {3: triple}
    n = 4
    while True:
        previous_sets = big_sets[n-1]
        current_sets = set()
        big_sets[n] = current_sets
        for node, connected in connected_to.items():
            for chosen_set in previous_sets:
                s_set = chosen_set.split(",")
                if node in s_set:
                    continue
                if any(u not in connected for u in s_set):
                    continue
                current_sets.add(",".join(sorted((*s_set, node))))
        print(n, len(current_sets))
        if len(current_sets) == 0:
            break
        n += 1

    return big_sets[n-1]


p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
