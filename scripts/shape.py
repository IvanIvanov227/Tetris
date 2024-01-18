import pygame
import random

from constants import TYPES_OF_SHAPES, START_SHAPES, START_COORDINATES, COLORS


def draw_shapes(x, y, surface, coords, colors, size_block):
    for i in range(len(coords)):
        line = coords[i]
        for j, cube in enumerate(line):
            if cube != 0:
                draw_cube(x + j * size_block, y + i * size_block, surface, colors, size_block)


def draw_cube(x, y, surface, colors, size_block):
    color1 = colors[0]
    color2 = colors[1]
    color3 = colors[2]
    color4 = colors[3]

    points1 = [
        (x, y), (x + size_block // 4, y + size_block // 4), (x + size_block * 3 // 4, y + size_block // 4),
        (x + size_block, y)
    ]
    points2 = [
        (x + size_block, y), (x + size_block, y + size_block),
        (x + size_block * 3 // 4, y + size_block * 3 // 4),
        (x + size_block * 3 // 4, y + size_block // 4)
    ]
    points3 = [
        (x, y + size_block), (x + size_block // 4, y + size_block * 3 / 4),
        (x + size_block * 3 // 4, y + size_block * 3 // 4), (x + size_block, y + size_block)
    ]
    points4 = [
        (x, y), (x + size_block // 4, y + size_block // 4), (x + size_block // 4, y + size_block * 3 // 4),
        (x, y + size_block)
    ]
    pygame.draw.polygon(surface, color1, points1)
    pygame.draw.polygon(surface, color3, points2)
    pygame.draw.polygon(surface, color4, points3)
    pygame.draw.polygon(surface, color3, points4)

    pygame.draw.rect(surface, color2,
                     pygame.Rect(x + size_block // 4, y + size_block // 4, size_block // 2 + 1, size_block / 2 + 1))


class Shape(pygame.sprite.Sprite):
    def __init__(self, level, group, size_screen, size_block, parent=None):
        super().__init__(group)
        self.size_screen = size_screen
        self.size_block = size_block
        self.top = (size_screen[1] - 21 * size_block) // 2
        self.left = size_screen[0] // 2 - size_block * 5
        color_random = random.choice(COLORS)
        self.color1 = pygame.Color(*color_random)
        self.color2 = pygame.Color(*color_random)
        self.color3 = pygame.Color(*color_random)
        self.color4 = pygame.Color(*color_random)
        self.form = random.randint(1, 7)
        self.rotate = 0
        self.color = random.choice(COLORS)
        self.set_color()
        width_image = len(TYPES_OF_SHAPES[self.form][self.rotate][0]) * size_block
        height_image = len(TYPES_OF_SHAPES[self.form][self.rotate]) * size_block
        self.image = pygame.Surface((width_image, height_image), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.coords = []
        self.cube_coords = []
        # После вставки в поле
        self.coordinates = None
        self.v = (0.8 - (level * 0.007)) ** level
        self.update_move = True
        self.parent = parent

    def update_size(self, size_block):
        width_image = len(TYPES_OF_SHAPES[self.form][self.rotate][0]) * size_block
        height_image = len(TYPES_OF_SHAPES[self.form][self.rotate]) * size_block
        self.image = pygame.Surface((width_image, height_image), pygame.SRCALPHA)

    def update_coords_now_shape(self, left, top, size_block, screen_size):
        width_image = len(TYPES_OF_SHAPES[self.form][self.rotate][0]) * size_block
        height_image = len(TYPES_OF_SHAPES[self.form][self.rotate]) * size_block
        count_x = (self.rect.x - self.left) // self.size_block
        count_y = (self.rect.y - self.top) // self.size_block
        self.top = top
        self.left = left
        self.size_block = size_block
        self.size_screen = screen_size
        self.rect = pygame.Rect(count_x * size_block + self.left, count_y * size_block + self.top, width_image,
                                height_image)

        draw_shapes(0, 0, self.image, TYPES_OF_SHAPES[self.form][self.rotate],
                    [self.color1, self.color2, self.color3, self.color4], self.size_block)

    def update_coords_future_shape(self, left, top, size_block, screen_size):
        self.left = left
        self.top = top
        count_width = len(START_SHAPES[self.form][0])
        count_height = len(START_SHAPES[self.form])
        width_image = len(TYPES_OF_SHAPES[self.form][self.rotate][0]) * size_block
        height_image = len(TYPES_OF_SHAPES[self.form][self.rotate]) * size_block

        height_text = pygame.font.Font(None, int(screen_size[0] // 100 * 2.5)).get_height()
        self.size_block = size_block
        self.size_screen = screen_size
        x = self.left + 12 * size_block
        y = self.top * 2 + height_text + 5
        x_center = x + size_block * 3
        y_center = y + size_block * 3
        self.rect.x = x_center - size_block * count_width // 2
        self.rect.y = y_center - size_block * count_height // 2
        self.rect.w = width_image
        self.rect.h = height_image
        self.draw_start(0, 0, self.image)

    def set_color(self):
        hsv1 = self.color1.hsva
        hsv2 = self.color2.hsva
        hsv3 = self.color3.hsva
        hsv4 = self.color4.hsva
        self.color1.hsva = (hsv1[0], hsv1[1], 100, hsv1[3])
        self.color2.hsva = (hsv2[0], hsv2[1], 75, hsv1[3])
        self.color3.hsva = (hsv3[0], hsv3[1], 60, hsv1[3])
        self.color4.hsva = (hsv4[0], hsv3[1], 50, hsv1[3])

    def set_coord_board(self):
        self.coords = []
        start_x = START_COORDINATES[self.form][0]
        for i in range(len(START_SHAPES[self.form])):
            self.coords.append([])
            for j in range(len(START_SHAPES[self.form][0])):
                if START_SHAPES[self.form][i][j] != 0:
                    self.coords[-1].append([start_x + j, i])
                self.parent.board.board[i][start_x + j] += START_SHAPES[self.form][i][j]

    def set_coord_cube_board(self):
        self.cube_coords = []
        start_x = START_COORDINATES[self.form][0]
        for i in range(len(TYPES_OF_SHAPES[self.form][self.rotate])):
            self.cube_coords.append([])
            for j in range(len(TYPES_OF_SHAPES[self.form][self.rotate][0])):
                self.cube_coords[-1].append([start_x + j, i])

    def draw_start(self, x, y, surface):
        i = 0
        count_y = 0
        n = len(TYPES_OF_SHAPES[self.form][self.rotate])
        while i < n:
            line = TYPES_OF_SHAPES[self.form][self.rotate][i]
            if sum(line) != 0:
                for j, cube in enumerate(line):
                    if cube != 0:
                        draw_cube(x + j * self.size_block, y + count_y * self.size_block, surface,
                                  [self.color1, self.color2, self.color3, self.color4], self.size_block)
                count_y += 1
            i += 1

    def move(self, action):
        if action == 'left':
            self.left_shape()

        elif action == 'right':
            self.right_shape()

        elif action == 'down':
            self.down_shape()

        elif action == 'rotate':
            self.rotate_shape()

    def right_shape(self):
        result = self.check_move_right()
        if result is True:
            for index, coord_line in enumerate(self.coords):
                for index2, coord in enumerate(coord_line[::-1]):
                    index2 = len(coord_line) - index2 - 1
                    self.parent.board.board[coord[1]][coord[0]] = 0
                    self.coords[index][index2] = [coord[0] + 1, coord[1]]
                    self.parent.board.board[coord[1]][coord[0] + 1] = 1

            for index, coord_line in enumerate(self.cube_coords):
                for index2, coord in enumerate(coord_line):
                    self.cube_coords[index][index2][0] += 1

            self.rect.x += self.size_block

    def left_shape(self):
        result = self.check_move_left()
        if result is True:
            for index, coord_line in enumerate(self.coords):
                for index2, coord in enumerate(coord_line):
                    self.parent.board.board[coord[1]][coord[0]] = 0
                    self.coords[index][index2] = [coord[0] - 1, coord[1]]
                    self.parent.board.board[coord[1]][coord[0] - 1] = 1

            for index, coord_line in enumerate(self.cube_coords):
                for index2, coord in enumerate(coord_line):
                    self.cube_coords[index][index2][0] -= 1

            self.rect.x -= self.size_block

    def down_shape(self):
        result = self.check_move_down()
        if result is True:

            for index, coord_line in enumerate(self.coords[::-1]):
                index = len(self.coords) - index - 1
                for index2, coord in enumerate(coord_line):
                    self.parent.board.board[coord[1]][coord[0]] = 0
                    self.coords[index][index2] = [coord[0], coord[1] + 1]
                    self.parent.board.board[coord[1] + 1][coord[0]] = 1

            for index, coord_line in enumerate(self.cube_coords):
                for index2, coord in enumerate(coord_line):
                    self.cube_coords[index][index2][1] += 1

            self.rect.y += self.size_block
        else:
            self.update_move = False

    def check_move_left(self):

        for coord_line in self.coords:
            coord = coord_line[0]
            if coord[0] == 0 or self.parent.board.board[coord[1]][coord[0] - 1]:
                return False
        return True

    def check_move_right(self):
        for coord_line in self.coords:
            coord = coord_line[-1]
            if coord[0] == 9 or self.parent.board.board[coord[1]][coord[0] + 1]:
                return False
        return True

    def check_move_down(self):
        for coord_line in self.coords:
            for coord in coord_line:
                if coord[1] == 19 or (self.parent.board.board[coord[1] + 1][coord[0]] and
                                      [coord[0], coord[1] + 1] not in [j for i in self.coords for j in i]):
                    return False
        return True

    def rotate_shape(self):
        self.rotate = (self.rotate + 1) % 4
        # Новые координаты
        new_coords = []
        for index, coord_line in enumerate(TYPES_OF_SHAPES[self.form][self.rotate]):
            if sum(coord_line) != 0:
                new_coords.append([])
                for index2, coord in enumerate(coord_line):
                    coord = coord_line[index2]
                    if coord == 1:
                        new_coords[-1].append(self.cube_coords[index][index2])
        # Проверка на корректность новых координат
        for index, coord_line in enumerate(new_coords):
            for index2, coord in enumerate(coord_line):
                if coord[1] > 19 or coord[1] < 0 or coord[0] < 0 or coord[0] > 9:
                    self.rotate = (self.rotate - 1) % 4
                    return
                elif (coord not in [j for i in self.coords for j in i]
                      and self.parent.board.board[coord[1]][coord[0]] == 1):
                    self.rotate = (self.rotate - 1) % 4
                    return
        # Установление новой фигуры на поле за место старой
        for index, coord_line in enumerate(self.coords):
            for index2, coord in enumerate(coord_line):
                self.parent.board.board[coord[1]][coord[0]] = 0

        for index, coord_line in enumerate(new_coords):
            for index2, coord in enumerate(coord_line):
                self.parent.board.board[coord[1]][coord[0]] = 1

        self.coords = new_coords
        width_image = len(TYPES_OF_SHAPES[self.form][self.rotate][0]) * self.size_block
        height_image = len(TYPES_OF_SHAPES[self.form][self.rotate]) * self.size_block
        self.image = pygame.Surface((width_image, height_image), pygame.SRCALPHA)
        draw_shapes(0, 0, self.image, TYPES_OF_SHAPES[self.form][self.rotate],
                    [self.color1, self.color2, self.color3, self.color4], self.size_block)
