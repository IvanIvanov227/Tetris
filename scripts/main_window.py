import copy
import os
import sys

import pygame
import random

from constants import TYPES_OF_SHAPES, START_SHAPES, START_COORDINATES, COLORS

pygame.init()
screensize = pygame.display.list_modes()
SIZE_SCREEN = width, height = screensize[6][0], screensize[6][1]
screen = pygame.display.set_mode(SIZE_SCREEN)
FPS = 60
SIZE_BLOCK = 0
image_block = None
group_buttons = []
particle_sprites = pygame.sprite.Group()
buttons_start_sprites = pygame.sprite.Group()
buttons_main_sprites = pygame.sprite.Group()
shape_sprites = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


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


def draw_shapes(x, y, surface, coords, colors):
    for i in range(len(coords)):
        line = coords[i]
        for j, cube in enumerate(line):
            if cube != 0:
                draw_cube(x + j * SIZE_BLOCK, y + i * SIZE_BLOCK, surface, colors)


def draw_cube(x, y, surface, colors):
    color1 = colors[0]
    color2 = colors[1]
    color3 = colors[2]
    color4 = colors[3]
    pygame.draw.rect(surface, color2,
                     pygame.Rect(x + SIZE_BLOCK / 4, y + SIZE_BLOCK / 4, SIZE_BLOCK / 2, SIZE_BLOCK / 2))
    pygame.draw.rect(surface, color3,
                     pygame.Rect(x, y + SIZE_BLOCK / 4, SIZE_BLOCK / 4, SIZE_BLOCK / 2))
    pygame.draw.rect(surface, color3,
                     pygame.Rect(x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK / 4, SIZE_BLOCK / 4 + 1, SIZE_BLOCK / 2))
    pygame.draw.rect(surface, color1,
                     pygame.Rect(x + SIZE_BLOCK / 4, y, SIZE_BLOCK / 2, SIZE_BLOCK / 4))
    pygame.draw.rect(surface, color4,
                     pygame.Rect(x + SIZE_BLOCK / 4, y + SIZE_BLOCK * 3 / 4, SIZE_BLOCK / 2, SIZE_BLOCK / 4 + 1))

    pygame.draw.polygon(surface, color3,
                        ((x, y), (x, y + SIZE_BLOCK / 4), (x + SIZE_BLOCK / 4, y + SIZE_BLOCK / 4)))
    pygame.draw.polygon(surface, color1,
                        ((x, y), (x + SIZE_BLOCK / 4, y), (x + SIZE_BLOCK / 4, y + SIZE_BLOCK / 4)))
    pygame.draw.polygon(surface, color1,
                        ((x + SIZE_BLOCK * 3 / 4, y), (x + SIZE_BLOCK, y),
                         (x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK / 4)))
    pygame.draw.polygon(surface, color3,
                        ((x + SIZE_BLOCK, y), (x + SIZE_BLOCK, y + SIZE_BLOCK / 4),
                         (x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK / 4)))
    pygame.draw.polygon(surface, color3,
                        ((x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK * 3 / 4),
                         (x + SIZE_BLOCK, y + SIZE_BLOCK * 3 / 4), (x + SIZE_BLOCK, y + SIZE_BLOCK)))
    pygame.draw.polygon(surface, color4,
                        ((x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK * 3 / 4),
                         (x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK), (x + SIZE_BLOCK, y + SIZE_BLOCK)))
    pygame.draw.polygon(surface, color4,
                        ((x, y + SIZE_BLOCK), (x + SIZE_BLOCK / 4, y + SIZE_BLOCK * 3 / 4),
                         (x + SIZE_BLOCK / 4, y + SIZE_BLOCK)))
    pygame.draw.polygon(surface, color3,
                        ((x, y + SIZE_BLOCK * 3 / 4), (x, y + SIZE_BLOCK),
                         (x + SIZE_BLOCK / 4, y + SIZE_BLOCK * 3 / 4)))


