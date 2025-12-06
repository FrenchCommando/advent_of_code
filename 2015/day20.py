from utils.printing import display



with open("day20.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p):
    n = int(p[0])
    print(n)

    n_over_10 = n // 10

    t = [0 for i in range(n_over_10 + 1)]
    k = 1
    candidate = n
    while k < candidate:
        i = 1
        while k * i <= n_over_10:
            t[k * i] += k * 10
            if t[k * i] >= n:
                candidate = min(candidate, k * i)
                # print(k * i, candidate)
                break
            i += 1
        k += 1
    print(candidate)

    print()


get_count(p=[sss.strip() for sss in s])
get_count(p=["100"])
print()


def get_count2(p):
    n = int(p[0])
    print(n)

    n_over_10 = n // 10

    t = [0 for i in range(n_over_10 + 1)]
    k = 1
    candidate = n
    while k < candidate:
        i = 1
        while k * i <= n_over_10 and i <= 50:
            t[k * i] += k * 11
            if t[k * i] >= n:
                candidate = min(candidate, k * i)
                # print(k * i, candidate)
                break
            i += 1
        k += 1
    print(candidate)

    print()


get_count2(p=[sss.strip() for sss in s])
print()
