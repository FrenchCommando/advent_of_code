from utils.printing import display


with open("day3.txt", "r") as f:
    lines = f.readlines()


display(lines)
# display([score(s=s) for s in lines])
print(ord('a'))
print(ord('A'))


def common_item_from_sack(sack):
    n = len(sack)
    n_half = n // 2
    left, right = sack[:n_half], sack[n_half:]
    # display(left)
    # display(right)
    for u in left:
        if u in right:
            return u


display(common_item_from_sack(sack="abtnnb"))


def priority_from_item(item):
    letter = item.lower()
    value = ord(letter) - ord('a') + 1
    if item != letter:
        return value + 26
    return value


display(priority_from_item(item="A"))
display(priority_from_item(item="a"))

display(sum(
    priority_from_item(item=common_item_from_sack(sack=line))
    for line in lines
))


def common_item_from_group(elf1, elf2, elf3):
    for u in elf1:
        if u in elf2:
            if u in elf3:
                return u


display(common_item_from_group(
    elf1="vJrwpWtwJgWrhcsFMMfFFhFp",
    elf2="jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    elf3="PmmdzqPrVvPwwTWBwg",
))

display(common_item_from_group(
    elf1="wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    elf2="ttgJtRGJQctTZtZT",
    elf3="CrZsJsPPZsGzwwsLwLmpwMDw",
))


display(sum(
    priority_from_item(item=common_item_from_group(
        elf1=item1,
        elf2=item2,
        elf3=item3,
    ))
    for (item1, item2, item3) in zip(*[iter(lines)] * 3)
))
