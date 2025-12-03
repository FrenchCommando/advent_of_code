import re
from utils.printing import display


with open("day5.txt", "r") as f:
    lines = f.readlines()


display(lines)

i = 0
for l_line in lines:
    if l_line == '\n':
        break
    i += 1

pre_lines = lines[:i]
post_lines = lines[i + 1:]
display(pre_lines)
display(post_lines)


def parse_init(l_lines):
    count = len([u for u in l_lines[-1].strip().split(" ") if u])
    display(count)
    display(l_lines[-1].strip().split(" "))
    l_out = []
    for iii in range(count):
        l_out.append([])
    for line in reversed(l_lines[:-1]):
        for ii in range(count):
            index = 1 + ii * 4
            if index < len(line):
                s = line[index]
                if s != " ":
                    l_out[ii].append(s)
    return l_out


l_init = parse_init(l_lines=pre_lines)
display(l_init)


def advance(l_object, line, order=False):
    d = re.match(
        pattern=r"move (?P<number>.*) from (?P<from>.*) to (?P<to>.*)",
        string=line,
    ).groupdict()
    # display(d)
    l_number = int(d['number'])
    l_from = int(d['from']) - 1
    l_to = int(d['to']) - 1
    if order:
        l_internal = []
        for iii in range(l_number):
            item = l_object[l_from].pop()
            l_internal.append(item)
        l_object[l_to].extend(l_internal[::-1])
    else:
        for iii in range(l_number):
            item = l_object[l_from].pop()
            l_object[l_to].append(item)


l_init = parse_init(l_lines=pre_lines)
display(l_init)
for l_line in post_lines:
    advance(l_object=l_init, line=l_line, order=False)
display(l_init)
display("".join(l[-1] for l in l_init))


l_init = parse_init(l_lines=pre_lines)
display(l_init)
for l_line in post_lines:
    advance(l_object=l_init, line=l_line, order=True)
display(l_init)
display("".join(l[-1] for l in l_init))
