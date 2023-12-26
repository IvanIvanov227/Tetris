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
    global SIZE_BLOCK, image_block
    # картинка куба
    image = load_image('cube.png')
    SIZE_BLOCK = image.get_width()
    while 24 * SIZE_BLOCK > SIZE_SCREEN[1]:
        SIZE_BLOCK -= 1
    image_block = load_image('cube.png', -1, (SIZE_BLOCK, SIZE_BLOCK))
    load_buttons()


def load_buttons():
    global start_button, up_button, right_button, down_button
    # Кнопка старта
    start_image_1 = load_image('start.png', colorkey=-1, size=(4 * SIZE_BLOCK, SIZE_BLOCK * 2))
    start_image_2 = load_image('start2.png', colorkey=-1, size=(4 * SIZE_BLOCK, SIZE_BLOCK * 2))
    start_button = Button(SIZE_SCREEN[0] // 2 - 4 * SIZE_BLOCK // 2,
                          SIZE_SCREEN[1] // 2 + SIZE_BLOCK * 4, start_image_1, start_image_2)
    up_button = Button(SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 4, SIZE_SCREEN[1] // 2 - SIZE_BLOCK * 4,
                       load_image('up.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)), load_image('up.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)))
    Button(SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 4, SIZE_SCREEN[1] // 2 - SIZE_BLOCK * 2,
           load_image('left.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)), load_image('left.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)))
    right_button = Button(SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 2, SIZE_SCREEN[1] // 2 - SIZE_BLOCK * 2,
                          load_image('right.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)), load_image('right.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)))
    down_button = Button(SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 4, SIZE_SCREEN[1] // 2 + SIZE_BLOCK // 10,
                         load_image('down.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)), load_image('down.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)))
    easy_img = load_image(f'easy.png', size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
    normal_img = load_image(f'normal.png', size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
    hard_img = load_image(f'hard.png', size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
    easy_button = Button(SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 5, SIZE_BLOCK * 19, easy_img, easy_img)
    normal_button = Button(SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 1.8, SIZE_BLOCK * 19, normal_img, normal_img)
    hard_button = Button(SIZE_SCREEN[0] // 2 + SIZE_BLOCK * 1.5, SIZE_BLOCK * 19, hard_img, hard_img)


class Tetris:
    """Главный класс игры"""

    def __init__(self):
        y = SIZE_SCREEN[1] // 4 - SIZE_BLOCK * 2 // 2
        self.coords_letters = self.coords_letters = [
            [SIZE_SCREEN[0] // 2 - 3 * SIZE_BLOCK, y, 0, -1], [SIZE_SCREEN[0] // 2 - 2 * SIZE_BLOCK, y, 0, 1],
            [SIZE_SCREEN[0] // 2 - SIZE_BLOCK, y, 0, -1], [SIZE_SCREEN[0] // 2, y, 0, 1],
            [SIZE_SCREEN[0] // 2 + SIZE_BLOCK, y, 0, -1], [SIZE_SCREEN[0] // 2 + 2 * SIZE_BLOCK, y, 0, 1]
        ]
        self.start_image = None
        self.time_draw_particle = 0
        self.start_flag = True
        self.start_button = start_button
        self.up_button, self.right_button, self.down_button = up_button, right_button, down_button
        self.image_block = image_block
        self.down_click = None
        self.up_click = None

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
                        self.down_click = event.pos
                        self.up_click = None
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.up_click = event.pos
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
        y = (SIZE_SCREEN[1] - 21 * SIZE_BLOCK) // 2
        x1 = SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 6
        x = x1
        for i in range(20):
            screen.blit(self.image_block, (x1, y))
            y += SIZE_BLOCK
        x2 = x1 + SIZE_BLOCK * 11
        y = (SIZE_SCREEN[1] - 21 * SIZE_BLOCK) // 2
        for i in range(20):
            screen.blit(self.image_block, (x2, y))
            y += SIZE_BLOCK
        for i in range(12):
            screen.blit(self.image_block, (x1, y))
            x1 += SIZE_BLOCK
        y = (SIZE_SCREEN[1] - 21 * SIZE_BLOCK) // 2 + SIZE_BLOCK
        pygame.draw.rect(screen, (11, 2, 20),
                         (x + SIZE_BLOCK, y, 10 * SIZE_BLOCK, 19 * SIZE_BLOCK))

    def draw_start_screen(self):
        """Рисование стартового окна"""
        self.draw_buttons()
        self.draw_letters()
        self.draw_instruction()

    def draw_buttons(self):
        for button in buttons_sprites:
            button.check_do_select(self.up_click, self.down_click)

    def draw_letters(self):

        letters = ['T', 'E', 'T', 'R', 'I', 'S']
        for index, val in enumerate(letters):
            screen.blit(load_image(f'tetris/{val}.png', -1, size=(SIZE_BLOCK, SIZE_BLOCK)),
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
        size = int(SIZE_SCREEN[0] / SIZE_BLOCK / 1.9)
        font = pygame.font.Font(None, size)
        text = font.render("Поворот против часовой стрелки", True, (226, 235, 231))
        text_x = self.up_button.rect.x + self.up_button.rect.w
        text_y = self.up_button.rect.y + self.up_button.rect.h // 2
        screen.blit(text, (text_x, text_y))

        text2 = font.render("Смещение фигуры", True, (226, 235, 231))
        text_x2 = self.right_button.rect.x + self.right_button.rect.w
        text_y2 = self.right_button.rect.y + self.right_button.rect.h // 2
        screen.blit(text2, (text_x2, text_y2))

        text3 = font.render("Ускорение фигуры вниз", True, (226, 235, 231))
        text_x3 = self.down_button.rect.x + self.down_button.rect.w
        text_y3 = self.down_button.rect.y + self.down_button.rect.h // 2
        screen.blit(text3, (text_x3, text_y3))


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
    def __init__(self, x, y, prev_image, select_image):
        super().__init__(buttons_sprites)
        self.prev_image = prev_image
        self.select_image = select_image
        self.image = prev_image
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def check_do_select(self, up_click, down_click):
        x = self.rect.x
        y = self.rect.y
        w = self.rect.w
        h = self.rect.h
        if (up_click is None and down_click
                and x <= down_click[0] <= x + w
                and y <= down_click[1] <= h + y):
            self.image = self.select_image
        elif up_click is not None and down_click is not None and (
                x <= down_click[0] <= x + w and
                y <= down_click[1] <= h + y and x <=
                up_click[0] <= x + w and
                y <= up_click[1] <= y + w):
            self.image = self.select_image
        else:
            self.image = self.prev_image


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
    SIZE_BLOCK = 0
    image_block = None
    start_button, up_button, right_button, down_button = None, None, None, None
    particle_sprites = pygame.sprite.Group()
    buttons_sprites = pygame.sprite.Group()
    load_data()

    game = Tetris()
    game.start_game()
