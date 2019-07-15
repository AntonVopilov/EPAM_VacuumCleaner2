import sys
import curses

import map_constructor as mc
import robot as rob
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_F1, KEY_F2


def main_graphics(stdscr, map_width, map_length, hurdles_count):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    # параметры окна
    stdscr.clear()
    stdscr.keypad(1)
    curses.noecho()
    curses.curs_set(0)

    # длинна и ширина текущего окна
    scr_length, scr_width = stdscr.getmaxyx()

    # приветсвие
    msg_list = ['Vacuum Cleaner',
                'Press any key to continue',
                'to EXIT press key accept control keys',
                'control keys: up, down, left, right',
                'F1/F2 - rotation'
                ]
    for i, msg in enumerate(msg_list):
        stdscr.addstr(scr_length // 2 - len(msg_list) // 2 + i, scr_width // 2 - len(msg) // 2, msg)
    stdscr.getch()
    stdscr.clear()
    stdscr.refresh()

    # инициализация робота
    robot_width = 3
    robot_length = 4
    robot_object = rob.Robot(map_width // 2, map_length // 2, robot_width, robot_length)
    area = robot_object.get_initial_area()

    # инициализация карты
    map_pad = curses.newpad(map_length + 3, map_width + 3)
    hurdles_max_size = max(robot_length, robot_width)
    map_object = mc.MapConstructor(map_width, map_length, hurdles_max_size, hurdles_count, area)

    # доваление препятствий в память роботу
    robot_object.set_hudler_points(map_object.hurdles_points)

    # добавляем карту и робота на экран
    map_object.add_map_to_pad(map_pad)
    robot_object.add_robot_to_pad(map_pad)

    # определяем фрейм в котором будет отображаться карта
    view_box = [1, 1, scr_length - 1, scr_width // 2]

    # определяемя координаты карты, которые будут загруженны в фрейм
    # выводим на экран

    x, y = robot_object.get_pad_coord()
    map_pad.refresh(y, x, view_box[0], view_box[1], view_box[2], view_box[3])

    while True:
        event = stdscr.getch()
        if event not in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_F1, KEY_F2]:
            robot_object.export_way()
            break

        robot_object.make_move(event)
        robot_object.add_robot_to_pad(map_pad)
        if not robot_object.collision:
            x, y = robot_object.get_pad_coord()
        x_pos, y_pos = robot_object.get_coodrd()

        stdscr.addstr(0, 0, f'robot location {x_pos} {y_pos}, robot collision status {robot_object.collision} ',
                      curses.color_pair(1))
        map_pad.refresh(y, x, view_box[0], view_box[1], view_box[2], view_box[3])


if __name__ == '__main__':
    map_width = int(sys.argv[1])
    map_length = int(sys.argv[2])
    hurdles_count = int(sys.argv[3])
    curses.wrapper(main_graphics, map_width, map_length, hurdles_count)
