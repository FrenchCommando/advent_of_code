from utils.printing import display

example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


with open("day7.txt", "r") as f:
    s = f.readlines()
    display(s)


strength = {t: i for i, t in enumerate("23456789TJQKA", 2)}


def get_type(hand):
    c = hand[0]
    n = hand.count(c)
    if n == 5:
        return 7
    if n == 4:
        return 6
    h_bar = ''.join(filter(lambda x: x != c, hand))
    c1 = h_bar[0]
    n1 = h_bar.count(c1)
    if n1 == 4:
        return 6
    if n + n1 == 5:
        return 5
    h_bar2 = ''.join(filter(lambda x: x != c1, h_bar))
    c2 = h_bar2[0]
    n2 = h_bar2.count(c2)
    if n == 3 or n1 == 3 or n2 == 3:
        return 4
    if n + n1 + n2 == 5:
        return 3
    h_bar3 = ''.join(filter(lambda x: x != c2, h_bar2))
    c3 = h_bar3[0]
    n3 = h_bar3.count(c3)
    if max(n, n1, n2, n3) == 2:
        return 2
    return 1


def parse(text):
    data = []
    for line in text:
        left, right = line.strip().split(" ")
        data.append((left.strip(), int(right.strip())))
    return data


def get_key(hand):
    t = get_type(hand=hand)
    strengths = [strength[i] for i in hand]
    return tuple([t, *strengths])


def attribute(l_hands_to_score):
    data = []
    for hand, score in l_hands_to_score:
        key = get_key(hand=hand)
        data.append((key, score))
    return data


def check_type(hands):
    maps = {i: [] for i in range(1, 8)}
    for hand in hands:
        t = get_type(hand=hand)
        maps[t].append(hand)
    display(x=list(maps.values()))


def check_keys(hands):
    for hand in hands:
        key = get_key(hand=hand)
        print(key, hand)


hands_to_score = parse(text=example.split("\n"))
# hands_to_score = parse(text=s)

check_type(hands=[u[0] for u in hands_to_score])
# check_keys(hands=[u[0] for u in hands_to_score])


key_to_score = attribute(l_hands_to_score=hands_to_score)
s_scores = sorted(key_to_score)

display(x=hands_to_score)
display(x=key_to_score)
display(x=s_scores)
display(x=sum(i * t[-1] for i, t in enumerate(s_scores, 1)))

# 244091935 low
# 245896488 low
# 246097427 low

strength2 = {t: i for i, t in enumerate("J23456789TQKA", 1)}


def get_type2(hand):
    j_count = hand.count("J")
    if j_count == 0:
        return get_type(hand=hand)
    if j_count >= 4:
        return 7
    h_bar = ''.join(filter(lambda x: x != 'J', hand))
    c1 = h_bar[0]
    n1 = h_bar.count(c1)

    if j_count == 3:
        if n1 == 2:
            return 7
        return 6

    if j_count == 2:
        if n1 == 3:
            return 7
        if n1 == 2:
            return 6
        if h_bar[-2] == h_bar[-1]:
            return 6
        return 4  # 3 of a kind

    # j_count == 1
    if n1 == 4:
        return 7
    if n1 == 3:
        return 6
    h_bar2 = ''.join(filter(lambda x: x != c1, h_bar))
    c2 = h_bar2[0]
    n2 = h_bar2.count(c2)

    if n2 == 3:
        return 6
    if (n1, n2) == (2, 2):
        return 5
    h_bar3 = ''.join(filter(lambda x: x != c2, h_bar2))
    c3 = h_bar3[0]
    n3 = h_bar3.count(c3)

    if max(n1, n2, n3) == 2:
        return 4
    return 2


def get_key2(hand):
    t = get_type2(hand=hand)
    strengths = [strength2[i] for i in hand]
    return tuple([t, *strengths])


def attribute2(l_hands_to_score):
    data = []
    for hand, score in l_hands_to_score:
        key = get_key2(hand=hand)
        data.append((key, score))
    return data


def check_type2(hands):
    maps = {i: [] for i in range(1, 8)}
    for hand in hands:
        t = get_type2(hand=hand)
        maps[t].append(hand)
    display(x=list(maps.values()))


check_type2(hands=[u[0] for u in hands_to_score])

key_to_score2 = attribute2(l_hands_to_score=hands_to_score)
s_scores2 = sorted(key_to_score2)

display(x=key_to_score2)
display(x=s_scores2)
display(x=sum(i * t[-1] for i, t in enumerate(s_scores2, 1)))
