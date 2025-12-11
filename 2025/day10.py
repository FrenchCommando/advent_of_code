import asyncio
import itertools
import queue
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import reduce

from utils.printing import display

example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


with open("day10.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def line_to_data(stuff):
    line = stuff.split(" ")
    lights = line[0][1:-1]
    buttons = [tuple(map(int, u[1:-1].split(","))) for u in line[1:-1]]
    joltage = tuple(map(int, line[-1][1:-1].split(",")))
    return lights, buttons, joltage


def convert_binary(item):
    return sum(1 << i for i in item)


def get_best_result(stuff):
    lights, buttons, joltage = line_to_data(stuff=stuff)
    b_light = convert_binary(item=[i for i, c in enumerate(lights) if c == "#"])
    b_button = [convert_binary(item=item) for item in buttons]
    print(b_light, b_button)

    k = 0
    while k <= len(b_button):
        for c in itertools.combinations(b_button, k):
            # print(c)
            result = reduce(lambda x, y: x ^ y, c, 0)
            if result == b_light:
                print([bin(u) for u in c])
                return k
        k += 1
    return None


def get_count(p_internal):
    contents = []
    for stuff in p_internal:
        best_result = get_best_result(stuff=stuff)
        contents.append(best_result)
        print(stuff)
        print(best_result)
        print()
    count = sum(contents)
    print(count)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()


def candidates_q(t, buttons, l_set_bits):
    non_zeros = [i for i, tt in enumerate(t) if tt != 0]
    optimal_non_zero = min(non_zeros, key=lambda i: l_set_bits[i])
    # optimal_non_zero = min(non_zeros, key=lambda i: 100 * l_set_bits[i] + t[i])
    # optimal_non_zero = min(non_zeros, key=lambda i: (l_set_bits[i], t[i]))
    # optimal_non_zero = min(non_zeros, key=lambda i: t[i])
    # optimal_non_zero = max(non_zeros, key=lambda i: t[i])
    # optimal_non_zero = non_zeros[max(0, min(len(non_zeros) - 1, 2))]

    qq = queue.LifoQueue()
    qq.put((0, t))

    clean_bit_to_set = [u for u in buttons if all(z in non_zeros for z in u) and (optimal_non_zero in u)]
    if len(clean_bit_to_set) == 0:
        return qq, optimal_non_zero
    # if len(non_zeros) > len(t) - 2:
    #     print("\t\t\t", optimal_non_zero, non_zeros, t, clean_bit_to_set)

    i_last = len(clean_bit_to_set) - 1
    for i_button, button in enumerate(clean_bit_to_set):
        # print(button, qq.qsize(), len(clean_bit_to_set))
        qqq = queue.LifoQueue()
        while not qq.empty():
            c, tt = qq.get()
            number = 0
            if i_button == i_last:
                number = tt[optimal_non_zero]
            while True:
                bad = False
                t_b = list(tt)
                for i in button:
                    t_b[i] = t_b[i] - number
                    if t_b[i] < 0:
                        bad = True
                        break
                if bad:
                    break
                t_t_b = tuple(t_b)
                qqq.put((c + number, t_t_b))
                number += 1
        qq = qqq
    return qq, optimal_non_zero


def get_best_result2(stuff):
    lights, buttons, joltage = line_to_data(stuff=stuff)
    # print(buttons, joltage)

    l_joltage = max(u for b in buttons for u in b) + 1
    l_set_bits = [0 for u in range(l_joltage)]
    for u in buttons:
        for b in u:
            l_set_bits[b] = l_set_bits[b] + 1

    best_right = dict()
    best_solution = None
    qq, optimal_non_zero = candidates_q(t=joltage, buttons=buttons, l_set_bits=l_set_bits)
    while not qq.empty():
        c_b, t_t_b = qq.get()
        if t_t_b in best_right and best_right[t_t_b] <= c_b:
            continue

        if all(u == 0 for u in t_t_b):
            if best_solution is None:
                best_solution = c_b
            best_solution = min(c_b, best_solution)
            # print("Best", best_solution)
            continue
        best_right[t_t_b] = c_b

    other_buttons = sorted([b for b in buttons if optimal_non_zero not in b], key=len, reverse=False)
    print(f"{other_buttons=}")

    best_left = {tuple(0 for _ in joltage): 0}

    for b in other_buttons:
        print(f"\t{b=} - {len(best_left)=} - {len(best_right)=}")
        if len(best_left) < len(best_right):
            for bb in list(best_left.keys()):
                cc = best_left[bb]
                if best_solution is not None:
                    if cc >= best_solution:
                        continue

                number = 1
                while True:
                    bad = False
                    t_b = list(bb)
                    for i in b:
                        t_b[i] = t_b[i] + number
                        if t_b[i] > joltage[i]:
                            bad = True
                            break
                    if bad:
                        break
                    t_t_b = tuple(t_b)
                    if t_t_b not in best_left:
                        best_left[t_t_b] = cc + number
                    best_left[t_t_b] = min(cc + number, best_left[t_t_b])

                    if t_t_b in best_right:
                        c_left = best_left[t_t_b]
                        c_right = best_right[t_t_b]
                        c_full = c_right + c_left
                        if best_solution is None:
                            best_solution = c_full
                        best_solution = min(c_full, best_solution)
                        print("Best", best_solution)

                    number += 1
        else:
            for bb in list(best_right.keys()):
                cc = best_right[bb]
                if best_solution is not None:
                    if cc >= best_solution:
                        continue

                number = 1
                while True:
                    bad = False
                    t_b = list(bb)
                    for i in b:
                        t_b[i] = t_b[i] - number
                        if t_b[i] < 0:
                            bad = True
                            break
                    if bad:
                        break
                    t_t_b = tuple(t_b)

                    if t_t_b not in best_right:
                        best_right[t_t_b] = cc + number
                    best_right[t_t_b] = min(cc + number, best_right[t_t_b])

                    if t_t_b in best_left:
                        c_left = best_left[t_t_b]
                        c_right = best_right[t_t_b]
                        c_full = c_right + c_left
                        if best_solution is None:
                            best_solution = c_full
                        best_solution = min(c_full, best_solution)
                        print("Best", best_solution)

                    number += 1

    return best_solution


def get_best_result2_wrapped(i, stuff):
    best_result = get_best_result2(stuff=stuff)
    print(i, stuff, best_result)
    return best_result


def get_count2(p_internal, n_workers):
    result = []
    with ThreadPoolExecutor(max_workers=n_workers) as exe:
        result = exe.map(get_best_result2_wrapped, range(len(p_internal)), p_internal)
    count = sum(result)
    print(count)


get_count2(p_internal=[parsed(l=s)[100]], n_workers=1)
# get_count2(p_internal=[parsed(l=s)[4]], n_workers=1)
print()
# get_count2(p_internal=parsed(l=s), n_workers=30)
# print()
# get_count2(p_internal=p, n_workers=1)
# print()
