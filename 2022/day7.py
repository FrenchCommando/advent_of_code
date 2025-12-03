import re
from utils.printing import display


with open("day7.txt", "r") as f:
    lines = f.readlines()


display(lines)

d_parent = dict()  # directory to parent - to enable navigation
d_size = dict()  # directory to size of files - value set during ls command
file_size = []
current_dir = None


class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.size = 0
        self.children = dict()


root = Node(name='root', parent=None)
node = root


for line_raw in lines:
    line = line_raw.strip()
    if line == "$ cd /":
        pass
    elif line == "$ cd ..":
        node = node.parent
    elif d := re.match(
        pattern=r"\$ cd (?P<dirname>.*)",
        string=line,
    ) is not None:
        d_group = re.match(
           pattern=r"\$ cd (?P<dirname>.*)",
           string=line,
        ).groupdict()
        node = node.children[d_group['dirname']]
    elif line == "$ ls":
        pass
    else:
        type_or_size, name_value = line.split(" ")
        if type_or_size == "dir":
            node.children[name_value] = Node(name=name_value, parent=node)
        else:
            size_value = int(type_or_size)
            node.size += size_value
            file_size.append((name_value, size_value))
            node_loop = node
            while node_loop.name != 'root':
                node_loop = node_loop.parent
                node_loop.size += size_value

display(d_parent)
display(d_size)
display(file_size)
display(root)
display(node)


threshold = 100000
count = 0


def increment_count_with_condition(n):
    global count
    if n.size <= threshold:
        count += n.size
    for n_child in n.children.values():
        increment_count_with_condition(n=n_child)


increment_count_with_condition(n=root)
display(count)


total_disk = 70000000
space_need = 30000000
space_to_free = space_need - (total_disk - root.size)
display(space_to_free)


candidate_value = root.size


def report_directory_deletion_candidate(n):
    global candidate_value
    if n.size >= space_to_free:
        if n.size < candidate_value:
            candidate_value = n.size
    for n_child in n.children.values():
        report_directory_deletion_candidate(n=n_child)


report_directory_deletion_candidate(n=root)
display(candidate_value)
