import itertools
import queue
import array as arr
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
    non_zeros = [i for i, tt in enumerate(t) if tt != 0]

    l_set_bits = [0 for u in range(l_joltage)]
    for u in buttons_internal:
        for b in u:
            l_set_bits[b] += 1

    # choose the non_zero value that would optimise the number of buttons processed in the 2 steps
    # we want "min((l_set_bits * l_set_bits) and not zero)"

    def get_optimal_non_zero(i):
        # not really cleaned after trashing the _left part of the code
        clean_bit_to_set_internal = sorted([u for u in buttons_internal if all(z in non_zeros for z in u) and (i in u)], key=len, reverse=True)
        i0 = l_set_bits[i]

        l_set_bits_internal = [0 for u in range(l_joltage)]
        # for u in buttons_internal:
        #     if u in clean_bit_to_set_internal:
        #         continue
        #     for b in u:
        #         l_set_bits_internal[b] += 1
            # print(u)
        for u in clean_bit_to_set_internal:
            for b in u:
                l_set_bits_internal[b] += 1
        optimal_non_zero_internal = max(non_zeros, key=l_set_bits_internal.__getitem__)

        i1 = l_set_bits_internal[optimal_non_zero_internal]

        # low_bounds_right = [min(short_to_int(i=b, k=k) for b in best_right) for k in range(l_joltage)]
        # high_bounds_right = [max(short_to_int(i=b, k=k) for b in best_right) for k in range(l_joltage)]
        # non_zeros_left = [i for i, (ltt, rtt) in enumerate(zip(low_bounds_right, high_bounds_right)) if ltt == rtt and ltt != 0]
        out = max(i0, i1) < l_joltage // 2, i0 * i1
        # print(i, out, i0, i1, l_set_bits_internal, l_set_bits, clean_bit_to_set_internal)
        return out

    optimal_non_zero = min(non_zeros, key=get_optimal_non_zero)
    # optimal_non_zero = min(non_zeros, key=l_set_bits.__getitem__)
    # optimal_non_zero = non_zeros[max(0, min(len(non_zeros) - 1, 0))]  # just manually change the initial guess
    clean_bit_to_set = sorted([u for u in buttons_internal if all(z in non_zeros for z in u) and (optimal_non_zero in u)], key=len, reverse=True)

    b_t = ints_to_short(i=t)
    d_qq = {b_t: 0}

    # print(len(clean_bit_to_set), f"{clean_bit_to_set=}", f"{optimal_non_zero}")
    if len(clean_bit_to_set) == 0:
        return d_qq, optimal_non_zero
    # if len(non_zeros) > len(t) - 2:
    if do_print:
        print("\t\t\t", optimal_non_zero, non_zeros, t, b_t, clean_bit_to_set)

    i_last = len(clean_bit_to_set) - 1


    for i_button, button in enumerate(clean_bit_to_set):
        if do_print:
            print(button, len(d_qq), len(clean_bit_to_set))
        d_qqq = dict()
        for tt, c in d_qq.items():
            number = 0
            if i_button == i_last:
                number = short_to_ints(i=tt)[optimal_non_zero]
            while True:
                bad = False
                for i in button:
                    if short_to_int(i=tt, k=i) - number < 0:
                        bad = True
                        break
                if bad:
                    break
                ss = short_to_ints(i=tt)
                t_t_b = ints_to_short(i=(sss - number * (i in button) for i, sss in enumerate(ss)))
                d_qqq[t_t_b] = min(d_qqq.get(t_t_b, c + number), c + number)
                number += 1
        d_qq = dict()
        for k, v in d_qqq.items():
            d_qq[k] = v
    if do_print:
        print(f"{len(d_qq)=}")
    return d_qq, optimal_non_zero


