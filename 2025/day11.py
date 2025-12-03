from utils.printing import display

example = """SAMPLE"""


with open("day11.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_best_result(stuff):
    return f"{stuff}100"


def get_count(p_internal):
    contents = []
    for stuff in p_internal:
        best_result = get_best_result(stuff=stuff)
        contents.append(best_result)
        print(stuff, best_result)
    count = sum(map(int, contents))
    print(count)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()
raise ValueError()


def get_best_result2(stuff):
    return f"{stuff}200"


def get_count2(p_internal):
    contents = []
    for stuff in p_internal:
        best_result = get_best_result2(stuff=stuff)
        contents.append(best_result)
        print(stuff, best_result)
    count = sum(map(int, contents))
    print(count)


get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p)
print()
