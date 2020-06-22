from math import sqrt
from matplotlib import pyplot

distinct_color_offset = 25

distinct_colors = (
    '#a9a9a9ff',  # darkgray
    '#dcdcdcff',  # gainsboro
    '#2f4f4fff',  # darkslategray
    '#556b2fff',  # darkolivegreen
    '#8b4513ff',  # saddlebrown
    '#6b8e23ff',  # olivedrab
    '#228b22ff',  # forestgreen
    '#191970ff',  # midnightblue
    '#708090ff',  # slategray
    '#8b0000ff',  # darkred
    '#3cb371ff',  # mediumseagreen
    '#bc8f8fff',  # rosybrown
    '#663399ff',  # rebeccapurple
    '#b8860bff',  # darkgoldenrod
    '#bdb76bff',  # darkkhaki
    '#008b8bff',  # darkcyan
    '#cd853fff',  # peru
    '#4682b4ff',  # steelblue
    '#d2691eff',  # chocolate
    '#9acd32ff',  # yellowgreen
    '#cd5c5cff',  # indianred
    '#00008bff',  # darkblue
    '#32cd32ff',  # limegreen
    '#8fbc8fff',  # darkseagreen
    '#800080ff',  # purple
    '#b03060ff',  # maroon3
    '#48d1ccff',  # mediumturquoise
    '#ff0000ff',  # red
    '#ffa500ff',  # orange
    '#ffd700ff',  # gold
    '#c71585ff',  # mediumvioletred
    '#0000cdff',  # mediumblue
    '#deb887ff',  # burlywood
    '#00ff00ff',  # lime
    '#9400d3ff',  # darkviolet
    '#ba55d3ff',  # mediumorchid
    '#00ff7fff',  # springgreen
    '#4169e1ff',  # royalblue
    '#dc143cff',  # crimson
    '#00ffffff',  # aqua
    '#00bfffff',  # deepskyblue
    '#9370dbff',  # mediumpurple
    '#0000ffff',  # blue
    '#adff2fff',  # greenyellow
    '#ff6347ff',  # tomato
    '#ff00ffff',  # fuchsia
    '#db7093ff',  # palevioletred
    '#ffff54ff',  # laserlemon
    '#6495edff',  # cornflower
    '#dda0ddff',  # plum
    '#87ceebff',  # skyblue
    '#ff1493ff',  # deeppink
    '#ffa07aff',  # lightsalmon
    '#afeeeeff',  # paleturquoise
    '#ee82eeff',  # violet
    '#98fb98ff',  # palegreen
    '#7fffd4ff',  # aquamarine
    '#ff69b4ff',  # hotpink
    '#ffe4c4ff',  # bisque
    '#ffb6c1ff')  # lightpink


# f(z) = z^3 + 1
def function(z):
    return z ** 3.0 + 1.0


# f'(z) = 3z^2
def derivative(z):
    return 3.0 * z ** 2.0


roots = (complex(-1.0), complex(0.5, 0.5 * sqrt(3.0)), complex(0.5, -0.5 * sqrt(3.0)))


def newton_step(z):
    return function(z) / derivative(z)


def newton_method(z, accuracy, max_iterations):
    z_n, root_index = [z], len(roots)

    for iteration in range(max_iterations):
        for index in range(len(roots)):
            if abs(z - roots[index]) < accuracy:
                root_index = index

                break

        z = z - newton_step(z)
        z_n.append(z)

    return z_n, root_index


class EventHandler:

    def __init__(self, parent_axes):
        self.axes = parent_axes
        self.line = parent_axes.plot([None], [None], linestyle='--', marker='o')[0]

    def on_mouse_move(self, event):
        if not event.inaxes:
            return

        z_0 = complex(event.xdata, event.ydata)
        z_n, root_index = newton_method(z_0, 0.01, 50)

        self.line.set_xdata([z.real for z in z_n])
        self.line.set_ydata([z.imag for z in z_n])
        self.line.set_color(distinct_colors[root_index + distinct_color_offset])
        self.axes.figure.canvas.draw()


if __name__ == '__main__':
    figure, axes = pyplot.subplots()
    figure.canvas.set_window_title('Fractals')
    event_handler = EventHandler(axes)
    figure.canvas.mpl_connect('motion_notify_event', event_handler.on_mouse_move)
    axes.scatter([root.real for root in roots], [root.imag for root in roots], color=distinct_colors[distinct_color_offset:distinct_color_offset + len(roots)], marker='x')

    pyplot.xlim(-5.0, 5.0)
    pyplot.ylim(-5.0, 5.0)
    pyplot.grid()
    pyplot.show()
