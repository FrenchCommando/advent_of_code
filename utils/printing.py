def display(x):
    print(f"{x}\t{type(x)}")
    if isinstance(x, list):
        print(f"\tlength {len(x)}")


if __name__ == '__main__':
    my_object = [1, 3, 6]
    display(x=my_object)
    my_object2 = 100
    display(x=my_object2)