class Tetris:
    """Главный класс игры"""
    def __init__(self):
        self.main_game = None
        self.coords_letters = None
        self.time_draw_particle = 0
        self.new_shape = True
        self.time_key_pressed = 0
        self.start_flag = True
        self.up_button, self.right_button, self.down_button = None, None, None
        self.image_block = None
        self.down_click = None
        self.up_click = None
        self.level = 'easy'
        self.action = None

    def start_game(self):
        """Начало игры"""
        clock = pygame.time.Clock()
        screen_image = load_image('screen.png', size=(SIZE_SCREEN[0], SIZE_SCREEN[1]))
        self.load_data()
        keys = None
        while True:
            for event in pygame.event.get():
                # Получаем список зажатых клавиш
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.down_click = event.pos
                        self.up_click = None
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.up_click = event.pos

                if event.type == pygame.KEYDOWN:
                    self.check_key_down(event)

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        self.new_shape = True
                        self.time_key_pressed = 0

            if self.action is None and self.new_shape:
                if self.time_key_pressed >= 1:
                    if keys[pygame.K_LEFT]:
                        self.action = 'left'
                    elif keys[pygame.K_RIGHT]:
                        self.action = 'right'
                    elif keys[pygame.K_DOWN]:
                        self.action = 'down'
                    self.time_key_pressed = 0
                self.time_key_pressed += 0.2

            screen.blit(screen_image, (0, 0))
            self.draw_game(self.action)
            self.action = None
            pygame.display.flip()
            clock.tick(FPS)

    def check_key_down(self, event):
        if event.key in (pygame.K_w, pygame.K_UP):
            self.time_key_pressed = 0
            self.action = 'rotate'

        elif event.key in (pygame.K_a, pygame.K_LEFT):
            self.time_key_pressed = 0
            self.action = 'left'

        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            self.time_key_pressed = 0
            self.action = 'right'

        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.time_key_pressed = 0
            self.action = 'down'

        elif event.key == pygame.K_ESCAPE:
            if self.main_game is not None and not self.main_game.open_home:
                self.main_game.pause_button.image = self.main_game.pause_button.select_image
                self.main_game.set_pause()

        elif event.key == pygame.K_q:
            if self.main_game is not None and self.main_game.open_home:
                self.start_flag = True
                for button in buttons_start_sprites:
                    button.be = True
                for button in buttons_main_sprites:
                    button.be = False

    def load_data(self):
        global SIZE_BLOCK, image_block
        # картинка куба
        image = load_image('cube.png')
        SIZE_BLOCK = image.get_width()
        while 24 * SIZE_BLOCK > SIZE_SCREEN[1]:
            SIZE_BLOCK -= 1
        y = SIZE_SCREEN[1] // 4 - SIZE_BLOCK * 2 // 2
        self.coords_letters = [
            [SIZE_SCREEN[0] // 2 - 3 * SIZE_BLOCK, y, 0, -1], [SIZE_SCREEN[0] // 2 - 2 * SIZE_BLOCK, y, 0, 1],
            [SIZE_SCREEN[0] // 2 - SIZE_BLOCK, y, 0, -1], [SIZE_SCREEN[0] // 2, y, 0, 1],
            [SIZE_SCREEN[0] // 2 + SIZE_BLOCK, y, 0, -1], [SIZE_SCREEN[0] // 2 + 2 * SIZE_BLOCK, y, 0, 1]
        ]
        self.image_block = load_image('cube.png', -1, (SIZE_BLOCK, SIZE_BLOCK))
        self.load_buttons()

    def load_buttons(self):
        global group_buttons
        # Кнопка старта
        start_image_1 = load_image('start4.png', colorkey=-1, size=(5 * SIZE_BLOCK, SIZE_BLOCK * 2.5))
        start_image_2 = load_image('start3.png', colorkey=-1, size=(5 * SIZE_BLOCK, SIZE_BLOCK * 2.5))
        start_button = Button((SIZE_SCREEN[0] // 2 - 2.5 * SIZE_BLOCK,
                               SIZE_SCREEN[1] // 2 + SIZE_BLOCK * 6), start_image_1, start_image_2,
                              buttons_start_sprites,
                              self.click_start_button)
        self.up_button = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 4, SIZE_SCREEN[1] // 2 - SIZE_BLOCK * 4),
                                load_image('up.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                                load_image('up.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)), buttons_start_sprites)
        Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 4, SIZE_SCREEN[1] // 2 - SIZE_BLOCK * 2),
               load_image('left.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
               load_image('left.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)), buttons_start_sprites)
        self.right_button = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 2, SIZE_SCREEN[1] // 2 - SIZE_BLOCK * 2),
                                   load_image('right.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                                   load_image('right.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                                   buttons_start_sprites)
        self.down_button = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 4, SIZE_SCREEN[1] // 2 + SIZE_BLOCK // 10),
                                  load_image('down.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                                  load_image('down.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)), buttons_start_sprites)

        easy_img = load_image(f'easy.png', size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5), )
        normal_img = load_image(f'normal.png', size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        hard_img = load_image(f'hard.png', size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        easy_img2 = load_image(f'easy2.png', size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        normal_img2 = load_image(f'normal2.png', size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        hard_img2 = load_image(f'hard2.png', size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        easy = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 5, SIZE_BLOCK * 16), easy_img, easy_img2,
                      buttons_start_sprites,
                      lambda: self.click_level('easy'))
        easy.image = easy.select_image
        normal = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 1.8, SIZE_BLOCK * 16), normal_img, normal_img2,
                        buttons_start_sprites,
                        lambda: self.click_level('normal'))
        hard = Button((SIZE_SCREEN[0] // 2 + SIZE_BLOCK * 1.5, SIZE_BLOCK * 16), hard_img, hard_img2,
                      buttons_start_sprites,
                      lambda: self.click_level('hard'))

        group_buttons.append(GroupButtons([easy, normal, hard]))
        group_buttons.append(GroupButtons([start_button]))

    def click_start_button(self):
        self.start_flag = False
        self.main_game = MainGame(self.level, self)
        for button in buttons_start_sprites:
            button.be = False

    def click_level(self, name_level):
        self.level = name_level

    def draw_game(self, action):
        """Рисование самого дизайна игры"""
        particle_sprites.draw(screen)
        self.update_particles()
        self.draw_field()
        self.draw_buttons()

        if self.start_flag:
            self.draw_letters()
            self.draw_instruction()
            buttons_start_sprites.draw(screen)
        else:
            buttons_main_sprites.draw(screen)
            self.main_game.draw()
            self.main_game.update_shapes(action)

    def update_particles(self):
        """Обновление снежинок"""
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

    def draw_field(self):
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
        y = (SIZE_SCREEN[1] - 21 * SIZE_BLOCK) // 2
        pygame.draw.rect(screen, (11, 2, 20),
                         (x + SIZE_BLOCK, y, 10 * SIZE_BLOCK, 20 * SIZE_BLOCK))

    def draw_buttons(self):
        for group in group_buttons:
            current_button = group.check_do_select_buttons_for_group(self.up_click, self.down_click)

            if current_button is not None:
                self.up_click, self.down_click = None, None
                for button in group.buttons:
                    if button != current_button:
                        button.image = button.prev_image

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
        size = int(SIZE_SCREEN[0] / SIZE_BLOCK / 2.1)
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


class MainGame:
    def __init__(self, level, parent=None):
        self.open_home = None
        self.pause_button = None
        self.parent = parent
        self.top = (SIZE_SCREEN[1] - 21 * SIZE_BLOCK) // 2
        self.left = SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 5
        self.board = Board(10, 20, self.left, self.top)
        self.points = 0
        self.shape_now = None
        self.shape_future = None
        self.update_shape = True
        self.level = level
        self.activity = True
        self.time_update_shape = 0
        self.start_game = True
        self.count_lines = 0
        self.count_levels = 1
        # Цвета фигур после падения
        self.color1 = pygame.Color((212, 211, 201))
        self.color2 = pygame.Color((212, 211, 201))
        self.color3 = pygame.Color((212, 211, 201))
        self.color4 = pygame.Color((212, 211, 201))
        self.set_color()
        self.load_button()

    def set_color(self):
        hsv1 = self.color1.hsva
        hsv2 = self.color2.hsva
        hsv3 = self.color3.hsva
        hsv4 = self.color4.hsva
        self.color1.hsva = (hsv1[0], hsv1[1], 100, hsv1[3])
        self.color2.hsva = (hsv2[0], hsv2[1], 75, hsv1[3])
        self.color3.hsva = (hsv3[0], hsv3[1], 60, hsv1[3])
        self.color4.hsva = (hsv4[0], hsv3[1], 50, hsv1[3])

    def draw(self):
        self.board.render()
        self.draw_information()
        self.draw_field_next_shape()

        if self.update_shape:
            if not self.start_game:
                self.parent.new_shape = False
            self.start_game = False

            self.update_shape = False
            if self.shape_now is not None:
                self.shape_now.kill()
                self.shape_now = self.shape_future
            else:
                self.shape_now = Shape(self)

            self.shape_future = Shape(self)

            self.shape_now.rect.x = self.left + SIZE_BLOCK * START_COORDINATES[self.shape_now.form][0]
            self.shape_now.rect.y = self.top
            self.shape_now.set_coord_board()
            self.shape_now.set_coord_cube_board()

            self.shape_now.draw_start(0, 0, self.shape_now.image)

            count_width = len(START_SHAPES[self.shape_future.form][0])
            count_height = len(START_SHAPES[self.shape_future.form])

            font = pygame.font.Font(None, 50)
            text_h = font.render('Следующая', True, (240, 239, 224)).get_height()

            x = self.left + 12 * SIZE_BLOCK
            y = self.top + text_h
            x_center = x + SIZE_BLOCK * 3
            y_center = y + SIZE_BLOCK * 3
            self.shape_future.rect.x = x_center - SIZE_BLOCK * count_width // 2
            self.shape_future.rect.y = y_center - SIZE_BLOCK * count_height // 2
            self.shape_future.draw_start(0, 0, self.shape_future.image)

        shape_sprites.draw(screen)
        self.draw_fall_shapes()
        if self.open_home:
            self.draw_information_home()
        elif not self.activity:
            self.draw_information_pause()

    def draw_information_home(self):
        font = pygame.font.Font(None, 35)
        text_lines = ["Чтобы вернуться домой,",  "нажмите на кнопку Q"]
        rendered_lines = [font.render(line, True, (0, 0, 0)) for line in text_lines]
        text_w21 = rendered_lines[0].get_width()
        text_w22 = rendered_lines[1].get_width()
        text_h21 = rendered_lines[0].get_height()
        text_h22 = rendered_lines[1].get_height()
        text_x21 = SIZE_SCREEN[0] // 2 - text_w21 // 2
        text_x22 = SIZE_SCREEN[0] // 2 - text_w22 // 2
        text_y21 = SIZE_SCREEN[1] // 2 - text_h21 // 2
        text_y22 = text_y21 + text_h21
        background = pygame.Surface([text_w21 + 20, text_h21 + text_h22 + 20])
        background.fill((255, 255, 255))
        background.set_alpha(170)
        screen.blit(background, (text_x21 - 10, text_y21 - 10))
        screen.blit(rendered_lines[0], (text_x21, text_y21))
        screen.blit(rendered_lines[1], (text_x22, text_y22))

    def draw_information_pause(self):
        font = pygame.font.Font(None, 70)

        text = font.render('Пауза', True, (0, 0, 0))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = SIZE_SCREEN[0] // 2 - text_w // 2
        text_y = SIZE_SCREEN[1] // 2 - text_h // 2
        background = pygame.Surface([text_w + 20, text_h + 20])
        background.fill((255, 255, 255))
        background.set_alpha(170)
        screen.blit(background, (text_x - 10, text_y - 10))
        screen.blit(text, (text_x, text_y))

        font2 = pygame.font.Font(None, 35)
        text_lines = ["Чтобы продолжить, нажмите на кнопку", "или нажмите Escape"]
        rendered_lines = [font2.render(line, True, (0, 0, 0)) for line in text_lines]
        text_w21 = rendered_lines[0].get_width()
        text_w22 = rendered_lines[1].get_width()
        text_h21 = rendered_lines[0].get_height()
        text_h22 = rendered_lines[1].get_height()
        text_x21 = SIZE_SCREEN[0] // 2 - text_w21 // 2
        text_x22 = SIZE_SCREEN[0] // 2 - text_w22 // 2
        text_y21 = text_y + text_h + 50
        text_y22 = text_y21 + text_h21
        background = pygame.Surface([text_w21 + 20, text_h21 + text_h22 + 20])
        background.fill((255, 255, 255))
        background.set_alpha(170)
        screen.blit(background, (text_x21 - 10, text_y21 - 10))
        screen.blit(rendered_lines[0], (text_x21, text_y21))
        screen.blit(rendered_lines[1], (text_x22, text_y22))

    def draw_fall_shapes(self):
        board_copy = copy.deepcopy(self.board.board)
        for index, coord_line in enumerate(board_copy):
            for index2, coord in enumerate(coord_line):
                if [index2, index] in [j for i in self.shape_now.coords for j in i]:
                    board_copy[index][index2] = 0
        draw_shapes(self.left, self.top, screen, board_copy,
                    [self.color1, self.color2, self.color3, self.color4])

    def draw_information(self):
        font = pygame.font.Font(None, 50)
        text = font.render(f"Очки: {self.points}", True, (232, 229, 62))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = self.left - text_w - SIZE_BLOCK * 3
        text_y = self.top

        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (166, 164, 40), (text_x - 10, text_y - 10,
                                                  text_w + 20, text_h + 20), 4)

        text2 = font.render(f"Линии: {self.count_lines}", True, (232, 229, 62))
        text_w2 = text2.get_width()
        text_h2 = text2.get_height()
        text_x2 = self.left - text_w2 - SIZE_BLOCK * 3
        text_y2 = self.top + text_h + 50

        screen.blit(text2, (text_x2, text_y2))
        pygame.draw.rect(screen, (166, 164, 40), (text_x2 - 10, text_y2 - 10,
                                                  text_w2 + 20, text_h2 + 20), 4)

        text3 = font.render(f"Уровень: {self.count_levels}", True, (232, 229, 62))
        text_w3 = text3.get_width()
        text_h3 = text3.get_height()
        text_x3 = self.left - text_w3 - SIZE_BLOCK * 3
        text_y3 = self.top + text_h + 100 + text_h2

        screen.blit(text3, (text_x3, text_y3))
        pygame.draw.rect(screen, (166, 164, 40), (text_x3 - 10, text_y3 - 10,
                                                  text_w3 + 20, text_h3 + 20), 4)

    def draw_field_next_shape(self):
        font = pygame.font.Font(None, 50)

        text = font.render('Следующая', True, (240, 239, 224))

        text_h = text.get_height()
        text_x = self.left + 12 * SIZE_BLOCK
        text_y = self.top
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (240, 239, 224),
                         (self.left + 12 * SIZE_BLOCK, self.top + text_h, 6 * SIZE_BLOCK, 6 * SIZE_BLOCK), 4)
        x = self.left + 12 * SIZE_BLOCK
        y = self.top + text_h
        for i in range(6):
            pygame.draw.line(screen, (181, 178, 5),
                             (x + 4, y + i * SIZE_BLOCK), (x + 6 * SIZE_BLOCK - 4, y + i * SIZE_BLOCK))
            pygame.draw.line(screen, (181, 178, 5),
                             (x + i * SIZE_BLOCK, y + 4), (x + i * SIZE_BLOCK, y + 6 * SIZE_BLOCK - 4))

    def load_button(self):
        image_pause = load_image('pause.png', -1, size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2))
        image_pause2 = load_image('pause2.png', -1, size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2))
        x = SIZE_SCREEN[0] - image_pause.get_width() - 20
        y = 20
        self.pause_button = Button((x, y), image_pause, image_pause2, buttons_main_sprites, self.set_pause)

        image_home = load_image('home.png', -1, size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2))
        x = SIZE_SCREEN[0] - image_home.get_width() * 2 - 45
        home_image = Button((x, y), image_home, image_home, buttons_main_sprites, self.go_to_home)
        group_buttons.append(GroupButtons([self.pause_button, home_image]))

    def update_shapes(self, action):
        if self.activity and not self.open_home:
            if self.shape_now.update_move:
                self.shape_now.move(action)
                self.time_update_shape += self.shape_now.v
                if self.time_update_shape >= 1 and self.shape_now.update_move:
                    self.time_update_shape = 0
                    self.shape_now.move('down')

            else:
                self.update_shape = True
                self.checking_lines()

    def checking_lines(self):
        while True:
            list_indexes = []
            for index, line in enumerate(self.board.board):
                if sum(line) == 10:
                    list_indexes.append(index)

            if list_indexes:
                for index in list_indexes:
                    self.board.board[index] = [i - i for i in range(10)]

                ind = len(list_indexes) - 1
                while ind >= 0:
                    line_index = list_indexes[ind]
                    for index in range(line_index, 0, -1):
                        self.board.board[index] = self.board.board[index - 1]
                        self.board.board[index - 1] = [i - i for i in range(10)]
                    for j in range(ind):
                        list_indexes[j] += 1
                    ind -= 1
            else:
                break

    def set_pause(self):
        if self.activity:
            self.activity = False
        else:
            self.activity = True
            self.pause_button.image = self.pause_button.prev_image

    def go_to_home(self):
        if self.open_home:
            self.open_home = False
        else:
            self.activity = True
            self.open_home = True


