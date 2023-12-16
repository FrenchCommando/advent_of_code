from functools import lru_cache

from utils.printing import display

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


with open("day12.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def parse(text):
    out = []
    for t in text:
        tab = t.strip().split(" ")
        i = list(map(int, tab[-1].split(",")))
        out.append((tab[0].strip(), i))
    return out


def solve(ts, multiple=1):
    rep = []
    for i, (t, c) in enumerate(ts):
        mt = "?".join([t] * multiple)
        mc = c * multiple
        # print(i, t, c, mt, mc)
        result = solve_one(t=mt, c=mc)
        # print(result)
        rep.append(result)
    return rep


def solve_one(t, c):
    @lru_cache()
    def solve_pound(ti, ci, c0):
        # starts with a pound
        for i in range(c0 - 1):
            try:
                tt = t[ti]
                ti += 1
                if tt == ".":
                    return 0
            except IndexError:
                return 0
        try:
            tt = t[ti]
            ti += 1
            if tt == "#":
                return 0
            return solve_one_internal(ti=ti, ci=ci)
        except IndexError:
            return 1 if ci == len(c) else 0

    @lru_cache()
    def solve_one_internal(ti, ci):
        while ti < len(t) and t[ti] == ".":
            ti += 1
        if len(c[ci:]) == 0:
            if "#" in t[ti:]:
                return 0
            return 1
        if len(t) == ti:
            return 0

        res_one = solve_pound(ti=ti + 1, ci=ci + 1, c0=c[ci])
        res_zero = solve_one_internal(ti=ti + 1, ci=ci)

        if t[ti] == "#":
            return res_one
        return res_zero + res_one

    return solve_one_internal(ti=0, ci=0)


l_parsed = parse(text=example.split("\n"))
# l_parsed = parse(text=s)

display(x=l_parsed)
l_result = solve(ts=l_parsed)
display(x=l_result)
display(x=sum(l_result))

l_result = solve(ts=l_parsed, multiple=5)
display(x=l_result)
display(x=sum(l_result))