def find_best_solution(
        other_buttons, best_left, best_right, best_solution, do_print, l_joltage, loop_info,
):
    while len(other_buttons) > 0 and len(best_left) > 0 and len(best_right) > 0:
        low_bounds_right = [min(short_to_int(i=b, k=k) for b in best_right) for k in range(l_joltage)]
        high_bounds_right = [max(short_to_int(i=b, k=k) for b in best_right) for k in range(l_joltage)]
        low_bounds_left = [min((short_to_int(i=b, k=k) for b in best_left)) for k in range(l_joltage)]
        high_bounds_left = [max((short_to_int(i=b, k=k) for b in best_left)) for k in range(l_joltage)]

        index_from_right = [i for i, (low, high) in enumerate(zip(low_bounds_right, high_bounds_right)) if low == 0 and high == 0]
        index_from_left = [
            i for i, (low, high, low_r, high_r) in enumerate(zip(low_bounds_left, high_bounds_left, low_bounds_right, high_bounds_right))
            if low == high and low_r == high_r and low == low_r
        ]
        index_to_remove = sorted((set(index_from_left) | set(index_from_right)))
        if do_print:
            print(f"{index_from_right=}|{index_from_left=}|{index_to_remove=}")
        if index_to_remove and loop_info == "":
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
                bbb = short_to_ints(i=weights)
                out = []
                for i, w in enumerate(bbb):
                    if i in index_to_remove:
                        continue
                    out.append(w)
                rrr = ints_to_short(i=out)
                return rrr

            if do_print:
                print(f"{other_buttons=}")
            other_buttons = [convert_button(b) for b in other_buttons]
            if do_print:
                print(f"ReIndexed|{other_buttons=}")
            l_joltage = l_joltage - len(index_to_remove)
            c_best_left = dict()
            for b, c in best_left.items():
                c_best_left[convert_tuple(weights=b)] = c
            best_left = c_best_left
            c_best_right = dict()
            for b, c in best_right.items():
                c_best_right[convert_tuple(weights=b)] = c
            best_right = c_best_right
            low_bounds_left = [min((short_to_int(i=b, k=k) for b in best_left), default=0) for k in range(l_joltage)]
            high_bounds_right = [max((short_to_int(i=b, k=k) for b in best_right), default=0) for k in range(l_joltage)]
            if do_print:
                print(f"ReIndexed|{low_bounds_left=}")
                print(f"ReIndexed|{high_bounds_right=}")

        remaining_buttons = tuple({u for bs in other_buttons for u in bs})
        b = other_buttons.pop(0)
        is_last = len(other_buttons) == 0

        c_min_left = min(best_left.values())
        c_min_right = min(best_right.values())
        low_bounds_left_b = [min((short_to_int(i=bbb, k=bb) for bbb in best_left)) for bb in b]
        high_bounds_right_b = [max((short_to_int(i=bbb, k=bb) for bbb in best_right)) for bb in b]

        if do_print:
            print(f"\t{b=} - {len(best_left)=} - {len(best_right)=}|"
                  f"{c_min_left=}|{c_min_right=}|{low_bounds_left_b=}|{high_bounds_right_b=}")

        for bb in list(best_left.keys()):
            cc = best_left[bb]
            if cc + c_min_right >= best_solution:
                del best_left[bb]
        for bb in list(best_right.keys()):
            cc = best_right[bb]
            if cc + c_min_left >= best_solution:
                del best_right[bb]
        if not best_left or not best_right:
            return best_solution
        c_min_left = min(best_left.values())
        c_min_right = min(best_right.values())
        low_bounds_left_b = [min((short_to_int(i=bbb, k=bb) for bbb in best_left)) for bb in b]
        high_bounds_right_b = [max((short_to_int(i=bbb, k=bb) for bbb in best_right)) for bb in b]
        if do_print:
            print(f"\t\tpruning using best_solution value | "
                  f"{b=} - {len(best_left)=} - {len(best_right)=}|{c_min_left=}|{c_min_right=}|"
                  f"{low_bounds_left_b=}|{high_bounds_right_b=}")

        mask_left = dict()
        mask_right = dict()
        for bb in best_left:
            b_int = short_to_ints(i=bb)
            t_b = tuple(v for i, v in enumerate(b_int) if i not in remaining_buttons)
            if t_b not in mask_left:
                mask_left[t_b] = dict()
            mask_left[t_b][bb] = best_left[bb]
        for bb in best_right:
            b_int = short_to_ints(i=bb)
            t_b = tuple(v for i, v in enumerate(b_int) if i not in remaining_buttons)
            if t_b not in mask_right:
                mask_right[t_b] = dict()
            mask_right[t_b][bb] = best_right[bb]
        mask_both = set(u for u in mask_left.keys() & mask_right.keys())

        if do_print:
            print(f"\t\tintermediate for mask {len(mask_left)=} - {len(mask_right)=} - {len(mask_both)=} | \t{len(best_left)=}, {len(best_right)=}")

        if len(mask_both) > 1:
            l_mask = len(mask_both)
            q_mask = queue.Queue()
            for i_mask, bb_mask in enumerate(mask_both):
                best_left_temp = mask_left[bb_mask]
                best_right_temp = mask_right[bb_mask]
                q_mask.put((i_mask, best_left_temp, best_right_temp))
                del mask_left[bb_mask]
                del mask_right[bb_mask]
            del mask_both
            del mask_left
            del mask_right

            while not q_mask.empty():
                i_mask, best_left_temp, best_right_temp = q_mask.get()
                other_buttons_temp = [b]
                for bbbb in other_buttons:
                    other_buttons_temp.append(bbbb)

                loop_info_loop = f"{loop_info}|{i_mask=}/{l_mask=}"

                if do_print:
                    print(f"\t\tSub-branch|{i_mask} | {len(best_left_temp)=}, {len(best_right_temp)=} | {other_buttons_temp=}")
                    print(f"\t\t\t{loop_info_loop}")
                # print(bb_mask, best_left_temp, best_left, other_buttons_temp, best_right_temp)
                best_solution_temp = find_best_solution(
                    other_buttons_temp, best_left_temp, best_right_temp, best_solution,
                    do_print=False,
                    l_joltage=l_joltage,
                    loop_info=loop_info_loop,
                )
                if best_solution_temp < best_solution:
                    if do_print:
                        print(f"\t\tBest Found {best_solution_temp=} {best_solution=}| Sub-branch|{i_mask} | {len(best_left_temp)=}, {len(best_right_temp)=} | {other_buttons_temp=}")
                    best_solution = best_solution_temp

                if do_print:
                    print(f"\t\tEnd - Sub-branch|{i_mask} | {len(best_left_temp)=}, {len(best_right_temp)=}")
            return best_solution

        if not mask_both:
            return best_solution
        one_mask = next(iter(mask_both))
        best_left = mask_left[one_mask]
        best_right = mask_right[one_mask]

        if do_print:
            print(f"\t\t{len(mask_left)=} - {len(mask_right)=} - {len(mask_both)=} | \t{len(best_left)=}, {len(best_right)=}")

        if is_last:
            # reduce the size of best_left, best_right
            ll_left = []
            ll_right = []
            for ibb, bb in enumerate(best_left):
                cc = best_left[bb]
                max_number = best_solution - (cc + c_min_right)
                # if do_print:
                #     print(f"\t\t{bb=} - {len(l_left)=}, {len(l_right)=} - {max_number=}")
                number = 1
                while number < max_number:
                    bad = False
                    for bi, i in enumerate(b):
                        if short_to_int(i=bb, k=i) + number > high_bounds_right_b[bi]:
                            bad = True
                            break
                    if bad:
                        break
                    ss = short_to_ints(i=bb)
                    t_t_b = ints_to_short(i=(sss + number * (i in b) for i, sss in enumerate(ss)))
                    if t_t_b in best_right:
                        ll_left.append(bb)
                        ll_right.append(t_t_b)
                    number += 1
                if do_print:
                    if ibb % 100000 == 0:
                        print(f"\t\t{ibb=} {bb=} {number=} {len(best_left)=}, {len(best_right)=} | {len(ll_left)=} | {len(ll_right)=}")
            best_left = {left: best_left[left] for left in ll_left}
            best_right = {right: best_right[right] for right in ll_right}
            if do_print:
                print(f"\tafter pruning last loop: {len(best_left)=} - {len(best_right)=}")

        if len(best_left) < len(best_right):
            for bb in list(best_left.keys()):
                cc = best_left[bb]
                max_number = best_solution - (cc + c_min_right)

                number = 1
                while number < max_number:
                    bad = False
                    for bi, i in enumerate(b):
                        if short_to_int(i=bb, k=i) + number > high_bounds_right_b[bi]:
                            bad = True
                            break
                    if bad:
                        break
                    ss = short_to_ints(i=bb)
                    t_t_b = ints_to_short(i=(sss + number * (i in b) for i, sss in enumerate(ss)))
                    if t_t_b in best_right:
                        c_left = cc + number
                        c_right = best_right[t_t_b]
                        c_full = c_right + c_left
                        if do_print:
                            print("Best", best_solution, c_full)
                        best_solution = min(c_full, best_solution)
                    if not is_last:
                        best_left[t_t_b] = min(cc + number, best_left.get(t_t_b, cc + number))
                    number += 1
                if is_last:
                    del best_left[bb]
                    if do_print:
                        if (len(best_left) + len(best_right)) % 10000 == 0:
                            print("Reduced size", len(best_left), len(best_right))
        else:
            for bb in list(best_right.keys()):
                cc = best_right[bb]
                max_number = best_solution - (cc + c_min_left)

                number = 1
                while number < max_number:
                    bad = False
                    for bi, i in enumerate(b):
                        if short_to_int(i=bb, k=i) - number < low_bounds_left_b[bi]:
                            bad = True
                            break
                    if bad:
                        break
                    ss = short_to_ints(i=bb)
                    t_t_b = ints_to_short(i=(sss - number * (i in b) for i, sss in enumerate(ss)))
                    if t_t_b in best_left:
                        c_left = best_left[t_t_b]
                        c_right = cc + number
                        c_full = c_right + c_left
                        if do_print:
                            print("Best", best_solution, c_full)
                        best_solution = min(c_full, best_solution)
                    if not is_last:
                        best_right[t_t_b] = min(cc + number, best_right.get(t_t_b, cc + number))
                    number += 1
                if is_last:
                    del best_right[bb]
                    if do_print:
                        if (len(best_left) + len(best_right)) % 10000 == 0:
                            print("Reduced size", len(best_left), len(best_right))

        if do_print:
            print(f"\t{b=} - {len(best_left)=} - {len(best_right)=} - Post")

    return best_solution


