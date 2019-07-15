import curses
import body
import map_constructor2 as mc
import robot_object as rob
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_F1
import time




def move_pad(x, y, pad, event, view_box):
    if event == KEY_DOWN:
        y += 1
    if event == KEY_UP:
        y -= 1
    if event == KEY_LEFT:
        x -= 1
    if event == KEY_RIGHT:
        x += 1

    return x, y


def main_graphics(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.keypad(1)
    curses.noecho()
    curses.curs_set(0)

    scr_length, scr_width = stdscr.getmaxyx()

    map_width = 60
    map_length = 80
    map_pad = curses.newpad(map_length, map_width)

    hurdles_max_size = 3
    hurdles_count = 30
    map_object = mc.MapConstructor(map_width, map_length, hurdles_max_size, hurdles_count)

    map_object.add_map_to_pad(map_pad)

    robot_width = 3
    robot_length = 5
    robot_object = rob.Robot(map_width // 2, map_length // 2, robot_width, robot_length,
                             map_object.get_hurdlers_points())

    area = {
        'x_left': robot_object.x_position - 2,
        'x_right': robot_object.x_position + robot_object.width + 1,
        'y_top': robot_object.y_position + robot_object.length + 1,
        'y_bottom': robot_object.y_position - 1

    }

    view_box = [1, 1, scr_length - 1, scr_width // 2]


    x = max(map_width // 2 - 6 * robot_object.width, 0)
    y = max(map_length // 2 - robot_object.length, 0)

    map_pad.refresh(y, x, view_box[0], view_box[1], view_box[2], view_box[3])

    map_object.clear_area(area, map_pad)
    map_pad.refresh(y, x, view_box[0], view_box[1], view_box[2], view_box[3])

    robot_object.add_robot_to_pad(map_pad)
    map_pad.refresh(y, x, view_box[0], view_box[1], view_box[2], view_box[3])

    while True:

        event = stdscr.getch()
        x_pos, y_pos = robot_object.get_coodrd()
        stdscr.addstr(0, 0, f'robot location {x_pos} {y_pos}, pad location {x} {y}', curses.color_pair(1))
        if event not in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_F1]:
            break
        robot_object.move_dict[event]()
        robot_object.add_robot_to_pad(map_pad)
        if not robot_object.collision:
            x, y = move_pad(x, y, map_pad, event, view_box)
        map_pad.refresh(y, x, view_box[0], view_box[1], view_box[2], view_box[3])


if __name__ == '__main__':
    curses.wrapper(main_graphics)
