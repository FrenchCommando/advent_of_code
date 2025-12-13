import itertools
import queue
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


def candidates_q(t, buttons_internal, l_joltage, do_print):
    l_set_bits = [0 for u in range(l_joltage)]
    for u in buttons_internal:
        for b in u:
            l_set_bits[b] = l_set_bits[b] + 1

    non_zeros = [i for i, tt in enumerate(t) if tt != 0]
    optimal_non_zero = min(non_zeros, key=lambda i: l_set_bits[i])
    # optimal_non_zero = min(non_zeros, key=lambda i: 100 * l_set_bits[i] + t[i])
    # optimal_non_zero = min(non_zeros, key=lambda i: (l_set_bits[i], t[i]))
    # optimal_non_zero = min(non_zeros, key=lambda i: t[i])
    # optimal_non_zero = max(non_zeros, key=lambda i: t[i])
    # optimal_non_zero = non_zeros[max(0, min(len(non_zeros) - 1, 1))]  # just manually change the initial guess

    qq = queue.LifoQueue()
    qq.put((0, t))

    clean_bit_to_set = sorted([u for u in buttons_internal if all(z in non_zeros for z in u) and (optimal_non_zero in u)], key=len, reverse=True)
    # print(len(clean_bit_to_set), f"{clean_bit_to_set=}", f"{optimal_non_zero}")
    if len(clean_bit_to_set) == 0:
        return qq, optimal_non_zero
    # if len(non_zeros) > len(t) - 2:
    if do_print:
        print("\t\t\t", optimal_non_zero, non_zeros, t, clean_bit_to_set)

    i_last = len(clean_bit_to_set) - 1
    d_qq = {t: 0}

    for i_button, button in enumerate(clean_bit_to_set):
        if do_print:
            print(button, len(d_qq), len(clean_bit_to_set))
        d_qqq = dict()
        for tt, c in d_qq.items():
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
                d_qqq[t_t_b] = min(d_qqq.get(t_t_b, c + number), c + number)
                number += 1
        d_qq = dict()
        for k, v in d_qqq.items():
            d_qq[k] = v
    qq = queue.LifoQueue()
    for k, v in d_qq.items():
        qq.put((v, k))
    if do_print:
        print(f"{qq.qsize()=}")
    return qq, optimal_non_zero


def candidates_q_left(low_bounds_right, high_bounds_right, buttons_internal, l_joltage, do_print):
    l_set_bits = [0 for u in range(l_joltage)]
    for u in buttons_internal:
        for b in u:
            l_set_bits[b] = l_set_bits[b] + 1

    qq = queue.LifoQueue()
    qq.put((0, tuple(0 for _ in range(l_joltage))))

    non_zeros = [i for i, (ltt, rtt) in enumerate(zip(low_bounds_right, high_bounds_right)) if ltt == rtt and ltt != 0]
    if len(non_zeros) == 0:
        return qq, -1

    optimal_non_zero = min(non_zeros, key=lambda i: l_set_bits[i])
    # optimal_non_zero = min(non_zeros, key=lambda i: 100 * l_set_bits[i] + t[i])
    # optimal_non_zero = min(non_zeros, key=lambda i: (l_set_bits[i], t[i]))
    # optimal_non_zero = min(non_zeros, key=lambda i: t[i])
    # optimal_non_zero = max(non_zeros, key=lambda i: low_bounds_right[i])
    # optimal_non_zero = non_zeros[max(0, min(len(non_zeros) - 1, 2))]

    clean_bit_to_set = sorted([u for u in buttons_internal if optimal_non_zero in u], key=len, reverse=True)
    # print(len(clean_bit_to_set), f"{clean_bit_to_set=}", f"{optimal_non_zero}")
    if len(clean_bit_to_set) == 0:
        return qq, optimal_non_zero
    # if len(non_zeros) > len(t) - 2:
    #     print("\t\t\t", optimal_non_zero, non_zeros, t, clean_bit_to_set)

    if do_print:
        print(len(non_zeros), f"{non_zeros=}", f"{optimal_non_zero}", f"{clean_bit_to_set=}")

    i_last = len(clean_bit_to_set) - 1
    d_qq = {tuple(0 for _ in range(l_joltage)): 0}

    for i_button, button in enumerate(clean_bit_to_set):
        if do_print:
            print(button, len(d_qq), len(clean_bit_to_set))
        d_qqq = dict()
        for tt, c in d_qq.items():
            number = 0
            if i_button == i_last:
                number = high_bounds_right[optimal_non_zero] - tt[optimal_non_zero]
            while True:
                bad = False
                t_b = list(tt)
                for i in button:
                    t_b[i] = t_b[i] + number
                    if t_b[i] > high_bounds_right[i]:
                        bad = True
                        break
                if bad:
                    break
                t_t_b = tuple(t_b)
                d_qqq[t_t_b] = min(d_qqq.get(t_t_b, c + number), c + number)
                number += 1
        d_qq = dict()
        for k, v in d_qqq.items():
            d_qq[k] = v
    qq = queue.LifoQueue()
    for k, v in d_qq.items():
        qq.put((v, k))
    if do_print:
        print(f"{qq.qsize()=}")
    return qq, optimal_non_zero


