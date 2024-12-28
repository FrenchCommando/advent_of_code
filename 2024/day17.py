import re
from utils.printing import display

example = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""



with open("day17.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l, a_override=None):
    register = dict()
    i = iter(l)
    line = next(i)
    while line:
        reg, value = re.findall("Register (\w): (\d+)", line)[0]
        register[reg] = int(value)
        line = next(i)

    program_line = next(i)
    l_numbers = re.findall("Program: (.+)", program_line)[0]
    numbers = list(map(int, l_numbers.split(",")))

    if a_override is not None:
        register['A'] = a_override
    print(register)
    print(numbers)
    print([bin(u) for u in numbers])

    combo = [0, 1, 2, 3, register['A'], register['B'], register['C'], None]
    print(combo)

    pointer = 0

    def instruction(opcode, literal_value):
        nonlocal pointer
        combo_value = combo[literal_value]
        print(pointer, opcode, literal_value, combo_value, combo, '\t', combo[4], combo[5], combo[6])
        print('\t\t\t', bin(combo[4]), bin(combo[5]), bin(combo[6]))
        if opcode == 0:
            value_a = combo[4]
            value_divided = value_a >> combo_value
            combo[4] = value_divided
        elif opcode == 1:
            value_b = combo[5]
            value_xor = value_b ^ literal_value
            combo[5] = value_xor
        elif opcode == 2:
            combo[5] = combo_value & 0b111
        elif opcode == 3:
            value_a = combo[4]
            if value_a == 0:
                return
            pointer = literal_value - 2
        elif opcode == 4:
            value_b = combo[5]
            value_c = combo[6]
            value_xor = value_b ^ value_c
            combo[5] = value_xor
        elif opcode == 5:
            return combo_value & 0b111
        elif opcode == 6:
            value_a = combo[4]
            value_divided = value_a >> combo_value
            combo[5] = value_divided
        elif opcode == 7:
            value_a = combo[4]
            value_divided = value_a >> combo_value
            combo[6] = value_divided

    results = []
    c = 0
    while len(numbers) > pointer + 1 :
        output = instruction(opcode=numbers[pointer], literal_value=numbers[pointer+1])
        if output is not None:
            print('\t', output, '\t\t', bin(output))
            results.append(output)
        pointer += 2
        c += 1
        # if c > 10:
        #     break
    print('\t  ', ",".join(map(str, numbers)))
    return ",".join(map(str, results))


example2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)
print()


p2 = count(l=example2.split("\n"), a_override=117440)
print("count2", p2)
ps2 = count(l=[line.strip() for line in s], a_override=0b101110101011)  # test any number
print("count2", ps2)


def count2(l):
    register = dict()
    i = iter(l)
    line = next(i)
    while line:
        reg, value = re.findall("Register (\w): (\d+)", line)[0]
        register[reg] = int(value)
        line = next(i)

    program_line = next(i)
    l_numbers = re.findall("Program: (.+)", program_line)[0]
    numbers = list(map(int, l_numbers.split(",")))

    def solve(a):
        combo = [0, 1, 2, 3, register['A'], register['B'], register['C'], None]
        combo[4] = a

        pointer = 0

        def instruction(opcode, literal_value):
            nonlocal pointer
            combo_value = combo[literal_value]
            # print(pointer, opcode, literal_value, combo_value, combo, '\t', combo[4], combo[5], combo[6])
            # print('\t\t\t', bin(combo[4]), bin(combo[5]), bin(combo[6]))
            if opcode == 0:
                value_a = combo[4]
                value_divided = value_a >> combo_value
                combo[4] = value_divided
            elif opcode == 1:
                value_b = combo[5]
                value_xor = value_b ^ literal_value
                combo[5] = value_xor
            elif opcode == 2:
                combo[5] = combo_value & 0b111
            elif opcode == 3:
                value_a = combo[4]
                if value_a == 0:
                    return
                pointer = literal_value - 2
            elif opcode == 4:
                value_b = combo[5]
                value_c = combo[6]
                value_xor = value_b ^ value_c
                combo[5] = value_xor
            elif opcode == 5:
                return combo_value & 0b111
            elif opcode == 6:
                value_a = combo[4]
                value_divided = value_a >> combo_value
                combo[5] = value_divided
            elif opcode == 7:
                value_a = combo[4]
                value_divided = value_a >> combo_value
                combo[6] = value_divided

        results = []
        c = 0
        while len(numbers) > pointer + 1 :
            output = instruction(opcode=numbers[pointer], literal_value=numbers[pointer+1])
            if output is not None:
                # print('\t', output, '\t\t', bin(output))
                results.append(output)
            pointer += 2
            c += 1
        return results

    r = 0
    number_index = len(numbers) - 1
    while number_index >= 0:
        for candidate in range(8):
            r_candidate = r * 8 + candidate
            out = solve(a=r_candidate)
            print(number_index, bin(r_candidate), out)
            if all(left == right for left, right in zip(numbers[number_index:], out)):
                r = r_candidate
                number_index -= 1
                break
    return r


ps22 = count2(l=[line.strip() for line in s])
print("count22", ps22)
