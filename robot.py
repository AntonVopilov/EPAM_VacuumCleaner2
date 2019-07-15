from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_F1, KEY_F2
import body


class Robot:
    """
    Возвращает объект роботы
    x, y - начальное положение
    width - ширина робота
    length - длинная робота
    """

    def __init__(self, x, y, width, length):

        self.x_position = x
        self.y_position = y
        self.width = width
        self.length = length

        self._way = [(x, y)]
        self.collision = False

        self.hurdles_points = []

        # тело робота
        self._body = body.Body(self.x_position, self.y_position, width, length)
        self._prev_body = None
        # граница тела робота по направлению движения (движение вверх - _body._top_bounder)
        self._head_bounder = None

        # направление робота
        self.directions = ['right', 'top', 'left', 'bottom']
        # робот смотрит направо
        self.direct_indx = 0

        # соответсвие комманд и методов
        self.move_dict = {
            KEY_UP: self.up,
            KEY_DOWN: self.down,
            KEY_LEFT: self.left,
            KEY_RIGHT: self.right,
            KEY_F1: self.rotate_counterclockwise,
            KEY_F2: self.rotate_clockwise
        }

    def set_hudler_points(self, hurdlers_points):
        """
        Метод добавляет координаты препятсвий
        """
        self.hurdles_points = hurdlers_points

    def right(self):
        """
        Метод двигает робота вправо (увеличивает координату x)
        """
        self._head_bounder = self._body._right_bounder
        self._head_bounder += [self._body._top_bounder[-1], self._body._bottom_bounder[-1]]
        self.x_position += 1

    def left(self):
        """
        Метод двигает робота влево (уменьшает координату x)
        """
        self._head_bounder = self._body._left_bounder
        self._head_bounder += [self._body._top_bounder[0], self._body._bottom_bounder[0]]
        self.x_position -= 1

    def up(self):
        """
        Метод двигает робота вверх (уменьшает координату y)
        """
        self._head_bounder = self._body._top_bounder
        self.y_position -= 1

    def down(self):
        """
        Метод двигает робота ввниз (увеличивает координату y)
        """
        self._head_bounder = self._body._bottom_bounder
        self.y_position += 1

    def rotate_counterclockwise(self):
        """
        Метод вращает робота против часовой стрелки
        """
        self.length, self.width = self.width, self.length
        self.direct_indx += 1
        self.direct_indx = self.direct_indx % 4

    def rotate_clockwise(self):
        """
        Метод вращает робота против часовой стрелки
        """
        self.length, self.width = self.width, self.length
        self.direct_indx -= 1
        self.direct_indx = self.direct_indx % 4

    def make_move(self, command):
        """
        Метод используется для движения по карте с препятствиями
        command = KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_F1, что соответствует
        повороту направо, налево, вниз, вверх и вращению
        """

        # сохраним текущее положение и конфигурацию
        x_prev, y_prev = self.x_position, self.y_position
        len_prev, width_prev = self.length, self.width
        direct_indx_prev = self.direct_indx

        self.move_dict[command]()
        new_body = body.Body(self.x_position, self.y_position, self.width, self.length)

        if any(point in self.hurdles_points for point in new_body.get_body_coord()):
            self.x_position, self.y_position = x_prev, y_prev
            self.width, self.length = width_prev, len_prev
            self.direct_indx = direct_indx_prev
            self.collision = True
        else:
            self._prev_body = self._body
            self._body = new_body
            self.collision = False

        if not self.collision:
            self._way.append(self.get_coodrd())

    def export_way(self):
        """
        Метод экспортирует пройденный путь в файл
        """
        with open('way.txt', 'w') as file:
            for point in self._way:
                file.write(str(point) + '\n')

    def get_direction_bounder(self):
        """
        Метод возвращает границу, определяющую направление и символ отрисовки
        """
        direction_dict = {
            'top': ['^', self._body._top_bounder],
            'left': ['<', self._body._left_bounder],
            'right': ['>', self._body._right_bounder],
            'bottom': ['v', self._body._bottom_bounder]
        }

        return direction_dict[self.directions[self.direct_indx]]

    def get_coodrd(self):
        """
        Метод возвращает текущее положение робота
        """
        return self.x_position, self.y_position

    def get_pad_coord(self):
        x, y = self.get_coodrd()
        indent = max(self.width, self.length)
        x = max(0, x - 5 * indent)
        y = max(0, y - 2 * indent)
        return x, y

    def get_initial_area(self):
        """
        Метод возвращает область, где будет помещен робот
        Для того чтобы изолировать робота от препятсивй,
        результат работы данного метода можно передать в конструктор карты
        """
        indent = max(self.width, self.length)
        return {
            'x_left': max(self.x_position - indent, 0),
            'x_right': self.x_position + self.width + indent,
            'y_top': self.y_position + self.length + indent,
            'y_bottom': max(self.y_position - indent, 0)
        }

    def add_robot_to_pad(self, pad):
        """
        Метод довавляет тело робота на объект curses pad (curses.newpad)
        """

        # зарисовали пробелами предыдущее положение
        if self._prev_body:
            self._prev_body.add_body_to_scr(pad, ' ')

        self._body.add_body_to_scr(pad, '@')

        direction_char, direction_bounder = self.get_direction_bounder()

        for point in direction_bounder:
            pad.addch(point[1], point[0], direction_char)

        if self.collision:
            for point in self._head_bounder:
                pad.addch(point[1], point[0], '*')
