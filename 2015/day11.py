from utils.printing import display


examples = [
    # "hijklmmn",
    # "abbceffg",
    # "abbcegjk",
    "abcdefgh",  # abcdffaa
    "ghijklmn",  # ghjaabcc
]

with open("day11.txt", "r") as f:
    s = f.readlines()
    display(s)


bad_c = [ord(c) - ord('a') for c in 'iol']


def apply(v):
    v[-1] += 1
    i = -1
    while v[i] == 26:
        v[i] = 0
        v[i - 1] += 1
        i -= 1

    for i, c in enumerate(v):
        if c in bad_c:
            v[i] += 1
            for j in range(i+1, len(v)):
                v[j] = 0


def is_valid1(dv):
    for i in range(len(dv) - 1):
        if dv[i] == -1:
            if dv[i + 1] == -1:
                return True
    return False


def is_valid2(dv):
    m0 = None
    for i in range(len(dv)):
        if dv[i] == 0:
            if m0 is None:
                m0 = i
            else:
                if m0 + 2 <= i:
                    return True
    return False


def is_valid(v):
    dv = [a - b for a, b in zip(v, v[1:])]
    v1 = is_valid1(dv=dv)
    if not v1:
        return False
    v2 = is_valid2(dv=dv)
    return v2


def get_count(p_internal):
    for p in p_internal:
        v = [ord(c) - ord('a') for c in p]
        print(v)
        while not is_valid(v):
            apply(v)
            # print(v)
        print(''.join(chr(c + ord('a')) for c in v))
        print(len(v), p, v)
        print()



get_count(p_internal=[sss.strip() for sss in s])
print()
get_count(p_internal=[sss.strip() for sss in examples])
print()

get_count(p_internal=["cqjxxzaa"])
print()
