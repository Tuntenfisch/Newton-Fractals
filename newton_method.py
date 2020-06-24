ACCURACY = 0.01
MAX_ITERATIONS = 50


def newton_method(z, function_string, derivative_string):
    z_n, iterations = [(z.real, z.imag)], MAX_ITERATIONS

    for iteration in range(MAX_ITERATIONS):
        if abs(eval(function_string)) < ACCURACY:
            iterations = iteration

            break

        z = z - eval(function_string) / eval(derivative_string)
        z_n.append((z.real, z.imag))

    return z_n, iterations
