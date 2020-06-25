from collections import namedtuple

Function = namedtuple('Function', ['function_py', 'derivative_py', 'function_gl', 'derivative_gl', 'roots_gl'])

# noinspection LongLine
functions = [
    Function(
        function_py='z ** 3 + 1',
        derivative_py='3 * z ** 2',
        function_gl='power(z, 3) + VECTOR2(1.0, 0.0)',
        derivative_gl='3.0 * power(z, 2)',
        roots_gl='VECTOR2(-1.0, 0.0), VECTOR2(0.5, 0.5 * sqrt(3.0)), VECTOR2(0.5, -0.5 * sqrt(3.0))'),
    Function(
        function_py='(z ** 2 - 1) * (z ** 2 + 1)',
        derivative_py='2 * z * ((z ** 2 - 1) + (z ** 2 + 1))',
        function_gl='multiply(power(z, 2) + VECTOR2(-1.0, 0.0), power(z, 2) + VECTOR2(1.0, 0.0))',
        derivative_gl='multiply(2.0 * z, (power(z, 2) + VECTOR2(-1.0, 0.0)) + (power(z, 2) + VECTOR2(1.0, 0.0)))',
        roots_gl='VECTOR2(-1.0,  0.0), VECTOR2( 1.0,  0.0), VECTOR2( 0.0, -1.0), VECTOR2( 0.0,  1.0)'),
    Function(
        function_py='z ** 5 - 1',
        derivative_py='5 * z ** 4',
        function_gl='power(z, 5) - VECTOR2(1.0, 0.0)',
        derivative_gl='5.0 * power(z, 4)',
        roots_gl='VECTOR2(1.0, 0.0), VECTOR2(-0.809016994374947, 0.587785252292473), VECTOR2(-0.809016994374947, -0.587785252292473), VECTOR2(0.309016994374947, 0.951056516295154), VECTOR2(0.309016994374947, -0.951056516295154)'),
    Function(
        function_py='z ** 14 - 5 * z ** 13 + 3 * z ** 12 - 8 * z ** 11 + 2 * z ** 10 + 2 * z ** 9 + 6 * z ** 8 - 7 * z ** 7 + 2 * z ** 6 + 6 * z ** 5 + 5 * z ** 4 + 8 * z ** 3 - 7 * z ** 2 - 7 * z + 10',
        derivative_py='14 * z ** 13 - 65 * z ** 12 + 36 * z ** 11 - 88 * z ** 10 + 20 * z ** 9 + 18 * z ** 8 + 48 * z ** 7 - 49 * z ** 6 + 12 * z ** 5 + 30 * z ** 4 + 20 * z ** 3 + 24 * z ** 2 - 14 * z - 7',
        function_gl='power(z, 14) - 5.0 * power(z, 13) + 3.0 * power(z, 12) - 8.0 * power(z, 11) + 2.0 * power(z, 10) + 2.0 * power(z, 9) + 6.0 * power(z, 8) - 7.0 * power(z, 7) + 2.0 * power(z, 6) + 6.0 * power(z, 5) + 5.0 * power(z, 4) + 8.0 * power(z, 3) - 7.0 * power(z, 2) - 7.0 * z + VECTOR2(10.0, 0.0)',
        derivative_gl='14.0 * power(z, 13) - 65.0 * power(z, 12) + 36.0 * power(z, 11) - 88.0 * power(z, 10) + 20.0 * power(z, 9) + 18.0 * power(z, 8) + 48.0 * power(z, 7) - 49.0 * power(z, 6) + 12.0 * power(z, 5) + 30.0 * power(z, 4) + 20.0 * power(z, 3) + 24.0 * power(z, 2) - 14.0 * z - VECTOR2(7.0, 0.0)',
        roots_gl='VECTOR2(1.15154, 0.0), VECTOR2(4.69846, 0.0), VECTOR2(-0.873719, 0.242234), VECTOR2(-0.873719, -0.242234), VECTOR2(-0.825023, 0.750134), VECTOR2(-0.825023, -0.750134), VECTOR2(-0.229793, 1.01761), VECTOR2(-0.229793, -1.01761), VECTOR2(0.09474819, 1.49687), VECTOR2(0.09474819, -1.49687), VECTOR2(0.695535, 0.395332), VECTOR2(0.695535, -0.395332)')]
