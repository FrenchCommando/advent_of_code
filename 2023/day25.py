import queue
from utils.printing import display

example = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


with open("day25.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def parse(text):
    links = []
    for line in text:
        left, rights = line.split(": ")
        all_rights = rights.split(" ")
        for right in all_rights:
            links.append((left, right))
    return links


def solve(links):
    nodes = set(k for link in links for k in link)
    print("Nodes", len(nodes), nodes)
    connected = dict()
    for left, right in links:
        if left not in connected:
            connected[left] = {right}
        else:
            connected[left].add(right)
        if right not in connected:
            connected[right] = {left}
        else:
            connected[right].add(left)
    print("Connected", connected)

    n_ref = links[0][0]

    def collapse(item):
        # add node to inner_set when they have more than 3 connections
        # returns False if anything goes wrong (inner connected to outer)
        modified = True
        while modified:
            modified = False

            direct_connection_count = 0
            for n in item['inner_set']:
                for k in connected[n]:
                    if k in item['outer_set']:
                        direct_connection_count += 1
            if direct_connection_count > 3:
                return False

            connection_count = dict()
            for n in item['inner_set']:
                for k in connected[n]:
                    if k not in item['inner_set']:
                        if k not in connection_count:
                            connection_count[k] = 1
                        else:
                            connection_count[k] += 1

            high_count = {k for k in connection_count if connection_count[k] > 3}
            for k in high_count:
                if k in item['outer_set']:
                    return False

            outer_connection_count = dict()
            for n in item['outer_set']:
                for k in connected[n]:
                    if k not in item['outer_set']:
                        if k not in outer_connection_count:
                            outer_connection_count[k] = 1
                        else:
                            outer_connection_count[k] += 1

            outer_high_count = {k for k in outer_connection_count if outer_connection_count[k] > 3}
            for k in outer_high_count:
                if k in item['inner_set']:
                    return False

            if len(outer_high_count) > 0:
                modified = True
                for n in outer_high_count:
                    item['outer_set'].add(n)
            if len(high_count) > 0:
                modified = True
                for n in high_count:
                    item['inner_set'].add(n)

        return True

    def get_count(item):
        # definitions are consistent
        count = 0
        for n in item['inner_set']:
            for k in connected[n]:
                if k not in item['inner_set']:
                    count += 1
        return count

    def is_success(item):
        count = get_count(item=item)
        return count == 3

    def build_hypothesis(item):
        # choose an undecided node connected to the border
        # add it to either inner or outer
        candidate = None
        for n in item['inner_set']:
            for k in connected[n]:
                if k not in item['inner_set'] and k not in item['outer_set']:
                    candidate = k
                    break
            if candidate is not None:
                break
        if candidate is None:
            # print("Ran out of items, nothing to add")
            # print(item)
            return

        # print(candidate, item)
        item1 = dict(
            inner_set={*item['inner_set']}, outer_set={*item['outer_set'], candidate},
        )
        if collapse(item=item1):
            t_count1 = get_count(item=item1)
            t_item1_inner = tuple(item1['inner_set'])
            t_item1_outer = tuple(item1['outer_set'])
            q.put((t_count1 - len(t_item1_outer), t_item1_inner, t_item1_outer))

        item0 = dict(
            inner_set={*item['inner_set'], candidate}, outer_set={*item['outer_set']},
        )
        if collapse(item=item0):
            t_count0 = get_count(item=item0)
            t_item0_inner = tuple(item0['inner_set'])
            t_item0_outer = tuple(item0['outer_set'])
            q.put((t_count0 - len(t_item0_outer), t_item0_inner, t_item0_outer))
        # print(candidate)

    # q = queue.PriorityQueue()
    # q = queue.Queue()
    q = queue.LifoQueue()
    q.put((0, tuple({n_ref}), tuple()))

    q_count = 0

    while not q.empty():
        q_count += 1
        priority, inner, outer = q.get()
        d = dict(inner_set=set(inner), outer_set=set(outer))
        # if q_count > 1000000:
        #     break
        if q_count % 1000 == 0:
            print(
                q.qsize(),
                len(d['inner_set']) + len(d['outer_set']),
                len(d['inner_set']), len(d['outer_set']),
                q_count
            )
        # print(q.qsize(), len(d['inner_set']), len(d['outer_set']), q_count, d)
        # inner_set is connex
        # outer_set is not necessarily connex
        if is_success(item=d):
            nd = len(d['inner_set'])
            return nd * (len(nodes) - nd), nd, d
        build_hypothesis(item=d)
    return nodes, connected


# grid_value = example.split("\n")
grid_value = s
l_links = parse(text=grid_value)
l_solved = solve(links=l_links)
display(x=l_links)
display(x=l_solved)

# answer if 603xxx - I cleared it without recording it - can't reproduce
# I don't know how it's possible since the algo is not stochastic
# (603368, 796,  # wtf
# Christmas present? no idea what happened
