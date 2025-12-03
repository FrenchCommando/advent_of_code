import re
from utils.printing import display

example = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""



with open("day5.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
    i = iter(l)
    rules = []
    try:
        while True:
            line = next(i)
            if not line:
                break
            rules.append(line.strip().split("|"))
    except StopIteration:
        pass
    print(rules)

    d = dict()
    for left, right in rules:
        if left in d:
            d[left].append(right)
        else:
            d[left] = [right]
    print(d)

    def valid(book):
        for i_page, page in enumerate(book):
            previous = book[:i_page]
            rule_for_page = d.get(page, [])
            for candidate in previous:
                if candidate in rule_for_page:
                    return False
        return True

    c = 0
    try:
        while True:
            line = next(i)
            pages = line.split(",")
            if valid(pages):
                middle = int(pages[len(pages) // 2])
                # print(pages, middle)
                c += middle
    except StopIteration:
        pass
    return c

p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    i = iter(l)
    rules = []
    try:
        while True:
            line = next(i)
            if not line:
                break
            rules.append(line.strip().split("|"))
    except StopIteration:
        pass
    print(rules)

    d = dict()
    for left, right in rules:
        if left in d:
            d[left].append(right)
        else:
            d[left] = [right]
    print(d)

    def valid(book):
        for i_page, page in enumerate(book):
            previous = book[:i_page]
            rule_for_page = d.get(page, [])
            for candidate in previous:
                if candidate in rule_for_page:
                    return False
        return True

    def swap(book):
        for i_page, page in enumerate(book):
            previous = book[:i_page]
            rule_for_page = d.get(page, [])
            for j_page, candidate in enumerate(previous):
                if candidate in rule_for_page:
                    book[i_page], book[j_page] = book[j_page], book[i_page]
                    return False
        return True

    def order(book):
        while not swap(book):
            continue
        return book

    c = 0
    try:
        while True:
            line = next(i)
            pages = line.split(",")
            if not valid(pages):
                ordered = order(pages)
                middle = int(ordered[len(pages) // 2])
                # print(pages, middle)
                c += middle
    except StopIteration:
        pass
    return c

p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
