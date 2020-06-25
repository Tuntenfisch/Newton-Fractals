#version 120

#define DOUBLE_PRECISION

#if defined DOUBLE_PRECISION
    #extension GL_ARB_gpu_shader_fp64 : enable
    #define PACK_DOUBLE(vector) (double(vector.x) + double(vector.y))
    #define VECTOR2 dvec2
    #define VECTOR3 dvec3
    #define MATRIX3X3 dmat3x3
#else
    #extension GL_ARB_gpu_shader_fp64 : disable
    #define PACK_DOUBLE(vector) (vector.x)
    #define VECTOR2 vec2
    #define VECTOR3 vec3
    #define MATRIX3X3 mat3x3
#endif

#define PI (3.1415926535897932384626433832795)
#define DISTINCT_COLOR_OFFSET (25)
#define ACCURACY (0.01)
#define MAX_ITERATIONS (50)
#define FUNCTION(z) (VECTOR2(0.0, 0.0))
#define DERIVATIVE(z) (VECTOR2(1.0, 0.0))
#define ROOTS (VECTOR2[](VECTOR2(0.0, 0.0)))

vec3[] distinct_colors = vec3[]
(
    vec3( 0.6627450980392157,  0.6627450980392157,   0.6627450980392157),
    vec3( 0.8627450980392157,  0.8627450980392157,   0.8627450980392157),
    vec3( 0.1843137254901961, 0.30980392156862746,  0.30980392156862746),
    vec3( 0.3333333333333333,  0.4196078431372549,   0.1843137254901961),
    vec3( 0.5450980392156862, 0.27058823529411763,  0.07450980392156863),
    vec3( 0.4196078431372549,  0.5568627450980392,  0.13725490196078433),
    vec3(0.13333333333333333,  0.5450980392156862,  0.13333333333333333),
    vec3(0.09803921568627451, 0.09803921568627451,   0.4392156862745098),
    vec3( 0.4392156862745098,  0.5019607843137255,   0.5647058823529412),
    vec3( 0.5450980392156862,                 0.0,                  0.0),
    vec3(0.23529411764705882,  0.7019607843137254,  0.44313725490196076),
    vec3( 0.7372549019607844,  0.5607843137254902,   0.5607843137254902),
    vec3(                0.4,                 0.2,                  0.6),
    vec3( 0.7215686274509804,  0.5254901960784314, 0.043137254901960784),
    vec3( 0.7411764705882353,  0.7176470588235294,   0.4196078431372549),
    vec3(                0.0,  0.5450980392156862,   0.5450980392156862),
    vec3(  0.803921568627451,  0.5215686274509804,  0.24705882352941178),
    vec3(0.27450980392156865,  0.5098039215686274,   0.7058823529411765),
    vec3( 0.8235294117647058,  0.4117647058823529,  0.11764705882352941),
    vec3( 0.6039215686274509,   0.803921568627451,  0.19607843137254902),
    vec3(  0.803921568627451,  0.3607843137254902,   0.3607843137254902),
    vec3(                0.0,                 0.0,   0.5450980392156862),
    vec3(0.19607843137254902,   0.803921568627451,  0.19607843137254902),
    vec3( 0.5607843137254902,  0.7372549019607844,   0.5607843137254902),
    vec3( 0.5019607843137255,                 0.0,   0.5019607843137255),
    vec3( 0.6901960784313725, 0.18823529411764706,   0.3764705882352941),
    vec3( 0.2823529411764706,  0.8196078431372549,                  0.8),
    vec3(                1.0,                 0.0,                  0.0),
    vec3(                1.0,  0.6470588235294118,                  0.0),
    vec3(                1.0,  0.8431372549019608,                  0.0),
    vec3( 0.7803921568627451, 0.08235294117647059,   0.5215686274509804),
    vec3(                0.0,                 0.0,    0.803921568627451),
    vec3( 0.8705882352941177,  0.7215686274509804,   0.5294117647058824),
    vec3(                0.0,                 1.0,                  0.0),
    vec3( 0.5803921568627451,                 0.0,   0.8274509803921568),
    vec3( 0.7294117647058823,  0.3333333333333333,   0.8274509803921568),
    vec3(                0.0,                 1.0,   0.4980392156862745),
    vec3( 0.2549019607843137,  0.4117647058823529,   0.8823529411764706),
    vec3( 0.8627450980392157,  0.0784313725490196,  0.23529411764705882),
    vec3(                0.0,                 1.0,                  1.0),
    vec3(                0.0,  0.7490196078431373,                  1.0),
    vec3( 0.5764705882352941,  0.4392156862745098,   0.8588235294117647),
    vec3(                0.0,                 0.0,                  1.0),
    vec3( 0.6784313725490196,                 1.0,   0.1843137254901961),
    vec3(                1.0, 0.38823529411764707,   0.2784313725490196),
    vec3(                1.0,                 0.0,                  1.0),
    vec3( 0.8588235294117647,  0.4392156862745098,   0.5764705882352941),
    vec3(                1.0,                 1.0,  0.32941176470588235),
    vec3(0.39215686274509803,  0.5843137254901961,   0.9294117647058824),
    vec3( 0.8666666666666667,  0.6274509803921569,   0.8666666666666667),
    vec3( 0.5294117647058824,   0.807843137254902,   0.9215686274509803),
    vec3(                1.0,  0.0784313725490196,   0.5764705882352941),
    vec3(                1.0,  0.6274509803921569,  0.47843137254901963),
    vec3( 0.6862745098039216,  0.9333333333333333,   0.9333333333333333),
    vec3( 0.9333333333333333,  0.5098039215686274,   0.9333333333333333),
    vec3(  0.596078431372549,   0.984313725490196,    0.596078431372549),
    vec3( 0.4980392156862745,                 1.0,   0.8313725490196079),
    vec3(                1.0,  0.4117647058823529,   0.7058823529411765),
    vec3(                1.0,  0.8941176470588236,   0.7686274509803922),
    vec3(                1.0,  0.7137254901960784,   0.7568627450980392)
);

