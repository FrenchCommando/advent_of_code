import itertools
import re

from utils.printing import display


shop = """Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3"""


with open("day21.txt", "r") as f:
    s = f.readlines()
    display(s)


def win(n_h, damage, armor, boss_h, boss_d, boss_a):
    boss_hit_damage = max(1, boss_d - armor)
    me_hit_damage = max(1, damage - boss_a)
    c_boss, cc_boss = divmod(n_h, boss_hit_damage)
    c_me, cc_me = divmod(boss_h, me_hit_damage)
    w_boss = c_boss + (1 if cc_boss else 0)
    w_me = c_me + (1 if cc_me else 0)
    return w_me <= w_boss


def get_count(p, n_h, n_w, n_a, n_r):
    boss = dict()
    for line in p:
        entry, value = line.split(": ", 1)
        boss[entry] = int(value)
    print(boss)

    weapons_str, armors_str, rings_str = shop.split("\n\n")
    weapons = dict()
    for entry in weapons_str.split("\n")[1:]:
        name = entry.split(" ")[0]
        specs = re.findall(r"(\d+)", entry)
        weapons[name] = tuple(map(int, specs))
    armors = dict()
    for entry in armors_str.split("\n")[1:]:
        name = entry.split(" ")[0]
        specs = re.findall(r"(\d+)", entry)
        armors[name] = tuple(map(int, specs))
    rings = dict()
    for entry in rings_str.split("\n")[1:]:
        name = " ".join(entry.split(" ")[:2])
        specs = re.findall(r"(\d+)", entry[len(name) + 1:])
        rings[name] = tuple(map(int, specs))
    print(weapons)
    print(armors)
    print(rings)

    best_gold = 1000
    for i_w in n_w:
        for w_s in itertools.combinations(weapons, i_w):
            w_specs = [weapons[ww] for ww in w_s]
            for i_a in n_a:
                for a_s in itertools.combinations(armors, i_a):
                    a_specs = [armors[aa] for aa in a_s]
                    for i_r in n_r:
                        for r_s in itertools.combinations(rings, i_r):
                            r_specs = [rings[rr] for rr in r_s]
                            cost = sum(sss[0] for sss in itertools.chain(w_specs, a_specs, r_specs))
                            damage = sum(sss[1] for sss in itertools.chain(w_specs, a_specs, r_specs))
                            armor = sum(sss[2] for sss in itertools.chain(w_specs, a_specs, r_specs))

                            if win(n_h, damage, armor, boss["Hit Points"], boss['Damage'], boss['Armor']):
                                best_gold = min(cost, best_gold)

    print(best_gold)
    print()


get_count(p=[sss.strip() for sss in s], n_h=100, n_w=(1,), n_a=(0, 1), n_r=(0, 1, 2))
print()

def get_count2(p, n_h, n_w, n_a, n_r):
    boss = dict()
    for line in p:
        entry, value = line.split(": ", 1)
        boss[entry] = int(value)
    print(boss)

    weapons_str, armors_str, rings_str = shop.split("\n\n")
    weapons = dict()
    for entry in weapons_str.split("\n")[1:]:
        name = entry.split(" ")[0]
        specs = re.findall(r"(\d+)", entry)
        weapons[name] = tuple(map(int, specs))
    armors = dict()
    for entry in armors_str.split("\n")[1:]:
        name = entry.split(" ")[0]
        specs = re.findall(r"(\d+)", entry)
        armors[name] = tuple(map(int, specs))
    rings = dict()
    for entry in rings_str.split("\n")[1:]:
        name = " ".join(entry.split(" ")[:2])
        specs = re.findall(r"(\d+)", entry[len(name) + 1:])
        rings[name] = tuple(map(int, specs))
    print(weapons)
    print(armors)
    print(rings)

    best_gold = 0
    for i_w in n_w:
        for w_s in itertools.combinations(weapons, i_w):
            w_specs = [weapons[ww] for ww in w_s]
            for i_a in n_a:
                for a_s in itertools.combinations(armors, i_a):
                    a_specs = [armors[aa] for aa in a_s]
                    for i_r in n_r:
                        for r_s in itertools.combinations(rings, i_r):
                            r_specs = [rings[rr] for rr in r_s]
                            cost = sum(sss[0] for sss in itertools.chain(w_specs, a_specs, r_specs))
                            damage = sum(sss[1] for sss in itertools.chain(w_specs, a_specs, r_specs))
                            armor = sum(sss[2] for sss in itertools.chain(w_specs, a_specs, r_specs))

                            if not win(n_h, damage, armor, boss["Hit Points"], boss['Damage'], boss['Armor']):
                                best_gold = max(cost, best_gold)

    print(best_gold)
    print()


get_count2(p=[sss.strip() for sss in s], n_h=100, n_w=(1,), n_a=(0, 1), n_r=(0, 1, 2))
print()
