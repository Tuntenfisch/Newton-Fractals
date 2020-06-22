#version 130

#define PI 3.1415926535897932384626433832795
#define DISTINCT_COLOR_OFFSET 25
#define ACCURACY 0.01
#define MAX_ITERATIONS 50
#define F4

vec3[] distinct_colors = vec3[]
(
    vec3(  0.6627450980392157,  0.6627450980392157,   0.6627450980392157),
    vec3(  0.8627450980392157,  0.8627450980392157,   0.8627450980392157),
    vec3(  0.1843137254901961, 0.30980392156862746,  0.30980392156862746),
    vec3(  0.3333333333333333,  0.4196078431372549,   0.1843137254901961),
    vec3(  0.5450980392156862, 0.27058823529411763,  0.07450980392156863),
    vec3(  0.4196078431372549,  0.5568627450980392,  0.13725490196078433),
    vec3( 0.13333333333333333,  0.5450980392156862,  0.13333333333333333),
    vec3( 0.09803921568627451, 0.09803921568627451,   0.4392156862745098),
    vec3(  0.4392156862745098,  0.5019607843137255,   0.5647058823529412),
    vec3(  0.5450980392156862,                 0.0,                  0.0),
    vec3( 0.23529411764705882,  0.7019607843137254,  0.44313725490196076),
    vec3(  0.7372549019607844,  0.5607843137254902,   0.5607843137254902),
    vec3(                 0.4,                 0.2,                  0.6),
    vec3(  0.7215686274509804,  0.5254901960784314, 0.043137254901960784),
    vec3(  0.7411764705882353,  0.7176470588235294,   0.4196078431372549),
    vec3(                 0.0,  0.5450980392156862,   0.5450980392156862),
    vec3(   0.803921568627451,  0.5215686274509804,  0.24705882352941178),
    vec3( 0.27450980392156865,  0.5098039215686274,   0.7058823529411765),
    vec3(  0.8235294117647058,  0.4117647058823529,  0.11764705882352941),
    vec3(  0.6039215686274509,   0.803921568627451,  0.19607843137254902),
    vec3(   0.803921568627451,  0.3607843137254902,   0.3607843137254902),
    vec3(                 0.0,                 0.0,   0.5450980392156862),
    vec3( 0.19607843137254902,   0.803921568627451,  0.19607843137254902),
    vec3(  0.5607843137254902,  0.7372549019607844,   0.5607843137254902),
    vec3(  0.5019607843137255,                 0.0,   0.5019607843137255),
    vec3(  0.6901960784313725, 0.18823529411764706,   0.3764705882352941),
    vec3(  0.2823529411764706,  0.8196078431372549,                  0.8),
    vec3(                 1.0,                 0.0,                  0.0),
    vec3(                 1.0,  0.6470588235294118,                  0.0),
    vec3(                 1.0,  0.8431372549019608,                  0.0),
    vec3(  0.7803921568627451, 0.08235294117647059,   0.5215686274509804),
    vec3(                 0.0,                 0.0,    0.803921568627451),
    vec3(  0.8705882352941177,  0.7215686274509804,   0.5294117647058824),
    vec3(                 0.0,                 1.0,                  0.0),
    vec3(  0.5803921568627451,                 0.0,   0.8274509803921568),
    vec3(  0.7294117647058823,  0.3333333333333333,   0.8274509803921568),
    vec3(                 0.0,                 1.0,   0.4980392156862745),
    vec3(  0.2549019607843137,  0.4117647058823529,   0.8823529411764706),
    vec3(  0.8627450980392157,  0.0784313725490196,  0.23529411764705882),
    vec3(                 0.0,                 1.0,                  1.0),
    vec3(                 0.0,  0.7490196078431373,                  1.0),
    vec3(  0.5764705882352941,  0.4392156862745098,   0.8588235294117647),
    vec3(                 0.0,                 0.0,                  1.0),
    vec3(  0.6784313725490196,                 1.0,   0.1843137254901961),
    vec3(                 1.0, 0.38823529411764707,   0.2784313725490196),
    vec3(                 1.0,                 0.0,                  1.0),
    vec3(  0.8588235294117647,  0.4392156862745098,   0.5764705882352941),
    vec3(                 1.0,                 1.0,  0.32941176470588235),
    vec3( 0.39215686274509803,  0.5843137254901961,   0.9294117647058824),
    vec3(  0.8666666666666667,  0.6274509803921569,   0.8666666666666667),
    vec3(  0.5294117647058824,   0.807843137254902,   0.9215686274509803),
    vec3(                 1.0,  0.0784313725490196,   0.5764705882352941),
    vec3(                 1.0,  0.6274509803921569,  0.47843137254901963),
    vec3(  0.6862745098039216,  0.9333333333333333,   0.9333333333333333),
    vec3(  0.9333333333333333,  0.5098039215686274,   0.9333333333333333),
    vec3(   0.596078431372549,   0.984313725490196,    0.596078431372549),
    vec3(  0.4980392156862745,                 1.0,   0.8313725490196079),
    vec3(                 1.0,  0.4117647058823529,   0.7058823529411765),
    vec3(                 1.0,  0.8941176470588236,   0.7686274509803922),
    vec3(                 1.0,  0.7137254901960784,   0.7568627450980392)
);

