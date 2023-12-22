import os
import sys

import pygame
import random


def load_image(name, colorkey=None, size=None):
    full_name = os.path.join('../data', name)
    if not os.path.isfile(full_name):
        print(f"Файл с изображением '{full_name}' не найден")
        sys.exit()

    image = pygame.image.load(full_name)
    if colorkey is not None:

        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, (size[0], size[1]))
    return image


def load_data():
    global size_block, start_image_1, start_image_2, image_block, start_button
    # картинка куба
    image = load_image('cube.png')
    size_block = image.get_width()
    while 24 * size_block > SIZE_SCREEN[1]:
        size_block -= 1
    image_block = load_image('cube.png', -1, (size_block, size_block))
    # Кнопка старта
    start_image_1 = load_image('start.png', colorkey=-1, size=(4 * size_block, size_block * 2))
    start_image_2 = load_image('start2.png', colorkey=-1, size=(4 * size_block, size_block * 2))
    start_button = Button(SIZE_SCREEN[0] // 2 - 4 * size_block // 2,
                          SIZE_SCREEN[1] // 4 - size_block * 2 // 2, start_image_2)
    Button(SIZE_SCREEN[0] // 2 - size_block * 2.7, SIZE_SCREEN[1] // 2 + size_block * 2,
           load_image('up.png', size=(size_block * 2, size_block * 2)))
    Button(SIZE_SCREEN[0] // 2 - size_block * 4, SIZE_SCREEN[1] // 2 + size_block * 4,
           load_image('left.png', size=(size_block * 2, size_block * 2)))
    Button(SIZE_SCREEN[0] // 2 - size_block * 2, SIZE_SCREEN[1] // 2 + size_block * 4,
           load_image('right.png', size=(size_block * 2, size_block * 2)))
    Button(SIZE_SCREEN[0] // 2 - size_block * 2.7, SIZE_SCREEN[1] // 2 + size_block * 6,
           load_image('down.png', size=(size_block * 2, size_block * 2)))


class Tetris:
    """Главный класс игры"""

    def __init__(self):
        y = SIZE_SCREEN[1] // 2 - 3 * size_block
        self.coords_letters = self.coords_letters = [
            [SIZE_SCREEN[0] // 2 - 3 * size_block, y, 0, -1], [SIZE_SCREEN[0] // 2 - 2 * size_block, y, 0, 1],
            [SIZE_SCREEN[0] // 2 - size_block, y, 0, -1], [SIZE_SCREEN[0] // 2, y, 0, 1],
            [SIZE_SCREEN[0] // 2 + size_block, y, 0, -1], [SIZE_SCREEN[0] // 2 + 2 * size_block, y, 0, 1]
        ]
        self.start_image = None
        self.time_draw_particle = 0
        self.start_flag = True
        self.start_button = start_button
        self.image_block = image_block

    def start_game(self):
        """Начало игры"""
        running = True
        clock = pygame.time.Clock()
        screen_image = load_image('screen.png', size=(SIZE_SCREEN[0], SIZE_SCREEN[1]))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        start_button.down_click = event.pos
                        start_button.up_click = None
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        start_button.up_click = event.pos
            screen.blit(screen_image, (0, 0))
            particle_sprites.draw(screen)
            self.draw_design()
            if self.start_flag:
                buttons_sprites.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()

    def draw_design(self):
        """Рисование самого дизайна игры"""
        self.draw_particle()
        self.draw_field()
        if self.start_flag:
            self.draw_start_screen()

    def draw_particle(self):
        """Рисование снежинок"""
        self.time_draw_particle += 0.01

        if self.time_draw_particle >= 1:
            self.time_draw_particle = 0
            Particle(random.random() * SIZE_SCREEN[0], SIZE_SCREEN[1],
                     random.randint(15, 30), random.randint(2, 4))

        for particle in particle_sprites:
            if type(particle) == Particle:
                particle.update()
                if particle.rect.y <= 0:
                    particle_sprites.remove(particle)

    def draw_field(self, draw_cells=False):
        """Рисование поля"""
        # Рисование боковых стенок поля
        y = (SIZE_SCREEN[1] - 21 * size_block) // 2
        x1 = SIZE_SCREEN[0] // 2 - size_block * 6
        x = x1
        for i in range(20):
            screen.blit(self.image_block, (x1, y))
            y += size_block
        x2 = x1 + size_block * 11
        y = (SIZE_SCREEN[1] - 21 * size_block) // 2
        for i in range(20):
            screen.blit(self.image_block, (x2, y))
            y += size_block
        for i in range(12):
            screen.blit(self.image_block, (x1, y))
            x1 += size_block
        y = (SIZE_SCREEN[1] - 21 * size_block) // 2 + size_block
        pygame.draw.rect(screen, (11, 2, 20),
                         (x + size_block, y, 10 * size_block, 19 * size_block))

    def draw_start_screen(self):
        """Рисование стартового окна"""
        self.draw_start_button()
        self.draw_letters()
        self.draw_instruction()

    def draw_start_button(self):
        x = self.start_button.rect.x
        y = self.start_button.rect.y
        w = self.start_button.rect.w
        h = self.start_button.rect.h
        if (self.start_button.up_click is None and self.start_button.down_click
                and x <= self.start_button.down_click[0] <= x + w
                and y <= self.start_button.down_click[1] <= h + y):
            image = start_image_1
        elif self.start_button.up_click is not None and self.start_button.down_click is not None and (
                x <= self.start_button.down_click[0] <= x + w and
                y <= self.start_button.down_click[1] <= h + y and x <=
                self.start_button.up_click[0] <= x + w and
                y <= self.start_button.up_click[1] <= y + w):
            # Начать игру
            self.start_flag = False
            image = start_image_1
        else:
            self.start_button.up_click = None
            self.start_button.down_click = None
            image = start_image_2

        self.start_button.image = image

    def draw_letters(self):

        letters = ['T', 'E', 'T', 'R', 'I', 'S']
        for index, val in enumerate(letters):
            screen.blit(load_image(f'tetris/{val}.png', -1, size=(size_block, size_block)),
                        (self.coords_letters[index][0], self.coords_letters[index][1] + self.coords_letters[index][2]))
            elem = self.coords_letters[index][2]
            if self.coords_letters[index][3] == 1:
                elem += 1
            else:
                elem -= 1
            if abs(elem) == 10:
                self.coords_letters[index][3] *= -1
            self.coords_letters[index][2] = elem

    def draw_instruction(self):
        # Доделай нормальную инструкцию
        ...


class Board:
    # создание поля
    def __init__(self, width_count, height_count, left, top):
        self.screen = None
        self.width = width_count
        self.height = height_count
        # self.board = [[choice(['red', 'blue']) for _ in range(width_count)] for _ in range(height_count)]
        self.count = 0
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.screen = screen
        x, y = 0, 0
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (self.left + x, self.top + y, self.cell_size, self.cell_size), 1)
                pygame.draw.circle(screen, self.board[i][j],
                                   (self.left + j * self.cell_size + self.cell_size / 2,
                                    self.top + i * self.cell_size + self.cell_size / 2), self.cell_size / 2 - 2)
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

    def draw_cells(self, color, x_cell, y_cell):
        for i in range(self.width):
            x = self.left + i * self.cell_size
            y = self.top + y_cell * self.cell_size

            pygame.draw.circle(self.screen, color, (x + self.cell_size / 2, y + self.cell_size / 2),
                               self.cell_size / 2 - 2)
            if color == 'red' and self.board[y_cell][i] == 'blue':
                self.board[y_cell][i] = 'red'
            elif color == 'blue' and self.board[y_cell][i] == 'red':
                self.board[y_cell][i] = 'blue'
        for i in range(self.height):
            if i != y_cell:
                x = self.left + x_cell * self.cell_size
                y = self.top + i * self.cell_size
                pygame.draw.circle(self.screen, color, (x + self.cell_size / 2, y + self.cell_size / 2),
                                   self.cell_size / 2 - 2)
                if color == 'red' and self.board[i][x_cell] == 'blue':
                    self.board[i][x_cell] = 'red'
                elif color == 'blue' and self.board[i][x_cell] == 'red':
                    self.board[i][x_cell] = 'blue'


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, dy, size):
        super().__init__(particle_sprites)
        self.image = pygame.Surface((size, size))
        self.image.fill('white')
        self.rect = pygame.Rect(x, y, size, size)
        # у каждой частицы своя скорость — это вектор
        self.velocity = [0, dy]
        self.size = size
        self.y = y

    def update(self):
        self.y -= self.velocity[1] / FPS
        self.rect.y = self.y


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(buttons_sprites)
        self.image = image
        self.up_click = None
        self.down_click = None
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Тетрис')
    fullname = os.path.join('../data', 'icon.png')
    image_icon = pygame.image.load(fullname)
    pygame.display.set_icon(image_icon)
    screensize = pygame.display.list_modes()
    SIZE_SCREEN = width, height = screensize[1][0], screensize[1][1]
    screen = pygame.display.set_mode(SIZE_SCREEN)
    FPS = 60
    size_block = 0
    start_image_1, start_image_2, image_block = None, None, None
    start_button = None
    particle_sprites = pygame.sprite.Group()
    buttons_sprites = pygame.sprite.Group()
    load_data()

    game = Tetris()
    game.start_game()
