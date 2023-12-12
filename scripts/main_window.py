import os
import sys

import pygame
import random


def load_image(name, colorkey=None, size=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is not None:

        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, (size[0], size[1]))
    return image


class Tetris:
    """Главный класс игры"""
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.list_snow = []
        self.fps = 60
        self.time_draw_snow = 0
        self.color_screen = (8, 24, 36)

    def start_game(self):
        """Начало игры"""
        running = True
        clock = pygame.time.Clock()
        screen_image = load_image('screen.png', size=(self.size[0], self.size[1]))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.blit(screen_image, (0, 0))
            # Рисование снежинок
            self.draw_snow()
            # Отображение игрового поля
            self.draw_field()
            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()

    def draw_snow(self):
        """Рисование снежинок"""
        self.time_draw_snow += 0.01
        if self.time_draw_snow >= 1:
            self.time_draw_snow = 0
            self.list_snow.append([random.random() * self.size[0], self.size[1],
                                   random.randint(15, 30), random.randint(2, 4)])
        for index, snow in enumerate(self.list_snow):
            self.list_snow[index][1] -= snow[2] / self.fps
            snow = self.list_snow[index]
            pygame.draw.rect(self.screen, 'white', (snow[0], snow[1], snow[3], snow[3]))
            if snow[1] <= 0:
                del self.list_snow[index]

    def draw_field(self):
        """Рисование поля"""
        image = load_image('cube.png', -1)
        size = image.get_width()
        while 24 * size > self.size[1]:
            size -= 1
        # Рисование боковых стенок поля
        y = (self.size[1] - 21 * size) // 2
        x1 = self.size[0] // 2 - size * 6
        x = x1
        image = load_image('cube.png', -1, (size, size))
        for i in range(20):
            self.screen.blit(image, (x1, y))
            y += size
        x2 = x1 + size * 11
        y = (self.size[1] - 21 * size) // 2
        for i in range(20):
            self.screen.blit(image, (x2, y))
            y += size
        for i in range(12):
            self.screen.blit(image, (x1, y))
            x1 += size
        y = (self.size[1] - 21 * size) // 2 + size
        pygame.draw.rect(self.screen, 'black',
                         (x + size, y, 10 * size, 19 * size))
        # Рисование
        board = Board(size, x, (self.size[1] - 21 * size) // 2 + size)
        board.render(self.screen)


class Board:
    # создание поля
    def __init__(self, cell_size, left, top):
        self.screen = None
        self.width = 12
        self.height = 20
        self.screen = None
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.screen = screen
        x, y = 0, 0
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'orange', (self.left + x, self.top + y, self.cell_size, self.cell_size), 1)

                x += self.cell_size
            y += self.cell_size
            x = 0

    def get_cell(self, mouse_pos):
        """Возвращает координаты клетки в виде кортежа"""
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (self.left + self.width * self.cell_size >= x >= self.left
                and self.top + self.height * self.cell_size >= y >= self.top):
            n_x = (x - self.left) // self.cell_size
            n_y = (y - self.top) // self.cell_size
            return n_x, n_y
        else:
            return None

    def get_click(self, mouse_pos):
        """Изменяет поле, опираясь на полученные координаты клетки"""
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        """Получает событие нажатия и вызывает первые два метода"""
        if cell_coords is not None:
            x, y = cell_coords
            place = self.board[y][x]
            flag = False
            color = None
            if self.count % 2 == 0 and place == 'red':
                color = 'red'
                flag = True
            elif self.count % 2 != 0 and place == 'blue':
                color = 'blue'
                flag = True

            if flag:
                self.draw_cells(color, x, y)
                self.count += 1