uniform vec2 resolution;
uniform vec2 center;
uniform float scale;
uniform float time;

vec2 conjugate(vec2 z) {
    return vec2(z.x, -z.y);
}

vec2 multiply(vec2 z, vec2 w) {
    return vec2(z.x * w.x - z.y * w.y, z.x * w.y + z.y * w.x);
}

vec2 divide(vec2 z, vec2 w) {
    return multiply(z, conjugate(w) / dot(w, w));
}

vec2 power(vec2 z, int e) {
    vec2 w = vec2(1.0, 0.0);

    for (int _ = 0; _ < e; _++) {
        w = multiply(w, z);
    }
    return w;
}

vec2 sine(vec2 z) {
    return vec2(sin(z.x) * cosh(z.y), cos(z.x) * sinh(z.y));
}

vec2 cosine(vec2 z) {
    return vec2(cos(z.x) * cosh(z.y), -sin(z.x) * sinh(z.y));
}

#if defined F1
// f(z) = (z^2 - 1) * (z^2 + 1)
vec2 function(vec2 z) {
    return multiply(power(z, 2) + vec2(-1.0, 0.0), power(z, 2) + vec2(1.0, 0.0));
}

// f'(z) = 2z * ((z^2 - 1) + (z^2 + 1))
vec2 derivative(vec2 z) {
    return multiply(2.0 * z, (power(z, 2) + vec2(-1.0, 0.0)) + (power(z, 2) + vec2(1.0, 0.0)));
}

vec2[] roots = vec2[]
(
    vec2(-1.0,  0.0),
    vec2( 1.0,  0.0),
    vec2( 0.0, -1.0),
    vec2( 0.0,  1.0)
);
#elif defined F2
// f(z) = sin(z)
vec2 function(vec2 z) {
    return sine(z);
}

// f'(z) = cos(z)
vec2 derivative(vec2 z) {
    return cosine(z);
}

vec2[] roots = vec2[]
(
    vec2(-3.0 * PI, 0.0), 
    vec2(-2.0 * PI, 0.0),
    vec2(-1.0 * PI, 0.0), 
    vec2(      0.0, 0.0), 
    vec2( 1.0 * PI, 0.0), 
    vec2( 2.0 * PI, 0.0),
    vec2( 3.0 * PI, 0.0)
);
#elif defined F3
// f(z) = (z - 2) * (z - 0.5) * (z + 1.5) * (z + 2)
vec2 function(vec2 z) {
    return multiply(multiply(z + vec2(-2.0, 0.0), z + vec2(-0.5, 0.0)), multiply(z + vec2(1.5, 0.0), z + vec2(2.0, 0.0)));
}

// f'(z) = 4 * (z^3 + 0.75 * z^2 - 2.375 * z - 1)
vec2 derivative(vec2 z) {
    return 4.0 * (power(z, 3) + 0.75 * power(z, 2) - 2.375 * z - vec2(1.0, 0.0));
}

