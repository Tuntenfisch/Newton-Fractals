from numpy import array, clip

from vispy.app import Canvas, run, Timer
from vispy.gloo import Program


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

        self.timer = Timer(connect=self.update, start=True)
        self.show()

    def on_draw(self, event):
        self.program.draw()

    def on_resize(self, event):
        self.program['resolution'] = self.physical_size

    def on_mouse_move(self, event):
        if event.is_dragging and event.buttons[0] == 1:
            old_position = self.pixel_coordinates_to_complex_coordinates(event.last_event.pos[0], event.last_event.pos[1])
            new_position = self.pixel_coordinates_to_complex_coordinates(event.pos[0], event.pos[1])
            self.translate(new_position - old_position)

    def on_mouse_wheel(self, event):
        factor = 0.9 if event.delta[1] > 0 else 1.0 / 0.9
        old_position = self.pixel_coordinates_to_complex_coordinates(event.pos[0], event.pos[1])
        self.zoom(factor)
        new_position = self.pixel_coordinates_to_complex_coordinates(event.pos[0], event.pos[1])
        self.translate(new_position - old_position)

    def translate(self, delta):
        self.program['center'] = self.center = clip(self.center - delta, self.center_min, self.center_max)

    def zoom(self, factor):
        self.program['scale'] = self.scale = clip(self.scale * factor, self.scale_min, self.scale_max)

    def pixel_coordinates_to_complex_coordinates(self, x, y):
        return array([self.scale * (x - 0.5 * self.size[0]) / self.size[0] + self.center[0], self.scale * (-y + 0.5 * self.size[1]) / self.size[0] + self.center[1]])


if __name__ == '__main__':
    fractal = CustomCanvas(vertex_shader=open('fractal.vert').read(), fragment_shader=open('fractal.frag').read(), title='Fractals', size=(1000, 1000), keys='interactive')
    run()
