import queue

from utils.printing import display


with open("day22.txt", "r") as f:
    s = f.readlines()
    display(s)


spells_specs = {
    "Magic Missile": (53, 4),   # damage
    "Drain": (73, 2, 2),        # damage, heal
    "Shield": (113, 6, 7),      # armor
    "Poison": (173, 6, 3),      # damage
    "Recharge": (229, 5, 101),  # mana
    "Wait": (0,),
}


def get_count(p, n_h, n_m, hard):
    boss = dict()
    for line in p:
        entry, value = line.split(": ", 1)
        boss[entry] = int(value)
    print(boss)
    boss_h = boss["Hit Points"]
    # boss_h = 17
    # boss_h -= 10
    boss_d = boss["Damage"]
    # boss_h, boss_d = n_h, n_m

    best_mana_for_state = dict()

    min_boss_h = 1e10
    best_mana = 1e10
    best_used = None
    q = queue.PriorityQueue()
    # mana used | hit | mana | boss-hit | shield left | poison left | recharge left
    q.put((0, (0, n_h, n_m, boss_h, 0, 0, 0, tuple())))
    while not q.empty():
        _, (i_m_u, i_n_h, i_n_m, i_b_h, i_s_l, i_p_l, i_r_l, i_used) = q.get()
        if i_m_u > best_mana:
            continue
        state = i_n_h, i_n_m, i_b_h, i_s_l, i_p_l, i_r_l
        if state in best_mana_for_state:
            state_value = best_mana_for_state[state]
            if state_value <= i_m_u:
                continue
        best_mana_for_state[state] = i_m_u

        # print(q.qsize(), len(best_mana_for_state), i_m_u, i_n_h, i_n_m, i_b_h, i_s_l, i_p_l, i_r_l, i_used)
        # allow do nothing if Poison or Recharge
        spells = ["Magic Missile", "Drain", "Shield", "Poison", "Recharge"]
        # if i_s_l != 0 or i_p_l != 0 or i_r_l != 0:
        #     spells.append("Wait")

        if hard:
            i_n_h -= 1
            if i_n_h <= 0:  # pre-dead
                # print("Pre-Dead", i_m_u, i_n_h, i_n_m, i_b_h, i_s_l, i_p_l, i_r_l, i_used)
                continue

        if i_p_l:
            i_b_h -= spells_specs["Poison"][2]
        if i_r_l:
            i_n_m += spells_specs["Recharge"][2]
        i_s_l = max(0, i_s_l - 1)
        i_p_l = max(0, i_p_l - 1)
        i_r_l = max(0, i_r_l - 1)

        for spell in spells:
            i_used_p = i_used + (spell, )
            i_m_u_p = i_m_u + spells_specs[spell][0]

            i_b_h_p = i_b_h
            i_n_m_p = i_n_m - spells_specs[spell][0]
            i_n_h_p = i_n_h

            i_s_l_p = i_s_l
            i_p_l_p = i_p_l
            i_r_l_p = i_r_l

            if i_n_m_p < 0:  # not enough mana
                continue

            if spell == "Magic Missile":
                i_b_h_p -= spells_specs[spell][1]
            elif spell == "Drain":
                i_b_h_p -= spells_specs[spell][1]
                i_n_h_p += spells_specs[spell][2]
            elif spell == "Shield":
                if i_s_l_p > 0:
                    continue
                i_s_l_p = spells_specs[spell][1]
            elif spell == "Poison":
                if i_p_l_p > 0:
                    continue
                i_p_l_p = spells_specs[spell][1]
            elif spell == "Recharge":
                if i_r_l_p > 0:
                    continue
                i_r_l_p = spells_specs[spell][1]
            elif spell == "Wait":
                pass
            else:
                raise ValueError("Unknown spell %s" % spell)

            if i_b_h_p <= min_boss_h:
                # print(i_b_h_p, i_m_u_p, i_n_h_p, i_n_m_p, i_b_h_p, i_s_l_p, i_p_l_p, i_r_l_p, i_used_p)
                min_boss_h = i_b_h_p
            # print(i_b_h_p, i_n_h_p, i_m_u_p)
            min_boss_h = min(min_boss_h, i_b_h_p)
            # print(min_boss_h, end="\t")
            if i_b_h_p <= 0:  # won
                print("Won", i_m_u_p, i_n_h_p, i_n_m_p, i_b_h_p, i_s_l_p, i_p_l_p, i_r_l_p, i_used_p)
                if i_m_u_p <= best_mana:
                    best_mana = i_m_u_p
                    best_used = i_used_p
                continue

            armor = spells_specs["Shield"][2] if i_s_l_p else 0
            b_d = max(1, boss_d - armor)
            if i_p_l_p:
                i_b_h_p -= spells_specs["Poison"][2]
            if i_r_l_p:
                i_n_m_p += spells_specs["Recharge"][2]

            i_s_l_p = max(0, i_s_l_p - 1)
            i_p_l_p = max(0, i_p_l_p - 1)
            i_r_l_p = max(0, i_r_l_p - 1)

            i_n_h_p -= b_d

            if i_b_h_p <= 0:  # won
                print("Won", i_m_u_p, i_n_h_p, i_n_m_p, i_b_h_p, i_s_l_p, i_p_l_p, i_r_l_p, i_used_p)
                if i_m_u_p <= best_mana:
                    best_mana = i_m_u_p
                    best_used = i_used_p
                continue

            if i_n_h_p <= 0:  # dead
                # print("Dead", i_m_u_p, i_n_h_p, i_n_m_p, i_b_h_p, i_s_l_p, i_p_l_p, i_r_l_p, i_used_p)
                continue

            q.put((i_b_h_p + i_n_m_p, (i_m_u_p, i_n_h_p, i_n_m_p, i_b_h_p, i_s_l_p, i_p_l_p, i_r_l_p, i_used_p)))

    print()
    # print(best_mana_for_state)
    print(best_mana, best_used)
    print()


get_count(p=[sss.strip() for sss in s], n_h=50, n_m=500, hard=False)
print()


get_count(p=[sss.strip() for sss in s], n_h=50, n_m=500, hard=True)
print()
