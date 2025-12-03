from utils.printing import display


with open("day25.txt", "r") as f:
    lines = f.readlines()


lines = [line.strip() for line in lines]
display(lines)


snafu_digits = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}
digits_to_snafu = {v: k for k, v in snafu_digits.items()}


def snafu_to_decimal(x):
    if len(x) == 1:
        return snafu_digits[x]
    return snafu_to_decimal(x=x[:-1]) * 5 + snafu_to_decimal(x=x[-1])


def decimal_to_snafu(x):
    if x in digits_to_snafu:
        return digits_to_snafu[x]
    q, r = x // 5, x % 5
    if r == 4:
        q, r = q + 1, -1
    if r == 3:
        q, r = q + 1, -2
    return decimal_to_snafu(x=q) + digits_to_snafu[r]


print(f"{snafu_to_decimal(x='1=-0-2')=}")
print(f"{snafu_to_decimal(x='12111')=}")
print(f"{snafu_to_decimal(x='2=0=')=}")
print(f"{snafu_to_decimal(x='21')=}")
print(f"{snafu_to_decimal(x='2=01')=}")
print(f"{snafu_to_decimal(x='111')=}")
print(f"{snafu_to_decimal(x='20012')=}")
print(f"{snafu_to_decimal(x='112')=}")
print(f"{snafu_to_decimal(x='1=-1=')=}")
print(f"{snafu_to_decimal(x='1-12')=}")
print(f"{snafu_to_decimal(x='12')=}")
print(f"{snafu_to_decimal(x='1=')=}")
print(f"{snafu_to_decimal(x='122')=}")
print(f"{snafu_to_decimal(x='1')=}")
print(f"{snafu_to_decimal(x='2')=}")
print(f"{snafu_to_decimal(x='0')=}")
print(f"{snafu_to_decimal(x='-')=}")
print(f"{snafu_to_decimal(x='=')=}")
print()
print(f"{decimal_to_snafu(x=0)=}")
print(f"{decimal_to_snafu(x=1)=}")
print(f"{decimal_to_snafu(x=2)=}")
print(f"{decimal_to_snafu(x=3)=}")
print(f"{decimal_to_snafu(x=4)=}")
print(f"{decimal_to_snafu(x=5)=}")
print()

result = sum(snafu_to_decimal(x=line) for line in lines)
print(result)
print(decimal_to_snafu(x=result))
print()
