from utils.printing import display

example = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


with open("day15.txt", "r") as f:
    s = list(map(lambda u: u.strip(), f.readlines()))
    display(s)


def parse(line):
    return line.split(",")


def convert(code):
    value = 0
    for c in code:
        a = ord(c)
        value += a
        value *= 17
        value %= 256
    # print(code, value)
    return value


def bucket(items):
    buckets = [[] for i in range(256)]
    for item in items:
        if "-" in item:
            label = item[:-1]
            h = convert(code=label)
            buckets[h].append(("-", label))
        else:
            label_focal = item.split("=")

            label = label_focal[0]
            h = convert(code=label)
            focal = int(label_focal[-1])
            buckets[h].append((focal, label))
    return buckets


l_items = parse(line=example)
# l_items = parse(line=s[0])
l_converted = [convert(code=item) for item in l_items]
display(x=sum(l_converted))

l_buckets = bucket(items=l_items)

for l_i, l_b in enumerate(l_buckets):
    if l_b:
        print(l_i, l_b)


def process(buckets):
    result = []
    for i, bucket_operations in enumerate(buckets, 1):
        if bucket_operations:
            # print(i, bucket_operations)
            last_focal = dict()
            for focal, label in bucket_operations:
                if focal != "-":
                    last_focal[label] = focal
            # print("LastFocal", last_focal)
            contents = []
            for operation, label in bucket_operations:
                if operation == "-":
                    if label in contents:
                        contents.remove(label)
                else:
                    if label not in contents:
                        contents.append(label)
            score = sum(
                position * last_focal[label] for position, label in enumerate(contents, 1)
            )
            result.append(i * score)
    return result


l_processed = process(buckets=l_buckets)
print(l_processed)
display(x=sum(l_processed))
