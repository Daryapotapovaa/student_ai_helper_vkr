# Задание: замыкания и фабрики функций

def make_multiplier(factor):
    def multiplier(x):
    return x * factor
    return multiplier


def make_power(exponent):
    def power(base):
        return base ** exponent
    return power


def compose(f, g):
    def composed(x):
        return f(g(x))
    return composed


double = make_multiplier(2)
triple = make_multiplier(3)
square = make_power(2)
cube = make_power(3)

double_then_square = compose(square, double)
triple_then_cube = compose(cube, triple)

values = [1, 2, 3, 4, 5]
print("x | double | square | double->square | triple->cube")
for x in values:
    print(f"{x} | {double(x):6} | {square(x):6} | {double_then_square(x):14} | {triple_then_cube(x):12}")