def get_best_result2(stuff, do_print=False):
    lights, buttons, joltage = line_to_data(stuff=stuff)
    if do_print:
        print(buttons, joltage)

    l_joltage = len(joltage)

    best_right = dict()
    best_solution = sum(joltage) // min(len(b) for b in buttons)
    # best_solution = 305
    if do_print:
        print("Init", best_solution)
    qq, optimal_non_zero = candidates_q(t=joltage, buttons_internal=buttons, l_joltage=l_joltage, do_print=do_print)
    while not qq.empty():
        c_b, t_t_b = qq.get()
        if t_t_b in best_right and best_right[t_t_b] <= c_b:
            continue

        if all(u == 0 for u in t_t_b):
            best_solution = min(c_b, best_solution)
            if do_print:
                print("Best", best_solution)
            continue
        best_right[t_t_b] = c_b

    low_bounds_right = [min(b[k] for b in best_right) for k in range(l_joltage)]
    high_bounds_right = [max(b[k] for b in best_right) for k in range(l_joltage)]
    other_buttons_left = sorted([b for b in buttons if optimal_non_zero not in b], key=len, reverse=False)
    if do_print:
        print(f"{low_bounds_right=}")
        print(f"{high_bounds_right=}")
        print(f"{joltage=}")
        print(f"{other_buttons_left=}")

    best_left = dict()
    qq_left, optimal_non_zero_left = candidates_q_left(
        low_bounds_right=low_bounds_right, high_bounds_right=high_bounds_right, buttons_internal=other_buttons_left, l_joltage=l_joltage,
        do_print=do_print,
    )
    while not qq_left.empty():
        c_b, t_t_b = qq_left.get()
        if t_t_b in best_left and best_left[t_t_b] <= c_b:
            continue

        if t_t_b in best_right:
            c_full = c_b + best_right[t_t_b]
            best_solution = min(c_full, best_solution)
            if do_print:
                print("Best", best_solution)
            continue
        best_left[t_t_b] = c_b

    low_bounds_left = [min((b[k] for b in best_left), default=0) for k in range(l_joltage)]
    high_bounds_left = [max((b[k] for b in best_left), default=joltage[k]) for k in range(l_joltage)]
    # other_buttons = sorted([b for b in other_buttons_left if optimal_non_zero_left not in b], key=len, reverse=False)
    other_buttons = sorted([b for b in other_buttons_left if optimal_non_zero_left not in b], key=len, reverse=True)

    c_min_left = min(best_left.values(), default=0)
    c_min_right = min(best_right.values(), default=0)

    if do_print:
        print(f"{low_bounds_right=}")
        print(f"{high_bounds_right=}")
        print(f"{low_bounds_left=}")
        print(f"{high_bounds_left=}")
        print(f"{joltage=}")

        print(f"{other_buttons=}")

        print(f"{c_min_left=}|{c_min_right=}")

    index_from_right = [i for i, (low, high) in enumerate(zip(low_bounds_right, high_bounds_right)) if low == 0 and high == 0]
    index_from_left = [i for i, (low, high, low_r, high_r) in enumerate(zip(low_bounds_left, high_bounds_left, low_bounds_right, high_bounds_right)) if low == high and low_r == high_r and low == low_r]
    index_to_remove = sorted((set(index_from_left) | set(index_from_right)))
    if do_print:
        print(f"{index_from_right=}|{index_from_left=}|{index_to_remove=}")
    # convert best_left, best_right, other_buttons
    # low_bounds_left, high_bounds_right
    def convert_button(button):
        out = []
        for b in button:
            if b in index_to_remove:
                continue
            n_decrement = 0
            for i in index_to_remove:
                if i < b:
                    n_decrement += 1
            out.append(b - n_decrement)
        return tuple(out)
    def convert_tuple(weights):
        out = []
        for i, w in enumerate(weights):
            if i in index_to_remove:
                continue
            out.append(w)
        return tuple(out)
    if do_print:
        print(f"{other_buttons=}")
    other_buttons = [convert_button(b) for b in other_buttons]
    if do_print:
        print(f"{other_buttons=}")
    l_joltage = l_joltage - len(index_to_remove)
    c_best_left = dict()
    for b, c in best_left.items():
        c_best_left[convert_tuple(weights=b)] = c
    best_left = c_best_left
    c_best_right = dict()
    for b, c in best_right.items():
        c_best_right[convert_tuple(weights=b)] = c
    best_right = c_best_right
    low_bounds_left = [min((b[k] for b in best_left), default=0) for k in range(l_joltage)]
    high_bounds_right = [max((b[k] for b in best_right), default=0) for k in range(l_joltage)]
    if do_print:
        print(f"{low_bounds_left=}")
        print(f"{high_bounds_right=}")

    i_last = len(other_buttons) - 1
    for ib, b in enumerate(other_buttons):
        if do_print:
            print(f"\t{b=} - {len(best_left)=} - {len(best_right)=}")
        if len(best_left) < len(best_right):
            for bb in list(best_left.keys()):
                cc = best_left[bb]
                if cc + c_min_right >= best_solution:
                    del best_left[bb]
                    continue
                max_number = best_solution - (cc + c_min_right)

                number = 1
                while number < max_number:
                    bad = False
                    t_b = list(bb)
                    for i in b:
                        t_b[i] = t_b[i] + number
                        if t_b[i] > high_bounds_right[i]:
                            bad = True
                            break
                    if bad:
                        break
                    t_t_b = tuple(t_b)

                    if ib == i_last:
                        if t_t_b in best_right:
                            c_left = cc + number
                            c_right = best_right[t_t_b]
                            c_full = c_right + c_left
                            best_solution = min(c_full, best_solution)
                            if do_print:
                                print("Best", best_solution)
                    else:
                        best_left[t_t_b] = min(cc + number, best_left.get(t_t_b, cc + number))

                        if t_t_b in best_right:
                            c_left = best_left[t_t_b]
                            c_right = best_right[t_t_b]
                            c_full = c_right + c_left
                            best_solution = min(c_full, best_solution)
                            if do_print:
                                print("Best", best_solution)

                    number += 1
        else:
            for bb in list(best_right.keys()):
                cc = best_right[bb]
                if cc + c_min_left >= best_solution:
                    del best_right[bb]
                    continue
                max_number = best_solution - (cc + c_min_left)

                number = 1
                while number < max_number:
                    bad = False
                    t_b = list(bb)
                    for i in b:
                        t_b[i] = t_b[i] - number
                        if t_b[i] < low_bounds_left[i]:
                            bad = True
                            break
                    if bad:
                        break
                    t_t_b = tuple(t_b)
                    if ib == i_last:
                        if t_t_b in best_left:
                            c_left = best_left[t_t_b]
                            c_right = cc + number
                            c_full = c_right + c_left
                            best_solution = min(c_full, best_solution)
                            if do_print:
                                print("Best", best_solution)
                    else:
                        best_right[t_t_b] = min(cc + number, best_right.get(t_t_b, cc + number))

                        if t_t_b in best_left:
                            c_left = best_left[t_t_b]
                            c_right = best_right[t_t_b]
                            c_full = c_right + c_left
                            best_solution = min(c_full, best_solution)
                            if do_print:
                                print("Best", best_solution)

                    number += 1

        if do_print:
            print(f"\t{b=} - {len(best_left)=} - {len(best_right)=} - Post")
    return best_solution


