from random import randint
import curses
import time


class Body:
    def __init__(self, x: int, y: int, width: int, length: int):
        self.x_left_top = x
        self.y_left_top = y
        self.width = width  # associated with x direction
        self.length = length  # associated with y direction
        self._body_points = []
        self._top_bounder = []
        self._bottom_bounder = []
        self._right_bounder = []
        self._left_bounder = []


    def calculate_body_coord(self):
        self.set_to_empty()
        for i in range(self.width):
            self._top_bounder.append([self.x_left_top + i, self.y_left_top])
            self._bottom_bounder.append([self.x_left_top + i, self.y_left_top + self.length - 1])
        for i in range(1, self.length):
            self._right_bounder.append([self.x_left_top + self.width - 1, self.y_left_top + i])
            self._left_bounder.append([self.x_left_top, self.y_left_top + i])

    def get_body_coord(self):
        self.calculate_body_coord()
        self._body_points += self._top_bounder + self._bottom_bounder
        self._body_points += self._left_bounder + self._right_bounder
        return self._body_points

    def get_body_center(self):
        return self.x_left_top + self.width // 2, self.y_left_top + self.length // 2

    def set_body_center(self, xc, yc):
        self.x_left_top = xc - self.width // 2
        self.y_left_top = yc - self.length // 2

    def set_to_empty(self):
        self._body_points = []
        self._top_bounder = []
        self._bottom_bounder = []
        self._right_bounder = []
        self._left_bounder = []

    def add_body_to_scr(self, stdscr, char):

        for point in self.get_body_coord():
            stdscr.addch(point[1], point[0], char)

    def render(self, stdscr, char):
        self.get_body_coord()
        for point in self._body_points:
            stdscr.addch(point[1], point[0], char)
        # stdscr.refresh()


def print_bodies(stdscr):
    hurdles = []
    num_hurdles = 1000
    max_size = 2
    max_x = 200
    max_y = 100

    stdscr.clear()
    stdscr.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    scrh, scrw = stdscr.getmaxyx()

    for i in range(num_hurdles):
        width = randint(2, max_size)
        length = randint(2, max_size)
        x_pos = randint(max_size, max_x - max_size * 2)
        y_pos = randint(max_size, max_y - max_size * 2)

        hurdles.append(Body(x_pos, y_pos, width, length))
    hurdles.append(Body(0, 0, max_x - 1, max_y - 1))

    pad = curses.newpad(max_y, max_x)

    for item in hurdles:
        print(item.get_body_coord())
        item.render(pad, '@')

    pad.refresh(0, 0, 0, 0, scrh - 1, scrw - 1)

    time.sleep(3)


if __name__ == '__main__':
    curses.wrapper(print_bodies)
