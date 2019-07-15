class Body:
    """
    Класс Body возвращает прямоугольный объект для отображения на карте
    x_left_top, y_left_top - положение левого верхнего угла
    width - ширина прямоугольника (ассоциируется с x направлением)
    length - длина прямоугольника (ассоциируется с y направлением)

    """

    def __init__(self, x: int, y: int, width: int, length: int):
        if any(not isinstance(arg, int) for arg in [x, y, width, length]):
            raise TypeError(f'Expected int arguments')

        self.x_left_top = x
        self.y_left_top = y
        self.width = width
        self.length = length
        # Атрибуты отвечающие верхней, нижней, правой и левой границе прямоугольника соответственно
        self._top_bounder = []
        self._bottom_bounder = []
        self._right_bounder = []
        self._left_bounder = []
        # Все граничные точки
        self._body_points = []
        # Инициализируем координаты границы
        self.calculate_body_coord()

    def set_to_empty(self):
        self._body_points = []
        self._top_bounder = []
        self._bottom_bounder = []
        self._right_bounder = []
        self._left_bounder = []

    def calculate_body_coord(self):
        """
        Метод рассчитывает координаты границ
        """
        # удалим предыдущие координаты объекта
        self.set_to_empty()

        for i in range(self.width):
            self._top_bounder.append([self.x_left_top + i, self.y_left_top])
            self._bottom_bounder.append([self.x_left_top + i, self.y_left_top + self.length - 1])
        for i in range(1, self.length):
            self._right_bounder.append([self.x_left_top + self.width - 1, self.y_left_top + i])
            self._left_bounder.append([self.x_left_top, self.y_left_top + i])

    def get_body_coord(self):
        """
        Метод возвращает координаты границ в одном списке [[1, 2], [3, 4] ...]
        """
        self.calculate_body_coord()
        self._body_points += self._top_bounder + self._bottom_bounder
        self._body_points += self._left_bounder + self._right_bounder
        return self._body_points

    def get_body_center(self):
        """
        Метод возвращает положение центра прямоугольника (x_center: int, y_center: int)
        """
        return self.x_left_top + self.width // 2, self.y_left_top + self.length // 2

    def set_body_center(self, xc, yc):
        self.x_left_top = xc - self.width // 2
        self.y_left_top = yc - self.length // 2

    def add_body_to_scr(self, stdscr, char):
        """
        Метод рисует прямоугольник в объекте stdscr символами char
        Обновление stdscr не выполняется, чтобы обновить вызови stdscr.refresh(*args)
        """

        for point in self.get_body_coord():
            stdscr.addch(point[1], point[0], char)
