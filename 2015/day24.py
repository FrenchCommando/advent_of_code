import itertools
import operator
from functools import reduce
from utils.printing import display


with open("day24.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p, n_groups):
    packages = tuple(map(int, p))
    print(packages)

    full_weight = sum(packages)
    weight_per_group = full_weight // n_groups
    print(weight_per_group, full_weight, n_groups * weight_per_group)

    k = 1
    g1 = []
    while not g1:
        for g in itertools.combinations(packages, k):
            if sum(g) == weight_per_group:
                g1.append(g)
        k += 1
    print(g1)

    best_q = 1e20
    for g in g1:
        q_value = reduce(operator.mul, g)
        if q_value < best_q:
            best_q = q_value
    print(best_q)



get_count(p=[int(sss.strip()) for sss in s], n_groups=3)
print()
get_count(p=list(itertools.chain(range(1, 6), range(7, 12))), n_groups=3)
print()

get_count(p=[int(sss.strip()) for sss in s], n_groups=4)
print()
get_count(p=list(itertools.chain(range(1, 6), range(7, 12))), n_groups=4)
print()
