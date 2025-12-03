from utils.printing import display


example = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


l_list = []
val = 0
for x in s:
    if x.strip() == "":
        l_list.append(val)
        val = 0
    else:
        val += float(x)

display(l_list)
display(max(l_list))
display(sorted(l_list)[-3:])
display(sum(sorted(l_list)[-3:]))
