from utils.printing import display


examples = """\"\"
\"abc\"
\"aaa\\\"aaa\"
\"\\x27\""""


with open("day8.txt", "r") as f:
    s = f.readlines()
    display(s)


def get_count(p_internal):
    literal_count = 0
    string_count = 0

    for p in p_internal:
        lll = len(p)
        mmm = len(eval(p))
        # print(p, lll, mmm)
        literal_count += lll
        string_count += mmm

    print(literal_count, string_count, literal_count - string_count)


get_count(p_internal=[sss.strip() for sss in s])
print()
get_count(p_internal=examples.split("\n"))
print()


def get_count2(p_internal):
    literal_count = 0
    long_count = 0

    for p in p_internal:
        lll = len(p)
        c0 = p.count("\"")
        c1 = p.count("\\")
        mmm = lll + c0 + c1 + 2
        # print(p, lll, mmm)
        literal_count += lll
        long_count += mmm

    print(literal_count, long_count, long_count - literal_count)


get_count2(p_internal=[sss.strip() for sss in s])
print()
get_count2(p_internal=examples.split("\n"))
print()
