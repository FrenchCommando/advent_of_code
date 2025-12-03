import math
import queue
import re


from utils.printing import display

example = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""


example2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


with open("day20.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def parse(text):
    out = dict()
    for line in text:
        if line == "":
            continue
        pattern = r"(?P<type>[&%]?)(?P<name>[a-z]+) -> (?P<directions>(.*))"
        d_group = re.match(
            pattern=pattern,
            string=line,
        ).groupdict()

        module_type = d_group['type']
        name = d_group['name']
        directions = d_group['directions'].split(", ")

        # print(line)
        # print(module_type, name, directions)
        # print()

        out[name] = (module_type, directions)
    out['output'] = "", []
    out['rx'] = "machine", []
    return out


def solve(grid, n, machine):
    high_count = 0
    low_count = 0

    def module_type_init(module_type):
        if module_type == "":
            return None
        if module_type == "%":
            return False
        return {}
    states = {
        name: module_type_init(module_type=module_type)
        for name, (module_type, directions) in grid.items()
    }
    for name, (module_type, directions) in grid.items():
        for direction in directions:
            if grid[direction][0] == "&":
                states[direction][name] = False

    machine_count = dict()

    def push_button(machine_run, index=None):
        nonlocal high_count, low_count
        q = queue.Queue()
        q.put(("button", "broadcaster", False))
        while not q.empty():
            origin_name, name, level = q.get()
            if machine_run:
                # print(origin_name, name, level)
                if grid[name][0] == "machine" and not level:
                    return True  # never happening

                if name in states['kh']:
                    for kkk in states[name]:
                        if all(states[kkk].values()):
                            if kkk not in machine_count:
                                machine_count[kkk] = index
                            if len(machine_count) == len(states['kh']):
                                return math.lcm(*(machine_count.values())), machine_count

            if level:
                high_count += 1
            else:
                low_count += 1
            module_type, directions = grid[name]
            if module_type == "":
                # this is the broadcaster
                for direction_name in directions:
                    q.put((name, direction_name, level))
            elif module_type == "%":
                if not level:
                    states[name] = not states[name]
                    for direction_name in directions:
                        q.put((name, direction_name, states[name]))
            elif module_type == "&":
                states[name][origin_name] = level
                # if name == 'pv':
                #     print(states['pv'])
                if all(states[name].values()):
                    for direction_name in directions:
                        q.put((name, direction_name, False))
                else:
                    for direction_name in directions:
                        q.put((name, direction_name, True))

    if machine:
        print(0, states['kh'])
        for k in states['kh']:
            print("\t", k, states[k])
            for kk in states[k]:
                print("\t\t", kk, states[kk])
        i = 1
        while True:
            button_output = push_button(machine_run=machine, index=i)
            if button_output is not None:
                return button_output
            i += 1
    else:
        for i in range(n):
            if push_button(machine_run=False) is not None:
                return i
            # print(states)

    return dict(low=low_count, high=high_count)


# grid_value = example.split("\n")
# grid_value = example2.split("\n")
grid_value = s
l_grid = parse(text=grid_value)
display(x=l_grid)
l_solved = solve(grid=l_grid, n=1000, machine=False)
display(x=l_solved)
display(x=math.prod(l_solved.values()))
l_solved_machine = solve(grid=l_grid, n=None, machine=True)
display(x=l_solved_machine)


# copy past all the sub-problems one by one
# hz 4079
# qh 3761
# xm 3931
# pv 4049

print(4079 * 3761 * 3931 * 4049)