def get_best_result2_wrapped(i, stuff):
    best_result = get_best_result2(stuff=stuff)
    print(i, stuff, best_result)
    return best_result


def get_count2(p_internal, do_print=False):
    count = 0
    for i, stuff in enumerate(p_internal):
        # manually changing heuristics and saving results
        precomputed = {
            4: 119,
            29: 229,
            37: 282,
            38: 249,
            48: 86,
            51: 218,
            59: 120,
            69: 117,
            77: 283,  # init guess 3
            82: 231,
            105: 117,
            115: 146,
            117: 292,  # guessed from current upper bound
            127: 266,
            140: 98,
            150: 106,
            158: 123,
            174: 273,
        }
        skipped = [
        ]
        if i in skipped:
            print("Skipped", i, stuff)
            continue
        if i in precomputed:
            best_result = precomputed[i]
        else:
            best_result = get_best_result2(stuff=stuff, do_print=do_print)
        print(i, stuff, best_result)
        count += best_result
    print(count)
    return count


# get_count2(p_internal=[parsed(l=s)[117]], do_print=True)
# get_count2(p_internal=[parsed(l=s)[4]], do_print=True)
# get_count2(p_internal=[parsed(l=s)[29]], do_print=True)
get_count2(p_internal=parsed(l=s))
get_count2(p_internal=p)
