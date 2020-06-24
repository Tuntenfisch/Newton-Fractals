import re

from numpy import array, clip, dot
from vispy.app import Canvas, run, Timer, use_app
from vispy.gloo import Program
from vispy.visuals import LinePlotVisual, TextVisual

from functions import functions
from newton_method import newton_method


class FractalCanvas(Canvas):

    @property
    def fragment_shader(self):
        replacements = {
            '#define FUNCTION(z) (vec2(0.0, 0.0))': f'#define FUNCTION(z) ({self.functions[self.function_index].function_gl})',
            '#define DERIVATIVE(z) (vec2(1.0, 0.0))': f'#define DERIVATIVE(z) ({self.functions[self.function_index].derivative_gl})',
            '#define ROOTS (vec2[](vec2(0.0, 0.0)))': f'#define ROOTS (vec2[]({self.functions[self.function_index].roots_gl}))'
        }
        return re.compile('|'.join(re.escape(key) for key in replacements.keys())).sub(lambda match: replacements[match.group(0)], self.fragment_shader_template)

    @property
    def function_info(self):
        return f'f(z)  = {self.functions[self.function_index].function_py.replace(" ** ", "^").replace("*", "·")}\n' + \
               f'f\'(z) = {self.functions[self.function_index].derivative_py.replace(" ** ", "^").replace("*", "·")}'

    @property
    def pixel_to_complex_transform(self):
        return array([
            [self.scale / self.size[0], 0.0, -0.5 * self.scale / self.size[0] * self.size[0] + self.center[0]],
            [0.0, -self.scale / self.size[0], 0.5 * self.scale / self.size[0] * self.size[1] + self.center[1]],
            [0.0, 0.0, 1.0]])

    @property
    def complex_to_pixel_transform(self):
        return array([
            [self.size[0] / self.scale, 0.0, -self.size[0] / self.scale * self.center[0] + 0.5 * self.size[0]],
            [0.0, -self.size[0] / self.scale, self.size[0] / self.scale * self.center[1] + 0.5 * self.size[1]],
            [0.0, 0.0, 1.0]])

    # noinspection PyShadowingNames
    def __init__(self, vertex_shader, fragment_shader_template, functions, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vertex_shader = vertex_shader
        self.fragment_shader_template = fragment_shader_template
        self.functions = functions
        self.function_index = 0

        self.program = Program(self.vertex_shader, self.fragment_shader)
        self.program['position'] = [(-1.0, -1.0), (-1.0, 1.0), (1.0, 1.0), (-1.0, -1.0), (1.0, 1.0), (1.0, -1.0)]
        self.program['resolution'] = self.physical_size
        self.program['center'] = self.center = array([0.0, 0.0])
        self.program['scale'] = self.scale = 2.5
        self.center_min, self.center_max = array([-10.0, -10.0]), array([10.0, 10.0])
        self.scale_min, self.scale_max = 10.0 ** -5.0, 10.0 ** 2.0

        self.line = LinePlotVisual(array([[-10, -10]]), color='white')
        self.position_text = TextVisual('', color='white', font_size=10, anchor_x='right', anchor_y='top')
        self.iterations_text = TextVisual('', color='white', font_size=10, anchor_x='left', anchor_y='top')
        self.function_info_text = TextVisual(self.function_info, pos=(5, 5), color='white', font_size=10, anchor_x='left', anchor_y='bottom')

        if use_app().backend_name == 'PyQt5':
            self._backend.leaveEvent = self.on_mouse_exit

        self.timer = Timer(connect=self.update, start=True)
        self.show()

    def on_draw(self, event):
        self.program.draw()
        self.line.draw()
        self.position_text.draw()
        self.iterations_text.draw()
        self.function_info_text.draw()

    def on_resize(self, event):
        self.program['resolution'] = self.physical_size
        self.line.transforms.configure(canvas=self, viewport=(0, 0, *self.physical_size))
        self.position_text.transforms.configure(canvas=self, viewport=(0, 0, *self.physical_size))
        self.iterations_text.transforms.configure(canvas=self, viewport=(0, 0, *self.physical_size))
        self.function_info_text.transforms.configure(canvas=self, viewport=(0, 0, *self.physical_size))

    def on_mouse_exit(self, event):
        self.on_mouse_handler('mouse_exit', event)

    def on_mouse_move(self, event):
        self.on_mouse_handler('mouse_move', event)

    def on_mouse_release(self, event):
        self.on_mouse_handler('mouse_release', event)

    def on_mouse_wheel(self, event):
        self.on_mouse_handler('mouse_wheel', event)

    def on_mouse_handler(self, event_type, event):
        if event_type == 'mouse_move' or event_type == 'mouse_wheel':
            if event.type == 'mouse_wheel':
                self.zoom(0.9 if event.delta[1] > 0.0 else 1.0 / 0.9, event.pos)

            self.newton_method(event.pos)

            if event.is_dragging and event.buttons[0] == 1:
                new_position_complex = dot(self.pixel_to_complex_transform, array([[event.pos[0]], [event.pos[1]], [1.0]]))
                old_position_complex = dot(self.pixel_to_complex_transform, array([[event.last_event.pos[0]], [event.last_event.pos[1]], [1.0]]))
                self.translate((new_position_complex - old_position_complex)[:2].flatten())
        elif event_type == 'mouse_release':
            if event.last_event.is_dragging:
                return

            old_function_index = self.function_index
            self.function_index = (self.function_index + (1 if event.button == 1 else (-1 if event.button == 2 else 0))) % len(self.functions)
            new_function_index = self.function_index

            if new_function_index != old_function_index:
                self.program.set_shaders(vert=self.vertex_shader, frag=self.fragment_shader)
                self.newton_method(event.pos)
                self.function_info_text.text = self.function_info

        elif event_type == 'mouse_exit':
            self.line.set_data(array([[-10, -10]]))
            self.position_text.pos = (0, 0)
            self.iterations_text.pos = (0, 0)

    def newton_method(self, position_pixel):
        position_complex = dot(self.pixel_to_complex_transform, array([[position_pixel[0]], [position_pixel[1]], [1.0]]))
        z_0 = complex(*position_complex[:2].flatten())
        z_n, iterations = newton_method(z=z_0, function_string=self.functions[self.function_index].function_py, derivative_string=self.functions[self.function_index].derivative_py)

        # noinspection PyTypeChecker
        self.line.set_data(array([dot(self.complex_to_pixel_transform, array([[z[0]], [z[1]], [1.0]]))[:2].flatten() for z in z_n]), edge_width=0)
        self.position_text.text = '{:.3e}\n{:.3e}'.format(*position_complex[:2].flatten())
        self.position_text.pos = position_pixel + array([-5, -5])
        self.iterations_text.text = f'\n{iterations}'
        self.iterations_text.pos = dot(self.complex_to_pixel_transform, array([[z_n[-1][0]], [z_n[-1][1]], [1.0]]))[:2].flatten() + array([5, -5])

    def translate(self, delta_complex):
        self.program['center'] = self.center = clip(self.center - delta_complex, self.center_min, self.center_max)

    def zoom(self, factor, position_pixel):
        old_position_complex = dot(self.pixel_to_complex_transform, array([[position_pixel[0]], [position_pixel[1]], [1.0]]))
        self.program['scale'] = self.scale = clip(self.scale * factor, self.scale_min, self.scale_max)
        new_position_complex = dot(self.pixel_to_complex_transform, array([[position_pixel[0]], [position_pixel[1]], [1.0]]))
        self.translate((new_position_complex - old_position_complex)[:2].flatten())


if __name__ == '__main__':
    fractal_canvas = FractalCanvas(
        vertex_shader=open('newton_method.vert').read(),
        fragment_shader_template=open('newton_method.frag').read(),
        functions=functions,
        title='Fractals',
        size=(800, 800),
        keys='interactive')

    run()
