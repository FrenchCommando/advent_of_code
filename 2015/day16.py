from utils.printing import display


examples = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1"""


with open("day16.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(sues, specs):
    # print(sues)
    # print(specs)
    data = dict()
    for line in specs:
        entry, v = line.split(": ")
        data[entry] = int(v)
    data_s = dict()
    for line in sues:
        name, v = line.split(": ", maxsplit=1)
        entries = v.split(", ")
        d_s = dict()
        for entry in entries:
            key, value = entry.split(": ")
            d_s[key] = int(value)
        data_s[name] = d_s
    print(data_s)
    print(data)

    for name, d in data_s.items():
        good = True
        for k, v in d.items():
            kk = data[k]
            if kk != v:
                good = False
                break
        if good:
            print(name)


get_count(sues=[sss.strip() for sss in s], specs=[sss.strip() for sss in examples.split("\n")])
print()


def get_count2(sues, specs):
    # print(sues)
    # print(specs)
    data = dict()
    for line in specs:
        entry, v = line.split(": ")
        data[entry] = int(v)
    data_s = dict()
    for line in sues:
        name, v = line.split(": ", maxsplit=1)
        entries = v.split(", ")
        d_s = dict()
        for entry in entries:
            key, value = entry.split(": ")
            d_s[key] = int(value)
        data_s[name] = d_s
    # print(data_s)
    # print(data)

    for name, d in data_s.items():
        good = True
        for k, v in d.items():
            kk = data[k]
            if k in ["cats", "trees"]:
                if kk >= v:
                    good = False
                    break
            elif k in ["pomeranians", "goldfish"]:
                if kk <= v:
                    good = False
                    break
            else:
                if kk != v:
                    good = False
                    break
        if good:
            print(name)


get_count2(sues=[sss.strip() for sss in s], specs=[sss.strip() for sss in examples.split("\n")])
print()
