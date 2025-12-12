import queue

from utils.printing import display

example = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""


with open("day11.txt", "r") as f:
    s = f.readlines()
    display(s)


def parsed(l):
    return [ll.strip() for ll in l]


def get_count(p_internal):
    contents = dict()
    for stuff in p_internal:
        key, children = stuff.split(": ")
        l_children = children.split(" ")
        contents[key] = tuple(l_children)
    print(contents)

    paths = []
    q = queue.Queue()
    q.put(('you',))
    while not q.empty():
        path = q.get()
        last = path[-1]
        # print(path, last)
        for n in contents[last]:
            full_path = path + (n,)
            if n == 'out':
                paths.append(full_path)
                continue
            q.put(full_path)
    print(paths)
    count = len(paths)
    print(count)


p = parsed(l=example.split("\n"))
print(p)
print()
get_count(p_internal=parsed(l=s))
print()
get_count(p_internal=p)
print()



example2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


def get_count2(p_internal):
    contents = dict()
    for stuff in p_internal:
        key, children = stuff.split(": ")
        l_children = children.split(" ")
        contents[key] = tuple(l_children)
    print(contents)

    reverse_contents = dict()
    for key, children in contents.items():
        for child in children:
            if child not in reverse_contents:
                reverse_contents[child] = []
            reverse_contents[child].append(key)
    print(reverse_contents)

    def get_path_count(left, right, early, c):
        paths = []
        q = queue.LifoQueue()
        q.put((left,))
        while not q.empty():
            # print(q.qsize(), len(paths))
            path = q.get()
            last = path[-1]
            for n in c[last]:
                full_path = path + (n,)
                if n == right:
                    paths.append(full_path)
                    continue
                if n not in early:
                    q.put(full_path)
        # print(paths)
        count = len(paths)
        print(left, right, count)
        return count

    def get_node_list(left, right, early, c):
        nodes = set()
        q = queue.LifoQueue()
        q.put((left,))
        while not q.empty():
            path = q.get()
            last = path[-1]
            for n in c[last]:
                nodes.add(n)
                full_path = path + (n,)
                if n == right:
                    continue
                if n not in early:
                    q.put(full_path)
        # print(paths)
        count = len(nodes)
        print(left, right, count, nodes)
        return nodes

    c1 = get_path_count(left='fft', right='svr', early={}, c=reverse_contents)
    c3 = get_path_count(left='dac', right='out', early={}, c=contents)

    n1 = get_node_list(left='fft', right='svr', early={}, c=reverse_contents)
    n3 = get_node_list(left='dac', right='out', early={}, c=contents)
    nn = n1 | n3
    # print(len(n1), n1)
    # print(len(n3), n3)
    # print(len(nn), nn)
    # print(len(contents), len(reverse_contents))
    final_from, final_to = 'fft', 'dac'

    def filter_nodes_from_content(c):
        short_contents_internal = dict()
        for k, ccc in c.items():
            if k in nn:
                continue
            for cc in ccc:
                if cc in nn:
                    continue
                if k not in short_contents_internal:
                    short_contents_internal[k] = []
                short_contents_internal[k].append(cc)
        return short_contents_internal

    short_contents = filter_nodes_from_content(c=contents)
    # print(len(short_contents))
    short_nodes = {u for ccc in short_contents.values() for u in ccc}
    short_nodes.remove(final_to)
    short_nodes.add(final_from)
    while tuple(sorted(short_nodes)) != tuple(sorted(short_contents)):
        for nnn in short_nodes:
            if nnn == final_to:
                continue
            if nnn not in short_contents:
                # print("removing", nnn)
                nn.add(nnn)
        for nnn in short_contents:
            if nnn == final_from:
                continue
            if nnn not in short_nodes:
                # print("removing", nnn)
                nn.add(nnn)
        short_contents = filter_nodes_from_content(c=short_contents)
        short_nodes = {u for ccc in short_contents.values() for u in ccc}
        short_nodes.remove(final_to)
        short_nodes.add(final_from)
        # print(len(short_nodes), len(short_contents))
        # print(sorted(short_nodes))
        # print(sorted(short_contents))

    # print(short_contents['jta'])
    # print(contents['eym'])
    # print(short_contents['eym'])

    c2 = get_path_count(left='fft', right='dac', early=nn, c=short_contents)
    out = c1 * c2 * c3
    print(c1, c2, c3, out)


p2 = parsed(l=example2.split("\n"))
print(p2)
print()
get_count2(p_internal=parsed(l=s))
print()
get_count2(p_internal=p2)
print()
