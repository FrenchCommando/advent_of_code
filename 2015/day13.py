import itertools
from utils.printing import display


examples = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""


with open("day13.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p_internal):
    graph = dict()
    for p in p_internal:
        left, p1 = p.split(" happiness units by sitting next to ")
        p0, l1 = left.split(" would ")
        direction, value = l1.split(" ")
        value = int(value) * (1 if direction == "gain" else -1)
        graph[(p0, p1[:-1])] = value

    print(graph)

    guests = list(set(u for k in graph.keys() for u in k))

    def evaluate(permutation):
        happiness = 0
        for guest1, guest2 in zip(permutation, permutation[1:] + tuple([permutation[0]])):
            happiness += graph[(guest1, guest2)]
            happiness += graph[(guest2, guest1)]
        return happiness

    largest = max(evaluate(p) for p in itertools.permutations(guests))
    print(largest)


get_count(p_internal=[sss.strip() for sss in s])
print()
get_count(p_internal=[sss.strip() for sss in examples.split("\n")])
print()


def get_count2(p_internal):
    graph = dict()
    for p in p_internal:
        left, p1 = p.split(" happiness units by sitting next to ")
        p0, l1 = left.split(" would ")
        direction, value = l1.split(" ")
        value = int(value) * (1 if direction == "gain" else -1)
        graph[(p0, p1[:-1])] = value

    print(graph)

    guests = list(set(u for k in graph.keys() for u in k))

    def evaluate(permutation):
        happiness = 0
        for guest1, guest2 in zip(permutation, permutation[1:] + tuple([permutation[0]])):
            if guest1 != "me" and guest2 != "me":
                happiness += graph[(guest1, guest2)]
                happiness += graph[(guest2, guest1)]
        return happiness

    guests_plus_me = guests + ["me"]
    largest = max(evaluate(p) for p in itertools.permutations(guests_plus_me))
    print(largest)


get_count2(p_internal=[sss.strip() for sss in s])
print()
get_count2(p_internal=[sss.strip() for sss in examples.split("\n")])
print()

