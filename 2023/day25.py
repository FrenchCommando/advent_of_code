from utils.printing import display

example = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


with open("day25.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


grid_value = example.split("\n")
# grid_value = s
l_blocks = parse(text=grid_value)
display(x=l_blocks)
