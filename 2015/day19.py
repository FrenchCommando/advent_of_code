from utils.printing import display


examples = """H => HO
H => OH
O => HH

HOHOHO"""


with open("day19.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p):
    replacements = []
    molecule = None

    for line in p:
        if not line:
            continue
        if "=>" in line:
            left, right = line.split(" => ")
            replacements.append((left, right))
            continue
        if molecule is None:
            molecule = line
            continue
        raise ValueError(line)

    print(replacements)
    print(molecule)

    results = set()
    for r in replacements:
        left, right = r
        i = -1
        while True:
            i += 1
            j = molecule[i:].find(left)
            if j == -1:
                break
            t = molecule[:i+j] + molecule[i+j:].replace(left, right, 1)
            results.add(t)
            i = i + j
    print(len(results))

    print()


get_count(p=[sss.strip() for sss in s])
get_count(p=[sss.strip() for sss in examples.split("\n")])
print()


def get_count2(p):
    replacements = []
    molecule = None

    for line in p:
        if not line:
            continue
        if "=>" in line:
            left, right = line.split(" => ")
            replacements.append((left, right))
            continue
        if molecule is None:
            molecule = line
            continue
        raise ValueError(line)

    print(replacements)
    print(molecule, len(molecule))

    def replace_names(name):
        return (
            name
                .replace("Al", "L")
                .replace("Ar", "Z")
                .replace("Ca", "C")
                .replace("Mg", "M")
                .replace("Rn", "R")
                .replace("Si", "S")
                .replace("Th", "T")
                .replace("Ti", "I")
        )

    clean_replacements = []
    for r in replacements:
        left, right = r
        if right.startswith("CRn"):
            continue
        r_left, r_right = replace_names(left), replace_names(right)
        clean_replacements.append((r_left, r_right))
    d_replacements = dict()
    for r in clean_replacements:
        left, right = r
        if left not in d_replacements:
            d_replacements[left] = []
        d_replacements[left].append(right)

    print(clean_replacements, len(clean_replacements))
    print(d_replacements)
    clean_molecule = replace_names(molecule)
    print(clean_molecule, len(clean_molecule))

    # BFS too slow
    atoms = [
        "L", "Z",
        "B", "C",
        "F",
        "M",
        "N", "O", "P", "H",
        "R",
        "S", "T", "I",
        "Y",
    ]
    molecule_count = {c: clean_molecule.count(c) for c in atoms}
    print(molecule_count)

    zs = molecule_count["Z"]
    ys = molecule_count["Y"]
    l_clean = len(clean_molecule)
    n = l_clean - zs * 2 - ys * 2

    print(n)
    print(n - 1, "if electron yields 2 in example")


examples2 = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""

examples3 = """e => H
e => O
H => HO
H => OH
O => HH

HOHOHO"""

get_count2(p=[sss.strip() for sss in s])
print()
get_count2(p=[sss.strip() for sss in examples2.split("\n")])
print()
get_count2(p=[sss.strip() for sss in examples3.split("\n")])
print()
