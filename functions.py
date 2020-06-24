from collections import namedtuple


Function = namedtuple('Function', ['function_py', 'derivative_py', 'function_gl', 'derivative_gl', 'roots_gl'])

functions = [
    Function(
        function_py='z ** 3 + 1',
        derivative_py='3 * z ** 2',
        function_gl='power(z, 3) + dvec2(1.0, 0.0)',
        derivative_gl='3.0 * power(z, 2)',
        roots_gl='dvec2(-1.0, 0.0), dvec2(0.5, 0.5 * sqrt(3.0)), dvec2(0.5, -0.5 * sqrt(3.0))'),
    Function(
        function_py='(z ** 2 - 1) * (z ** 2 + 1)',
        derivative_py='2 * z * ((z ** 2 - 1) + (z ** 2 + 1))',
        function_gl='multiply(power(z, 2) + dvec2(-1.0, 0.0), power(z, 2) + dvec2(1.0, 0.0))',
        derivative_gl='multiply(2.0 * z, (power(z, 2) + dvec2(-1.0, 0.0)) + (power(z, 2) + dvec2(1.0, 0.0)))',
        roots_gl='dvec2(-1.0,  0.0), dvec2( 1.0,  0.0), dvec2( 0.0, -1.0), dvec2( 0.0,  1.0)')]
