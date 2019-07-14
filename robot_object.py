import time
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
import body


class Robot:
    def __init__(self, x, y, width, length, hudlers_points):

        self.x_position = x
        self.y_position = y
        self.collision = False

        self.hurdles_points = hudlers_points

        self.width = width
        self.length = length

        self._body = body.Body(self.x_position, self.y_position, width, length)
        self._prev_body = None
        self._head_bounder = None

        self.move_dict = {
            KEY_UP: self.up,
            KEY_DOWN: self.down,
            KEY_LEFT: self.left,
            KEY_RIGHT: self.right
        }

    def check_hurdles(self, x, y):
        body_buffer = body.Body(x, y, self.width, self.length)

        if any(body_point in self.hurdles_points for body_point in body_buffer.get_body_coord()):
            self._prev_body = self._body
            return True
        else:
            self._prev_body = self._body
            self._body = body_buffer
            return False

    def right(self):

        self.collision = self.check_hurdles(self.x_position + 1, self.y_position)
        self._head_bounder = self._body._right_bounder
        self._head_bounder += [self._body._top_bounder[-1], self._body._bottom_bounder[-1]]
        if not self.collision:
            self.x_position += 1

    def left(self):

        self.collision = self.check_hurdles(self.x_position - 1, self.y_position)
        self._head_bounder = self._body._left_bounder
        self._head_bounder += [self._body._top_bounder[0], self._body._bottom_bounder[0]]
        if not self.collision:
            self.x_position -= 1

    def up(self):

        self.collision = self.check_hurdles(self.x_position, self.y_position - 1)
        self._head_bounder = self._body._top_bounder
        if not self.collision:
            self.y_position -= 1

    def down(self):

        self.collision = self.check_hurdles(self.x_position, self.y_position + 1)
        self._head_bounder = self._body._bottom_bounder
        if not self.collision:
            self.y_position += 1

    def make_move(self, command):
        self.move_dict[command]()

    def get_coodrd(self):
        return self.x_position, self.y_position
    def get_center_coord(self):
        return self.x_position + self.width//2, self.y_position + self.length//2

    def add_robot_to_pad(self, pad):

        if self._prev_body:
            self._prev_body.add_body_to_scr(pad, ' ')

        self._body.add_body_to_scr(pad, '@')
        if self.collision:
            for point in self._head_bounder:
                pad.addch(point[1], point[0], '^')