vec2[] roots = vec2[]
(
    vec2(-2.0, 0.0), 
    vec2(-1.5, 0.0), 
    vec2( 0.5, 0.0), 
    vec2( 2.0, 0.0)
);
#elif defined F4
// f(z) = z^3 + 1
vec2 function(vec2 z) {
    return power(z, 3) + vec2(1.0, 0.0);
}

// f'(z) = 3z^2
vec2 derivative(vec2 z) {
    return 3.0 * power(z, 2);
}

vec2[] roots = vec2[]
(
    vec2(-1.0,              0.0),
    vec2( 0.5,  0.5 * sqrt(3.0)),
    vec2( 0.5, -0.5 * sqrt(3.0))
);
#elif defined F5
// f(z) = z^14 - 5z^13 + 3z^12 - 8z^11 + 2z^10 + 2z^9 + 6z^8 - 7z^7 + 2z^6 + 6z^5 + 5z^4 + 8z^3 - 7z^2 - 7z + 10
vec2 function(vec2 z) {
    return power(z, 14) - 5.0 * power(z, 13) + 3.0 * power(z, 12) - 8.0 * power(z, 11) + 2.0 * power(z, 10) + 2.0 * power(z, 9) + 6.0 * power(z, 8) - 7.0 * power(z, 7) + 2.0 * power(z, 6) + 6.0 * power(z, 5) + 5.0 * power(z, 4) + 8.0 * power(z, 3) - 7.0 * power(z, 2) - 7.0 * z + vec2(10.0, 0.0);
}

// f(z) = 14z^13 - 65z^12 + 36z^11 - 88z^10 + 20z^9 + 18z^8 + 48z^7 - 49z^6 + 12z^5 + 30z^4 + 20z^3 + 24z^2 - 14z - 7
vec2 derivative(vec2 z) {
    return 14.0 * power(z, 13) - 65.0 * power(z, 12) + 36.0 * power(z, 11) - 88.0 * power(z, 10) + 20.0 * power(z, 9) + 18.0 * power(z, 8) + 48.0 * power(z, 7) - 49.0 * power(z, 6) + 12.0 * power(z, 5) + 30.0 * power(z, 4) + 20.0 * power(z, 3) + 24.0 * power(z, 2) - 14.0 * z - vec2(7.0, 0.0);
}

vec2[] roots = vec2[]
(
    vec2(    1.15154,       0.0),
    vec2(    4.69846,       0.0),
    vec2(  -0.873719,  0.242234),
    vec2(  -0.873719, -0.242234),
    vec2(  -0.825023,  0.750134),
    vec2(  -0.825023, -0.750134),
    vec2(  -0.229793,   1.01761),
    vec2(  -0.229793,  -1.01761),
    vec2( 0.09474819,   1.49687),
    vec2( 0.09474819,  -1.49687),
    vec2(   0.695535,  0.395332),
    vec2(   0.695535, -0.395332)
);
#elif defined F6
// f(z) = z^2 + 1
vec2 function(vec2 z) {
    return power(z, 2) + vec2(1.0, 0.0);
}

// f'(z) = 2z
vec2 derivative(vec2 z) {
    return 2.0 * z;
}

vec2[] roots = vec2[]
(
    vec2(0.0,  1.0),
    vec2(0.0, -1.0)
);
#endif

vec2 newton_step(vec2 z) {
    return divide(function(z), derivative(z));
}

int newton_method(vec2 z, float accuracy, int max_iterations, out int iterations) {
    for (int iteration = 0; iteration < max_iterations; iteration++) {
        for (int index = 0; index < roots.length(); index++) {
            if (distance(z, roots[index]) < accuracy) {
                iterations = iteration;

                return index;
            }
        }
        z = z - newton_step(z);
    }
    iterations = max_iterations;

    return roots.length();
}

void main()
{
    int iterations;

    vec2 z_0 = scale * (gl_FragCoord.xy - 0.5 * resolution.xy) / vec2(resolution.x, resolution.x) + center;
    vec3 color = distinct_colors[int(mod(newton_method(z_0, ACCURACY, MAX_ITERATIONS, iterations) + DISTINCT_COLOR_OFFSET, distinct_colors.length()))];

    gl_FragColor = vec4(pow(mix(1.0, 0.25, float(iterations) / MAX_ITERATIONS), 2.2) * color, 1.0);
}