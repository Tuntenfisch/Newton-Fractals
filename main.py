from numpy import array, clip

from vispy.app import Canvas, run, Timer, use_app
from vispy.gloo import Program
from vispy.visuals import LinePlotVisual, TextVisual

from newton_method import *


class CustomCanvas(Canvas):

    def __init__(self, vertex_shader, fragment_shader, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)

        self.program = Program(vertex_shader, fragment_shader)
        self.program['position'] = [(-1.0, -1.0), (-1.0, 1.0), (1.0, 1.0), (-1.0, -1.0), (1.0, 1.0), (1.0, -1.0)]
        self.program['resolution'] = self.physical_size
        self.program['center'] = self.center = array([0.0, 0.0])
        self.program['scale'] = self.scale = 2.5
        self.center_min, self.center_max = array([-10.0, -10.0]), array([10.0, 10.0])
        self.scale_min, self.scale_max = 10.0 ** -5.0, 10.0 ** 2.0

        self.line = LinePlotVisual(array([[-10, -10]]), color='white')
        self.text = TextVisual('', color='white', font_size=10, anchor_x='right', anchor_y='top')

        if use_app().backend_name == 'PyQt5':
            self._backend.leaveEvent = self.on_mouse_exit

        self.timer = Timer(connect=self.update, start=True)
        self.show()

    def on_draw(self, event):
        self.program.draw()
        self.line.draw()
        self.text.draw()

    def on_resize(self, event):
        self.program['resolution'] = self.physical_size
        self.line.transforms.configure(canvas=self, viewport=(0, 0, *self.physical_size))
        self.text.transforms.configure(canvas=self, viewport=(0, 0, *self.physical_size))

    def on_mouse_exit(self, event):
        self.line.set_data(array([[-10, -10]]))
        self.text.pos = (0.0, 0.0)

    def on_mouse_move(self, event):
        self.on_mouse_handler(event)

    def on_mouse_wheel(self, event):
        self.on_mouse_handler(event)

    def on_mouse_handler(self, event):
        if event.type == 'mouse_move' or event.type == 'mouse_wheel':
            position = self.pixel_coordinates_to_complex_coordinates(event.pos[0], event.pos[1])
            z_0 = complex(*position)
            z_n = newton_method(z_0, ACCURACY, MAX_ITERATIONS)

            # noinspection PyTypeChecker
            self.line.set_data(array([self.complex_coordinates_to_pixel_coordinates(*z) for z in z_n]), edge_width=0)
            self.text.text = '{:.3e}\n{:.3e}'.format(*self.pixel_coordinates_to_complex_coordinates(*event.pos))
            self.text.pos = event.pos + array([-5.0, -5.0])

            if event.is_dragging and event.buttons[0] == 1:
                self.translate(position - self.pixel_coordinates_to_complex_coordinates(event.last_event.pos[0], event.last_event.pos[1]))

            if event.type == 'mouse_wheel':
                factor = 0.9 if event.delta[1] > 0 else 1.0 / 0.9
                position = self.pixel_coordinates_to_complex_coordinates(event.pos[0], event.pos[1])
                self.zoom(factor)
                self.translate(self.pixel_coordinates_to_complex_coordinates(event.pos[0], event.pos[1]) - position)

    def translate(self, delta):
        self.program['center'] = self.center = clip(self.center - delta, self.center_min, self.center_max)

    def zoom(self, factor):
        self.program['scale'] = self.scale = clip(self.scale * factor, self.scale_min, self.scale_max)

    def pixel_coordinates_to_complex_coordinates(self, x, y):
        return array([self.scale * (x - 0.5 * self.size[0]) / self.size[0] + self.center[0], self.scale * (-y + 0.5 * self.size[1]) / self.size[0] + self.center[1]])

    def complex_coordinates_to_pixel_coordinates(self, x, y):
        return array([0.5 * self.size[0] + (x - self.center[0]) * self.size[0] / self.scale, (self.center[1] - y) * self.size[0] / self.scale + 0.5 * self.size[1]])


if __name__ == '__main__':
    custom_canvas = CustomCanvas(vertex_shader=open('newton_method.vert').read(), fragment_shader=open('newton_method.frag').read(), title='Fractals', size=(800, 800), keys='interactive')
    run()
