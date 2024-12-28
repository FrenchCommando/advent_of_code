import re
from utils.printing import display

example = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""



with open("day17.txt", "r") as f:
    s = f.readlines()
    display(s)


def count(l):
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

    print(register)
    print(numbers)

    combo = [0, 1, 2, 3, register['A'], register['B'], register['C'], None]
    print(combo)

    pointer = 0

    def instruction(opcode, literal_value):
        nonlocal pointer
        combo_value = combo[literal_value]
        print(pointer, opcode, literal_value, combo_value, combo)
        if opcode == 0:
            value_a = combo[4]
            value_divided = value_a >> combo_value
            combo[4] = value_divided
        elif opcode == 1:
            value_b = combo[5]
            value_xor = value_b ^ literal_value
            combo[5] = value_xor
        elif opcode == 2:
            combo[5] = combo_value % 8
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
            return combo_value % 8
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
            results.append(output)
        pointer += 2
        c += 1
        # if c > 10:
        #     break
    return ",".join(map(str, results))


p = count(l=example.split("\n"))
print("count", p)
ps = count(l=[line.strip() for line in s])
print("count", ps)


def count2(l):
    return 1


p2 = count2(l=example.split("\n"))
print("count2", p2)
ps2 = count2(l=[line.strip() for line in s])
print("count2", ps2)
