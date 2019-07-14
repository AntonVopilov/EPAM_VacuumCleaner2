import body
from random import randint
import curses
import time


def hurdle_fabric(max_x, max_y, max_size, num_hurdles):
    hurdles = []
    for i in range(num_hurdles):
        x_pos = randint(1, max_x - max_size * 2)
        y_pos = randint(1, max_y - max_size * 2)
        width = randint(2, max_size)
        length = randint(2, max_size)
        hurdles.append(body.Body(x_pos, y_pos, width, length))
    hurdles.append(body.Body(0, 0, max_x - 1, max_y - 1))
    return hurdles


class MapConstructor:
    def __init__(self, map_width, map_length, hurdles_max_size, hurdles_count):

        self.map_width = map_width
        self.map_length = map_length
        self.hudlers_max_size = hurdles_max_size
        self.hudlers_count = hurdles_count

        self.hurdles = hurdle_fabric(map_width, map_length, hurdles_max_size, hurdles_count)
        self._hurdle_char = '#'

    def add_map_to_pad(self, pad):

        for item in self.hurdles:
            item.add_body_to_scr(pad, self._hurdle_char)

    def get_hurdlers_points(self):
        res = []
        for item in self.hurdles:
            res += item.get_body_coord()
        return res

    def clear_area(self, area, pad):
        for point in self.get_hurdlers_points():
            if area['x_left'] < point[0] < area['x_right'] and area['y_bottom'] < point[1] < area['y_top']:
                pad.addch(point[1], point[0], ' ')


def test_map_constructor(stdscr):
    stdscr.clear()
    map_width, map_length = 40, 11
    map_pad = curses.newpad(map_length, map_width)
    hurdles_max_size = 3
    hurdles_count = 100
    map_object = MapConstructor(map_width, map_length, hurdles_max_size, hurdles_count)

    map_object.add_map_to_pad(map_pad)
    map_pad.refresh(0, 0, 1, 1, 11, 40)
    time.sleep(3)

    area = {
        'x_left': map_width//2 - 3,
        'x_right': map_width // 2 + 3,
        'y_top': map_length//2 + 3,
        'y_bottom': map_length//2 - 3

    }

    map_object.clear_area(area, map_pad)
    map_pad.refresh(0, 0, 1, 1, 11, 40)
    time.sleep(3)


if __name__ == '__main__':
    curses.wrapper(test_map_constructor)
