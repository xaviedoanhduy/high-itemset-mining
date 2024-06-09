def main(a, b, c):
    delta = b**2 - 4 * a * c

    if delta < 0:
        print("Phương trình vô nghiệm!")
    elif delta == 0:
        x1 = x2 = -b / (2 * a)
        print(f"Phương trình có nghiệm kép x1 = x2 = {x1}")
    else:
        x1 = (-b + delta**0.5) / (2 * a)
        x2 = (-b - delta**0.5) / (2 * a)
        print(f"Phương trình có nghiệm x1 = {x1}")
        print(f"Phương trình có nghiệm x2 = {x2}")

main(1, -2, 1)
