import copy
import queue
import re

from utils.printing import display

example = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


with open("day19.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def parse(text):
    i_text = iter(text)
    workflows = dict()

    def parse_condition(condition):
        pattern = r"(?P<category>([xmas]))(?P<relation>([<>]))(?P<value>([0-9]+)):(?P<destination>[a-zAR]+)"
        d = re.fullmatch(pattern=pattern, string=condition).groupdict()
        d['value'] = int(d['value'])
        return d['value'], d['category'], d['relation'], d['destination']

    def parse_line_workflow(one_line):
        pattern = r"(?P<name>([a-z]+)){(?P<conditions>(.*)),(?P<last>[a-zAR]+)}"
        d = re.fullmatch(pattern=pattern, string=one_line).groupdict()
        workflows[d['name']] = (list(map(parse_condition, d['conditions'].split(","))), d['last'])

    def parse_line_part(one_line):
        pattern = r"{x=(?P<x>([0-9]+)),m=(?P<m>([0-9]+)),a=(?P<a>([0-9]+)),s=(?P<s>([0-9]+))}"
        d = re.fullmatch(pattern=pattern, string=one_line).groupdict()
        parts.append(dict(x=int(d['x']), m=int(d['m']), a=int(d['a']), s=int(d['s'])))

    line = next(i_text)
    while line != "":
        parse_line_workflow(one_line=line)
        line = next(i_text)

    parts = []
    try:
        while True:
            line = next(i_text)
            parse_line_part(one_line=line)
    except StopIteration:
        pass

    return workflows, parts


def apply_condition(condition, part):
    value, category, relation, destination = condition
    part_value = part[category]
    if relation == "<":
        if part_value < value:
            return True, destination
        return False, None
    else:
        if part_value > value:
            return True, destination
        return False, None


def inner_solve(workflows, part):
    result = "in"
    while result not in {"A", "R"}:
        # print(result)
        conditions, destination = workflows[result]
        success = False
        for condition in conditions:
            out_b, out_destination = apply_condition(condition=condition, part=part)
            if out_b:
                result = out_destination
                success = True
                break
        if not success:
            result = destination
    return result == "A"


def solve(workflows, parts):
    out_parts = []
    for part in parts:
        if inner_solve(workflows=workflows, part=part):
            out_parts.append(part)
    return out_parts


grid_value = example.split("\n")
# grid_value = s
l_workflows, l_parts = parse(text=grid_value)
display(x=l_workflows)
display(x=l_parts)
l_accepted = solve(workflows=l_workflows, parts=l_parts)
display(x=l_accepted)
display(x=[sum(l_part.values()) for l_part in l_accepted])
display(x=sum(sum(l_part.values()) for l_part in l_accepted))


def solve2(workflows):
    q = queue.Queue()
    value_min = 1
    value_max = 4000
    q.put((dict(
        x=dict(min=value_min, max=value_max),
        m=dict(min=value_min, max=value_max),
        a=dict(min=value_min, max=value_max),
        s=dict(min=value_min, max=value_max),
    ), 'in'))

    def count_size(d):
        return (
                (d['x']['max'] - d['x']['min'] + 1) *
                (d['m']['max'] - d['m']['min'] + 1) *
                (d['a']['max'] - d['a']['min'] + 1) *
                (d['s']['max'] - d['s']['min'] + 1)
        )

    accepted = []
    rejected = []

    while not q.empty():
        # print(len(accepted), len(rejected), q.qsize())
        ranges, position = q.get()
        # print(ranges, position)
        conditions, last = workflows[position]
        success = False
        for condition in conditions:
            value, category, relation, destination = condition
            selected_range = ranges[category]
            if relation == "<":
                if selected_range['max'] < value:
                    success = True
                    if destination == "A":
                        accepted.append(ranges)
                    elif destination == "R":
                        rejected.append(ranges)
                    else:
                        q.put((ranges, destination))
                    break
                elif selected_range['min'] >= value:
                    continue
                else:
                    dict_up = copy.deepcopy(ranges)
                    dict_up[category]['min'] = value
                    dict_down = copy.deepcopy(ranges)
                    dict_down[category]['max'] = value - 1
                    q.put((dict_up, position))
                    q.put((dict_down, position))
                    success = True
                    break
            else:
                if selected_range['min'] > value:
                    success = True
                    if destination == "A":
                        accepted.append(ranges)
                    elif destination == "R":
                        rejected.append(ranges)
                    else:
                        q.put((ranges, destination))
                    break
                elif selected_range['max'] <= value:
                    continue
                else:
                    dict_up = copy.deepcopy(ranges)
                    dict_up[category]['min'] = value + 1
                    dict_down = copy.deepcopy(ranges)
                    dict_down[category]['max'] = value
                    q.put((dict_up, position))
                    q.put((dict_down, position))
                    success = True
                    break
        if not success:
            if last == "A":
                accepted.append(ranges)
            elif last == "R":
                rejected.append(ranges)
            else:
                q.put((ranges, last))

    # print("Accepted")
    # for dd in accepted:
    #     print(dd)

    # print("Rejected")
    # for dd in rejected:
    #     print(dd)
    # print()

    return sum(count_size(d=a) for a in accepted)


def clean_up(workflows):
    modified = True
    while modified:
        print("numberofworkflows", len(workflows))
        r_list = []
        a_list = []
        for k, (conditions, last) in workflows.items():
            if last == "R":
                if all(map(lambda dddd: dddd['destination'] == "R", conditions)):
                    r_list.append(k)
            if last == "A":
                if all(map(lambda dddd: dddd['destination'] == "A", conditions)):
                    a_list.append(k)
        modified = len(r_list) != 0 or len(a_list) != 0
        for a in a_list:
            # print(a, a_list)
            del workflows[a]
        for r in r_list:
            # print(r, r_list)
            del workflows[r]

        def replace_function(name):
            if name in r_list:
                return "R"
            if name in a_list:
                return "A"
            return name

        for k, (conditions, last) in workflows.items():
            workflows[k] = (conditions, replace_function(name=last))
            for ddd in conditions:
                ddd['destination'] = replace_function(name=ddd['destination'])


def clean_up_last(workflows):
    print("numberofworkflows cleanuplast", len(workflows))
    for k, (conditions, last) in workflows.items():
        while last == conditions[-1]['destination']:
            # print(k, conditions)
            conditions.pop()
            # print(conditions, last)


def clean_up_cycle(workflows):
    print("numberofworkflows cleanupcycle", len(workflows))
    seen = {"in", "A", "R"}
    q = queue.Queue()
    q.put("in")
    while not q.empty():
        w = q.get()
        conditions, destination = workflows[w]
        for condition in conditions:
            inner_destination = condition['destination']
            if inner_destination not in seen:
                seen.add(inner_destination)
                q.put(inner_destination)
        if destination not in seen:
            seen.add(destination)
            q.put(destination)
    for w in workflows.copy():
        if w not in seen:
            del workflows[w]
    print("numberofworkflows cleanupcycle end", len(workflows))


def reduce_grid(text):
    i_text = iter(text)
    workflows = dict()

    def parse_condition(condition):
        pattern = r"(?P<first>(.*)):(?P<destination>[a-zAR]+)"
        d = re.fullmatch(pattern=pattern, string=condition).groupdict()
        return dict(first=d['first'], destination=d['destination'])

    def parse_line_workflow(one_line):
        pattern = r"(?P<name>([a-z]+)){(?P<conditions>(.*)),(?P<last>[a-zAR]+)}"
        d = re.fullmatch(pattern=pattern, string=one_line).groupdict()
        workflows[d['name']] = (list(map(parse_condition, d['conditions'].split(","))), d['last'])

    line = next(i_text)
    while line != "":
        parse_line_workflow(one_line=line)
        line = next(i_text)

    clean_up(workflows=workflows)
    clean_up_last(workflows=workflows)
    clean_up_cycle(workflows=workflows)
    print()

    out = [
        f"{k}{{{','.join(f'{ddd['first']}:{ddd['destination']}' for ddd in conditions)},{last}}}"
        for k, (conditions, last) in workflows.items()
    ]
    out.append("")
    # for i in out:
    #     print(i)
    # print(out[0])
    return out


# grid_value = example.split("\n")
grid_value = s
grid_value = reduce_grid(text=grid_value)
l_workflows, l_parts = parse(text=grid_value)
display(x=l_workflows)
l_workflows_solved = solve2(workflows=l_workflows)
display(x=l_workflows_solved)
