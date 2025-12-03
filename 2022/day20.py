from utils.printing import display


with open("day20.txt", "r") as f:
    lines = f.readlines()


lines = [int(line.strip()) for line in lines]
display(lines)


def mixing(i_lines, i_state):
    for i, value in i_lines:
        index_start = i_state.index((i, value))
        insert_index = (index_start + value) % (len(i_state) - 1)
        # if insert_index == 0:
        #     insert_index = len(l_state) - 1
        i_state.pop(index_start)
        i_state.insert(insert_index, (i, value))
        # print(l_state)
    return i_state


def get_nth(n, l_state, zero_index_value):
    index_zero = l_state.index((zero_index_value, 0))
    n_index = (index_zero + n) % len(l_state)
    return l_state[n_index][1]


zero_index = lines.index(0)
l_lines = list(enumerate(lines))
state = l_lines.copy()
# display(state)
state = mixing(i_lines=l_lines, i_state=state)
# display(state)
print()
print(get_nth(n=1000, l_state=state, zero_index_value=zero_index))
print(get_nth(n=2000, l_state=state, zero_index_value=zero_index))
print(get_nth(n=3000, l_state=state, zero_index_value=zero_index))
print()
print(
    sum(
        get_nth(n=n_value, l_state=state, zero_index_value=zero_index)
        for n_value in [1000, 2000, 3000]
    )
)


factor = 811589153
m_lines = [i * factor for i in lines]
l_lines = list(enumerate(m_lines))
m_state = l_lines.copy()
# display(m_state)
for i in range(10):
    # print(i)
    m_state = mixing(i_lines=l_lines, i_state=m_state)
print()
print(get_nth(n=1000, l_state=m_state, zero_index_value=zero_index))
print(get_nth(n=2000, l_state=m_state, zero_index_value=zero_index))
print(get_nth(n=3000, l_state=m_state, zero_index_value=zero_index))
print()
print(
    sum(
        get_nth(n=n_value, l_state=m_state, zero_index_value=zero_index)
        for n_value in [1000, 2000, 3000]
    )
)