class Shape(pygame.sprite.Sprite):
    def __init__(self, parent=None):
        super().__init__(shape_sprites)
        self.top = (SIZE_SCREEN[1] - 21 * SIZE_BLOCK) // 2
        self.left = SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 5
        color_random = random.choice(COLORS)
        self.color1 = pygame.Color(*color_random)
        self.color2 = pygame.Color(*color_random)
        self.color3 = pygame.Color(*color_random)
        self.color4 = pygame.Color(*color_random)
        self.form = random.randint(1, 7)
        self.rotate = 0
        self.color = random.choice(COLORS)
        self.set_color()
        width_image = len(TYPES_OF_SHAPES[self.form][self.rotate][0]) * SIZE_BLOCK
        height_image = len(TYPES_OF_SHAPES[self.form][self.rotate]) * SIZE_BLOCK
        self.image = pygame.Surface((width_image, height_image), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.coords = []
        self.cube_coords = []
        # После вставки в поле
        self.coordinates = None
        self.v = 0.02
        self.update_move = True
        self.parent = parent

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
                        draw_cube(x + j * SIZE_BLOCK, y + count_y * SIZE_BLOCK, surface,
                                  [self.color1, self.color2, self.color3, self.color4])
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

            self.rect.x += SIZE_BLOCK

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

            self.rect.x -= SIZE_BLOCK

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

            self.rect.y += SIZE_BLOCK
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
        width_image = len(TYPES_OF_SHAPES[self.form][self.rotate][0]) * SIZE_BLOCK
        height_image = len(TYPES_OF_SHAPES[self.form][self.rotate]) * SIZE_BLOCK
        self.image = pygame.Surface((width_image, height_image), pygame.SRCALPHA)
        draw_shapes(0, 0, self.image, TYPES_OF_SHAPES[self.form][self.rotate],
                    [self.color1, self.color2, self.color3, self.color4])


class Board:
    # создание поля
    def __init__(self, count_width, count_height, left, top):
        self.width = count_width
        self.height = count_height
        self.board = [[j - j for j in range(10 + i - i)] for i in range(20)]
        self.left = left
        self.top = top
        self.cell_size = SIZE_BLOCK

    def render(self):
        x, y = 0, 0
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (181, 178, 5),
                                 (self.left + x, self.top + y, self.cell_size, self.cell_size), 1)

                x += self.cell_size
            y += self.cell_size
            x = 0


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
    def __init__(self, coord, prev_image, select_image, group_sprites, action=None):
        super().__init__(group_sprites)
        self.be = True
        self.action = action
        self.prev_image = prev_image
        self.select_image = select_image
        self.image = prev_image
        self.rect = pygame.Rect(coord[0], coord[1], self.image.get_width(), self.image.get_height())

    def check_do_select(self, up_click, down_click):
        x = self.rect.x
        y = self.rect.y
        w = self.rect.w
        h = self.rect.h
        if self.be:
            if up_click is not None and down_click is not None and \
                x <= down_click[0] <= x + w and y <= down_click[1] <= h + y and \
                    not (x <= up_click[0] <= x + w and y <= up_click[1] <= y + h):
                self.image = self.prev_image
            elif up_click is not None and down_click is not None and (
                    x <= down_click[0] <= x + w and
                    y <= down_click[1] <= h + y):
                self.image = self.select_image
                if self.action is not None:
                    self.action()
                return True

            elif down_click is not None and \
                    x <= down_click[0] <= x + w and \
                    y <= down_click[1] <= h + y:
                self.image = self.select_image


class GroupButtons:
    def __init__(self, buttons):
        self.buttons = buttons

    def check_do_select_buttons_for_group(self, up_click, down_click):
        current_button = None
        for button in self.buttons:
            result = button.check_do_select(up_click, down_click)
            if result is True:
                current_button = button
                break
            else:
                ...
                # flag = False
                # for b in self.buttons:
                #     if b.image == b.select_image:
                #         flag = True
                #         break
                # if not flag:
                #     button.image = button.select_image
        return current_button


if __name__ == '__main__':

    pygame.display.set_caption('Тетрис')
    fullname = os.path.join('../data', 'icon.png')
    image_icon = pygame.image.load(fullname)
    pygame.display.set_icon(image_icon)

    game = Tetris()
    game.start_game()
