from utils.printing import display

example = """199
200
208
210
200
207
240
269
260
263"""


with open("day1.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_best_result(stuff, previous):
    i_stuff = int(stuff)
    i_previous = int(previous)
    return i_stuff > i_previous


def get_count(p_internal):
    contents = []
    previous = None
    for stuff in p_internal:
        if previous is not None:
            best_result = get_best_result(stuff=stuff, previous=previous)
            contents.append(best_result)
            print(stuff, best_result)
        previous = stuff
    count = sum(map(int, contents))
    print(count)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()


def get_best_result2(stuff):
    return f"{stuff}200"


def get_count2(p_internal):
    m = list(map(int, p_internal))
    n = 3
    i0 = iter(m)
    i1 = iter(m[n:])
    count = 0
    while True:
        try:
            increment = next(i1) - next(i0)
            if increment > 0:
                count += 1
        except StopIteration:
            break
    print(count)


get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p)
print()