uniform vec2 resolution;
uniform vec4 center;
uniform vec2 scale;

VECTOR2 conjugate(VECTOR2 z) {
    return VECTOR2(z.x, -z.y);
}

VECTOR2 multiply(VECTOR2 z, VECTOR2 w) {
    return VECTOR2(z.x * w.x - z.y * w.y, z.x * w.y + z.y * w.x);
}

VECTOR2 divide(VECTOR2 z, VECTOR2 w) {
    return multiply(z, conjugate(w) / dot(w, w));
}

VECTOR2 power(VECTOR2 z, int e) {
    VECTOR2 w = VECTOR2(1.0, 0.0);

    for (int _ = 0; _ < e; _++) {
        w = multiply(w, z);
    }
    return w;
}

int newton_method(VECTOR2 z, out int iterations) {
    iterations = MAX_ITERATIONS;

    for (int iteration = 0; iteration < MAX_ITERATIONS; iteration++) {
        if (length(FUNCTION(z)) < ACCURACY) {
            iterations = iteration;

            for (int index = 0; index < ROOTS.length; index++) {
                if (distance(z, ROOTS[index]) < ACCURACY) {
                    return index;
                }
            }
            return ROOTS.length;
        }
        z = z - divide(FUNCTION(z), DERIVATIVE(z));
    }
    return ROOTS.length;
}

void main()
{
    int iterations;

    MATRIX3X3 pixel_to_complex_transform = transpose(MATRIX3X3
    (
        PACK_DOUBLE(scale) / resolution.x,                                0.0,                               PACK_DOUBLE(center.xy) - 0.5 * PACK_DOUBLE(scale),
                                      0.0, -PACK_DOUBLE(scale) / resolution.x, 0.5 * resolution.y / resolution.x * PACK_DOUBLE(scale) - PACK_DOUBLE(center.zw),
                                      0.0,                                0.0,                                                                             1.0
    ));

    VECTOR2 z_0 = (pixel_to_complex_transform * vec3(gl_FragCoord.xy, 1.0)).xy;
    vec3 color = distinct_colors[int(mod(newton_method(z_0, iterations) + DISTINCT_COLOR_OFFSET, distinct_colors.length()))];

    gl_FragColor = vec4(pow(mix(1.0, 0.25, float(iterations) / MAX_ITERATIONS), 2.2) * color, 1.0);
}