import re
from utils.printing import display

example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

example2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


pattern = r"(\D*)(?P<left>\d)(.*)(?P<right>\d)(\D*)"
pattern_single = r"(\D*)(?P<single>\d)(\D*)"


def matched(val):
    print(val)
    try:
        d = re.fullmatch(pattern=pattern, string=val.strip()).groupdict()
        return d['left'], d['right']
    except AttributeError:
        d = re.fullmatch(pattern=pattern_single, string=val.strip()).groupdict()
        return d['single'], d['single']


l_list = []
# for x in s:
for x in example.split("\n"):
    out = matched(val=x)
    display(x=out)
    l_list.append(int(out[0] + out[1]))

display(l_list)
display(sum(l_list))


numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
r_numbers = [n[::-1] for n in numbers]


def match_left(val, reverse=False):
    candidates = []
    if reverse:
        for i, n in enumerate(r_numbers, 1):
            score = len(val.split(sep=n, maxsplit=1)[0])
            candidates.append((str(i), score))
    else:
        for i, n in enumerate(numbers, 1):
            score = len(val.split(sep=n, maxsplit=1)[0])
            candidates.append((str(i), score))
    score_int = len(re.split(pattern=r"\d", string=val, maxsplit=1)[0])
    if score_int < len(val):
        candidates.append((val[score_int], score_int))
    return min(candidates, key=lambda xx: xx[1])[0]


l_list2 = []


# for x in s:
for x in example2.split("\n"):
    left = match_left(val=x, reverse=False)
    right = match_left(val=x[::-1], reverse=True)
    display(x=left)
    display(x=right)
    l_list2.append(int(left + right))

display(l_list2)
display(sum(l_list2))
