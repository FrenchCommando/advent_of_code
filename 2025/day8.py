import itertools
import operator
from functools import reduce

from utils.printing import display

example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


with open("day8.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal, n):
    contents = []
    for stuff in p_internal:
        t = tuple(map(int, stuff.split(",")))
        contents.append(t)
        # print(stuff, t)

    indices = list(range(len(contents)))

    distances = [
        [
            sum((a - b) * (a - b) for a, b in zip(contents[left], contents[right]))
            for right in indices
        ]
        for left in indices
    ]

    circuits = dict()
    circuit_index = 0
    connected = dict()

    for i in range(n):
        shortest_distance = 1e10
        best_connection = None
        for link in itertools.combinations(indices, 2):
            left, right = link
            if left in connected and right in connected[left]:
                continue
            distance = distances[left][right]
            if distance < shortest_distance:
                shortest_distance = distance
                best_connection = (left, right)
        print(shortest_distance, best_connection, contents[best_connection[0]], contents[best_connection[1]])
        best_left, best_right = best_connection
        if best_left not in connected:
            connected[best_left] = set()
        if best_right not in connected:
            connected[best_right] = set()
        connected[best_left].add(best_right)
        connected[best_right].add(best_left)
        if best_left not in circuits and best_right not in circuits:
            best_circuit = circuit_index
            circuit_index += 1
            circuits[best_left] = best_circuit
            circuits[best_right] = best_circuit
        else:
            best_circuit = circuits.get(best_left, circuits.get(best_right))
            best_circuit2 = circuits.get(best_right, circuits.get(best_left))
            for node in list(circuits.keys()):
                if circuits[node] == best_circuit2:
                    circuits[node] = best_circuit
            circuits[best_left] = best_circuit
            circuits[best_right] = best_circuit

        circuit_sizes = [0 for iii in range(circuit_index)]
        for node, circuit in circuits.items():
            circuit_sizes[circuit] += 1
        print(circuits)
        print(i, sorted(circuit_sizes, reverse=True))
    print(circuits)

    count = reduce(operator.mul, sorted(circuit_sizes)[-3:])
    print(count)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s), n=1000)
print()
get_count(p_internal=p, n=10)
print()


def get_count2(p_internal, n):
    contents = []
    for stuff in p_internal:
        t = tuple(map(int, stuff.split(",")))
        contents.append(t)
        # print(stuff, t)

    indices = list(range(len(contents)))

    distances = [
        [
            sum((a - b) * (a - b) for a, b in zip(contents[left], contents[right]))
            for right in indices
        ]
        for left in indices
    ]

    circuits = dict()
    circuit_index = 0

    while True:
        shortest_distance = 1e10
        best_connection = None
        for link in itertools.combinations(indices, 2):
            left, right = link
            if right in circuits and left in circuits:
                left_circuit = circuits[left]
                right_circuit = circuits[right]
                if left_circuit == right_circuit:
                    continue
            distance = distances[left][right]
            if distance < shortest_distance:
                shortest_distance = distance
                best_connection = (left, right)
        # print(shortest_distance, best_connection, contents[best_connection[0]], contents[best_connection[1]])
        best_left, best_right = best_connection
        if best_left not in circuits and best_right not in circuits:
            best_circuit = circuit_index
            circuit_index += 1
            circuits[best_left] = best_circuit
            circuits[best_right] = best_circuit
        else:
            best_circuit = circuits.get(best_left, circuits.get(best_right))
            best_circuit2 = circuits.get(best_right, circuits.get(best_left))
            for node in list(circuits.keys()):
                if circuits[node] == best_circuit2:
                    circuits[node] = best_circuit
            circuits[best_left] = best_circuit
            circuits[best_right] = best_circuit

        circuit_sizes = [0 for iii in range(circuit_index)]
        for node, circuit in circuits.items():
            circuit_sizes[circuit] += 1
        # print(circuits)
        s_circuits = sorted(circuit_sizes, reverse=True)
        print(s_circuits)
        if s_circuits[0] == len(contents):
            print(best_connection)
            print(contents[best_left], contents[best_right])
            print(contents[best_left][0] * contents[best_right][0])
            break


get_count2(p_internal=parsed(l=s), n=1000)
print()
get_count2(p_internal=p, n=10)
print()