def ints_to_short(i):
    return arr.array('H', i).tobytes()


def short_to_int(i, k):
    a = arr.array('H', [])
    a.frombytes(i)
    return a[k]


def short_to_ints(i):
    a = arr.array('H', [])
    a.frombytes(i)
    return tuple(a)


def get_best_result2(stuff, do_print=False):
    lights, buttons, joltage = line_to_data(stuff=stuff)
    if do_print:
        print(buttons, joltage)

    l_joltage = len(joltage)

    best_solution = sum(joltage) // min(len(b) for b in buttons)
    if do_print:
        print("Init", best_solution)
    best_right, optimal_non_zero = candidates_q(t=joltage, buttons_internal=buttons, l_joltage=l_joltage, do_print=do_print)
    for t_t_b, c_b in best_right.items():
        if all(u == 0 for u in short_to_ints(i=t_t_b)):
            best_solution = min(c_b, best_solution)
            if do_print:
                print("Best", best_solution)
            continue
        best_right[t_t_b] = c_b

    if not best_right:
        return best_solution

    other_buttons = sorted([b for b in buttons if optimal_non_zero not in b], key=len, reverse=True)
    best_left = {ints_to_short(i=(0 for _ in range(l_joltage))): 0}
    best_solution = find_best_solution(
        other_buttons=other_buttons,
        best_left=best_left, best_right=best_right,
        best_solution=best_solution, do_print=do_print,
        l_joltage=l_joltage,
        loop_info="",
    )

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
            # 4: 119,  # just takes a long time
            # 29: 229,
            # 37: 282,
            # 38: 249,
            # 48: 86,
            # 51: 218,
            # 59: 120,
            # 69: 117,
            # 77: 283,  # init guess 3
            # 82: 231,
            # 105: 117,  # init guess 8
            # 115: 146,
            # 117: 292,  # just takes a very very long time - and 30GB of RAM
            # 127: 266,  # just takes a long time
            # 140: 98,
            # 150: 106,
            # 158: 123,
            # 174: 273,
        }
        skipped = [
            # *list(range(115))
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


# get_count2(p_internal=[parsed(l=s)[4]], do_print=True)
# get_count2(p_internal=[parsed(l=s)[117]], do_print=True)
# get_count2(p_internal=[parsed(l=s)[150]], do_print=True)
get_count2(p_internal=parsed(l=s))
# get_count2(p_internal=p, do_print=True)
# get_count2(p_internal=p)
