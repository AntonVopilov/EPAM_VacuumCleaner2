import body
from random import randint


def hurdle_fabric(max_x, max_y, max_size, num_hurdles):
    """
    Функция генерирует препятсвия случайного размера и в случайном положении
    max_x - крайннее допустимое значение по оси х
    max_y - крайннее допустимое значение по оси y
    max_size - максимальный размер препятсивия
    num_hurdles - количество препятсвий

    """
    hurdles = []
    for i in range(num_hurdles):
        x_pos = randint(1, max_x - max_size * 2)
        y_pos = randint(1, max_y - max_size * 2)
        width = randint(2, max_size)
        length = randint(2, max_size)
        hurdles.append(body.Body(x_pos, y_pos, width, length))

    return hurdles


class MapConstructor:
    """
    Возвращает карту заданного размера с заданным количеством препятсвий
    map_width - ширина карты,
    map_length - длинна карты,
    hurdles_max_size - максимальный размер препятсивий,
    hurdles_count - количество препятсвий,
    area - область, в которой появится робот. Эта область должна быть свободной от препятсивий.
    area = {
            'x_left': x_left,
            'x_right': x_right,
            'y_top': y_top,
            'y_bottom': y_bottom
        }
    """

    def __init__(self, map_width, map_length, hurdles_max_size, hurdles_count, area):

        self.map_width = map_width
        self.map_length = map_length
        self.hurdlers_max_size = hurdles_max_size
        self.hurdlers_count = hurdles_count

        self.hurdles = hurdle_fabric(map_width, map_length, hurdles_max_size, hurdles_count)
        self.hurdles_points = []
        self._hurdle_char = '#'

        self.get_hurdlers_points(area)

    def add_map_to_pad(self, pad):
        """
        Метод добавляет препятсвия на curses объект pad (curses.newpad(...))

        """

        for point in self.hurdles_points:
            pad.addch(point[1], point[0], self._hurdle_char)

    def get_hurdlers_points(self, area):
        """
        Метод возвращает препятсвия, которые находятся вне зоны area
        """
        res = []
        for item in self.hurdles:
            for point in item.get_body_coord():
                if not (area['x_left'] < point[0] < area['x_right'] and area['y_bottom'] < point[1] < area['y_top']):
                    res.append(point)
        res += body.Body(0, 0, self.map_width, self.map_length).get_body_coord()
        self.hurdles_points = res

        return res
