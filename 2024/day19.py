import queue
import re
from utils.printing import display

example = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""



with open("day19.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    g = l[0].split(", ")
    t = l[2:]

    print(len(g), g)
    print(len(t), t)

    while True:
        modified = False
        for sub in g:
            sub_pat = f"^({'|'.join(gg for gg in g if gg != sub)})+$"
            if re.match(sub_pat, sub):
                g.remove(sub)
                modified = True
                break
        if not modified:
            break
    print("g_modified", len(g), g)

    pat = f"^({'|'.join(g)})+$"
    print(pat)
    c = 0
    for line in t:
        if re.match(pat, line):
            c += 1
        else:
            print("\t\tnot-matched", end="\t")
        print(line, c)

    return c


p = count(l=example.split("\n"))
print("count", p)
# ps = count(l=[line.strip() for line in s])
# print("count", ps)


def count2(l):
    g = l[0].split(", ")
    t = l[2:]

    print(len(g), g)
    print(len(t), t)

    g_modified = [gg for gg in g]
    while True:
        modified = False
        for sub in g_modified:
            sub_pat = f"^({'|'.join(gg for gg in g_modified if gg != sub)})+$"
            if re.match(sub_pat, sub):
                g_modified.remove(sub)
                modified = True
                break
        if not modified:
            break
    print("g_modified", len(g_modified), g_modified)

    pat_mod = f"^({'|'.join(g_modified)})+$"
    pat = f"^({'|'.join(g)})+$"
    print(pat_mod)
    print(pat)


    match_cache = dict()

    def match_count(string_value):
        nonlocal match_cache
        if string_value in match_cache:
            return match_cache[string_value]

        if string_value == "":
            match_cache[string_value] = 1
            return 1

        rrr = 0
        for gg in g:
            # print(string_value, gg)
            if string_value.startswith(gg):
                ss_line = string_value[len(gg):]
                # print("\tSub", gg, string_value, ss_line)
                sub_match = match_count(string_value=ss_line)
                rrr += sub_match
        # print(string_value, rrr)
        match_cache[string_value] = rrr
        return rrr

    c = 0
    cc = 0
    for line in t:
        if re.match(pat_mod, line):
            c += 1
            cc += match_count(string_value=line)
            print()

        else:
            print("\t\tnot-matched", end="\t")
        print(line, c, cc)
    return cc


p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
