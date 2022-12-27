from utils.printing import display


with open("day4.txt", "r") as f:
    lines = f.readlines()


display(lines)


def parse_line(line):
    left, right = line.split(",")

    def split_range(r):
        r_left, r_right = r.split('-')
        return int(r_left), int(r_right)

    ll, lr = split_range(r=left)
    rl, rr = split_range(r=right)
    if ll <= rl:
        if lr >= rr:
            return True
    if rl <= ll:
        if rr >= lr:
            return True
    return False


display(parse_line(line="2-4,6-8"))
display(parse_line(line="2-8,3-7"))

display(sum(parse_line(line=line) for line in lines))


def parse_line2(line):
    left, right = line.split(",")

    def split_range(r):
        r_left, r_right = r.split('-')
        return int(r_left), int(r_right)

    ll, lr = split_range(r=left)
    rl, rr = split_range(r=right)
    if lr < rl:
        return False
    if rr < ll:
        return False
    return True


display(sum(parse_line2(line=line) for line in lines))
