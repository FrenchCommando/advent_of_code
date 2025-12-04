import itertools

from utils.printing import display


examples = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""


with open("day9.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p_internal):
    graph = dict()

    for p in p_internal:
        cities, distance = p.split(" = ")
        left, right = cities.split(" to ")
        graph[(left, right)] = int(distance)

    print(graph)
    print(len(graph))
    cities_list = list(set(k for u in graph.keys() for k in u ))
    n_cities = len(cities_list)
    print(n_cities, cities_list)

    a_to_b = {city: dict() for city in cities_list}
    for (left, right), distance in graph.items():
        a_to_b[left][right] = distance
        a_to_b[right][left] = distance
    print(a_to_b)

    def path_length(permutation):
        return sum(
            a_to_b[left][right]
            for (left, right) in zip(permutation, permutation[1:])
        )

    shortest = min(path_length(p) for p in itertools.permutations(cities_list))
    longest = max(path_length(p) for p in itertools.permutations(cities_list))
    print(shortest, longest)


get_count(p_internal=[sss.strip() for sss in s])
print()
get_count(p_internal=examples.split("\n"))
print()
