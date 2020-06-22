ACCURACY = 0.01
MAX_ITERATIONS = 50


# f(z) = z^3 + 1
def function(z):
    return z ** 3.0 + 1.0


# f'(z) = 3z^2
def derivative(z):
    return 3.0 * z ** 2.0


def newton_step(z):
    return function(z) / derivative(z)


def newton_method(z, accuracy, max_iterations):
    z_n = [(z.real, z.imag)]

    for iteration in range(max_iterations):
        if abs(function(z)) < accuracy:
            break

        z = z - newton_step(z)
        z_n.append((z.real, z.imag))

    return z_n
