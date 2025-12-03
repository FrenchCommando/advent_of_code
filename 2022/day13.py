import json
from functools import cmp_to_key
from utils.printing import display


with open("day13.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


def check_order(l1, l2):
    if isinstance(l1, int) and isinstance(l2, int):
        if l1 < l2:
            return True
        if l2 < l1:
            return False
        return None
    if isinstance(l1, list) and isinstance(l2, int):
        return check_order(l1=l1, l2=[l2])
    if isinstance(l1, int) and isinstance(l2, list):
        return check_order(l1=[l1], l2=l2)
    if isinstance(l1, list) and isinstance(l2, list):
        if l1 and not l2:
            return False
        if not l1 and l2:
            return True
        if not l1 and not l2:
            return None
        first = check_order(l1=l1[0], l2=l2[0])
        if first is not None:
            return first
        return check_order(l1=l1[1:], l2=l2[1:])
    raise ValueError(f"unrecognized type {l1} {l2}")


results = []
i_lines = iter(lines)
try:
    while True:
        line1 = json.loads(next(i_lines))
        line2 = json.loads(next(i_lines))
        results.append(check_order(l1=line1, l2=line2))
        next(i_lines)
except StopIteration:
    pass


display(results)
display(sum(i for i, j in enumerate(results, 1) if j))

sorted_lines = [json.loads(line) for line in lines if line]
sorted_lines.append([[2]])
sorted_lines.append([[6]])
sorted_lines = sorted(
    sorted_lines,
    key=cmp_to_key(
        lambda item1, item2: -1 if check_order(l1=item1, l2=item2) else 1
    ),
    reverse=False,
)
for line in sorted_lines:
    print(line)

sorted_lines_json = [json.dumps(line) for line in sorted_lines]
index_2 = sorted_lines_json.index("[[2]]") + 1
index_6 = sorted_lines_json.index("[[6]]") + 1
print(index_2, index_6)
print(index_2 * index_6)
