import os
import sys

import pygame
import random

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

TYPES_OF_SHAPES = {
    1: {
        0: ((0, 0, 0, 0), (1, 1, 1, 1), (0, 0, 0, 0), (0, 0, 0, 0)),
        1: ((0, 0, 1, 0), (0, 0, 1, 0), (0, 0, 1, 0), (0, 0, 1, 0)),
        2: ((0, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1), (0, 0, 0, 0)),
        3: ((0, 1, 0, 0), (0, 1, 0, 0), (0, 1, 0, 0), (0, 1, 0, 0))
    },
    2: {
        0: ((1, 0, 0), (1, 1, 1), (0, 0, 0)),
        1: ((0, 1, 1), (0, 1, 0), (0, 1, 0)),
        2: ((0, 0, 0), (1, 1, 1), (0, 0, 1)),
        3: ((0, 1, 0), (0, 1, 0), (1, 1, 0))
    },
    3: {
        0: ((0, 0, 1), (1, 1, 1), (0, 0, 0)),
        1: ((0, 1, 0), (0, 1, 0), (0, 1, 1)),
        2: ((0, 0, 0), (1, 1, 1), (1, 0, 0)),
        3: ((1, 1, 0), (0, 1, 0), (0, 1, 0))
    },
    4: {
        0: ((1, 1), (1, 1)),
        1: ((1, 1), (1, 1)),
        2: ((1, 1), (1, 1)),
        3: ((1, 1), (1, 1))
    },
    5: {
        0: ((0, 1, 1), (1, 1, 0), (0, 0, 0)),
        1: ((0, 1, 0), (0, 1, 1), (0, 0, 1)),
        2: ((0, 0, 0), (0, 1, 1), (1, 1, 0)),
        3: ((1, 0, 0), (1, 1, 0), (0, 1, 0))
    },
    6: {
        0: ((0, 1, 0), (1, 1, 1), (0, 0, 0)),
        1: ((0, 1, 0), (0, 1, 1), (0, 1, 0)),
        2: ((0, 0, 0), (1, 1, 1), (0, 1, 0)),
        3: ((0, 1, 0), (1, 1, 0), (0, 1, 0))
    },
    7: {
        0: ((1, 1, 0), (0, 1, 1), (0, 0, 0)),
        1: ((0, 0, 1), (0, 1, 1), (0, 1, 0)),
        2: ((0, 0, 0), (1, 1, 0), (0, 1, 1)),
        3: ((0, 1, 0), (1, 1, 0), (1, 0, 0))
    }
}

START_COORDINATES = {
    1: (3, 0),
    2: (4, 0),
    3: (4, 0),
    4: (4, 0),
    5: (4, 0),
    6: (4, 0),
    7: (4, 0),
}

COLORS = ((19, 252, 240), (2, 13, 235), (242, 173, 15), (243, 250, 4), (26, 250, 4), (155, 4, 250), (250, 7, 49))


START_SHAPES = {
    1: ((1, 1, 1, 1), ),
    2: ((1, 0, 0), (1, 1, 1)),
    3: ((0, 0, 1), (1, 1, 1)),
    4: ((1, 1), (1, 1)),
    5: ((0, 1, 1), (1, 1, 0)),
    6: ((0, 1, 0), (1, 1, 1)),
    7: ((1, 1, 0), (0, 1, 1))
}


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


class Tetris:
    """Главный класс игры"""

    def __init__(self):
        self.main_game = None
        self.coords_letters = None
        self.time_draw_particle = 0
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
                    if event.key in (pygame.K_w, pygame.K_UP):
                        self.action = 'rotate'

                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        self.action = 'left'

                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.action = 'right'

                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        self.action = 'down'
            # if self.action is None:
            #     if keys[pygame.K_LEFT]:
            #         self.action = 'left'
            #     elif keys[pygame.K_RIGHT]:
            #         self.action = 'right'
            #     elif keys[pygame.K_DOWN]:
            #         self.action = 'down'

            screen.blit(screen_image, (0, 0))
            self.draw_game(self.action)
            self.action = None
            pygame.display.flip()
            clock.tick(FPS)

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

        image_settings = load_image('settings.png', -1, size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2))
        x = SIZE_SCREEN[0] - SIZE_BLOCK * 2 - 20
        y = 20
        group_buttons.append(GroupButtons([Button((x, y), image_settings, image_settings, buttons_start_sprites,
                                                  self.open_settings)]))

        group_buttons.append(GroupButtons([easy, normal, hard]))
        group_buttons.append(GroupButtons([start_button]))

    def click_start_button(self):
        self.start_flag = False
        self.main_game = MainGame(self.level)
        for button in buttons_start_sprites:
            button.be = False

    def click_level(self, name_level):
        self.level = name_level

    def open_settings(self):
        ...

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
    def __init__(self, level):
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
        self.load_button()

    def draw(self):
        self.board.render()

        font = pygame.font.Font(None, 50)
        text = font.render(f"Очки: {self.points}", True, (232, 229, 62))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = self.left - text_w - SIZE_BLOCK * 3
        text_y = self.top

        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (166, 164, 40), (text_x - 10, text_y - 10,
                                                  text_w + 20, text_h + 20), 4)

        pygame.draw.rect(screen, (240, 239, 224),
                         (self.left + 12 * SIZE_BLOCK, self.top, 6 * SIZE_BLOCK, 6 * SIZE_BLOCK), 4)
        x = self.left + 12 * SIZE_BLOCK
        y = self.top
        for i in range(6):
            pygame.draw.line(screen, (181, 178, 5),
                             (x + 4, y + i * SIZE_BLOCK), (x + 6 * SIZE_BLOCK - 4, y + i * SIZE_BLOCK))
            pygame.draw.line(screen, (181, 178, 5),
                             (x + i * SIZE_BLOCK, y + 4), (x + i * SIZE_BLOCK, y + 6 * SIZE_BLOCK - 4))

        x_center = x + SIZE_BLOCK * 3
        y_center = y + SIZE_BLOCK * 3
        if self.update_shape:
            self.update_shape = False
            if self.shape_now is not None:
                self.shape_now = self.shape_future
            else:
                self.shape_now = Shape(self.board)

            self.shape_future = Shape(self.board)

            count_x = len(START_SHAPES[self.shape_now.form][0]) // 2

            self.shape_now.rect.x = self.left + SIZE_BLOCK * START_COORDINATES[self.shape_now.form][0]
            self.shape_now.rect.y = self.top
            self.shape_now.set_coord_board()
            self.shape_now.set_coord_cube_board()

            self.shape_now.draw_start(0, 0, self.shape_now.image)

            count_width = len(START_SHAPES[self.shape_future.form][0])
            count_height = len(START_SHAPES[self.shape_future.form])
            self.shape_future.rect.x = x_center - SIZE_BLOCK * count_width // 2
            self.shape_future.rect.y = y_center - SIZE_BLOCK * count_height // 2
            self.shape_future.draw_start(0, 0, self.shape_future.image)

        shape_sprites.draw(screen)

    def load_button(self):
        image_pause = load_image('pause.png', -1, size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2))
        image_pause2 = load_image('pause2.png', -1, size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2))
        x = SIZE_SCREEN[0] - image_pause.get_width() - 20
        y = 20
        pause_button = Button((x, y), image_pause, image_pause2, buttons_main_sprites, self.set_pause)

        image_home = load_image('home.png', -1, size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2))
        x = SIZE_SCREEN[0] - image_home.get_width() * 2 - 45
        home_image = Button((x, y), image_home, image_home, buttons_main_sprites, self.go_to_home)
        group_buttons.append(GroupButtons([pause_button, home_image]))

    def update_shapes(self, action):
        if self.activity:
            if self.shape_now.update_move:
                self.shape_now.update(action)
                self.time_update_shape += self.shape_now.v
                if self.time_update_shape >= 1 and self.shape_now.update_move:
                    self.time_update_shape = 0
                    self.shape_now.update('down')
            else:
                self.update_shape = True

    def set_pause(self):
        if self.activity:
            self.activity = False
        else:
            self.activity = True

    def go_to_home(self):
        ...


class Shape(pygame.sprite.Sprite):
    def __init__(self, board):
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
        self.board = board
        self.coords = []
        self.cube_coords = []
        self.index_coords = []
        self.v = 0.02
        self.update_move = True

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
                self.board.board[i][start_x + j] += START_SHAPES[self.form][i][j]

    def set_coord_cube_board(self):
        self.cube_coords = []
        start_x = START_COORDINATES[self.form][0]
        for i in range(len(TYPES_OF_SHAPES[self.form][self.rotate])):
            self.cube_coords.append([])
            for j in range(len(TYPES_OF_SHAPES[self.form][self.rotate][0])):
                self.cube_coords[-1].append([start_x + j, i])

        for index, coord_line in enumerate(self.cube_coords):
            for index2, coord in enumerate(coord_line):
                if coord in [j for i in self.coords for j in i]:
                    self.index_coords.append([index, index2])

    def draw(self, x, y, surface):
        i = 0
        n = len(TYPES_OF_SHAPES[self.form][self.rotate])
        while i < n:
            line = TYPES_OF_SHAPES[self.form][self.rotate][i]
            for j, cube in enumerate(line):
                if cube != 0:
                    self.draw_cube(x + j * SIZE_BLOCK, y + i * SIZE_BLOCK, surface)
            i += 1

    def draw_start(self, x, y, surface):
        i = 0
        count_y = 0
        n = len(TYPES_OF_SHAPES[self.form][self.rotate])
        while i < n:
            line = TYPES_OF_SHAPES[self.form][self.rotate][i]
            if sum(line) != 0:
                for j, cube in enumerate(line):
                    if cube != 0:
                        self.draw_cube(x + j * SIZE_BLOCK, y + count_y * SIZE_BLOCK, surface)
                count_y += 1
            i += 1

    def draw_cube(self, x, y, surface):
        pygame.draw.rect(surface, self.color2,
                         pygame.Rect(x + SIZE_BLOCK / 4, y + SIZE_BLOCK / 4, SIZE_BLOCK / 2, SIZE_BLOCK / 2))
        pygame.draw.rect(surface, self.color3,
                         pygame.Rect(x, y + SIZE_BLOCK / 4, SIZE_BLOCK / 4, SIZE_BLOCK / 2))
        pygame.draw.rect(surface, self.color3,
                         pygame.Rect(x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK / 4, SIZE_BLOCK / 4 + 1, SIZE_BLOCK / 2))
        pygame.draw.rect(surface, self.color1,
                         pygame.Rect(x + SIZE_BLOCK / 4, y, SIZE_BLOCK / 2, SIZE_BLOCK / 4))
        pygame.draw.rect(surface, self.color4,
                         pygame.Rect(x + SIZE_BLOCK / 4, y + SIZE_BLOCK * 3 / 4, SIZE_BLOCK / 2, SIZE_BLOCK / 4 + 1))

        pygame.draw.polygon(surface, self.color3,
                            ((x, y), (x, y + SIZE_BLOCK / 4), (x + SIZE_BLOCK / 4, y + SIZE_BLOCK / 4)))
        pygame.draw.polygon(surface, self.color3,
                            ((x, y + SIZE_BLOCK * 3 / 4), (x, y + SIZE_BLOCK),
                             (x + SIZE_BLOCK / 4, y + SIZE_BLOCK * 3 / 4)))
        pygame.draw.polygon(surface, self.color1,
                            ((x, y), (x + SIZE_BLOCK / 4, y), (x + SIZE_BLOCK / 4, y + SIZE_BLOCK / 4)))
        pygame.draw.polygon(surface, self.color1,
                            ((x + SIZE_BLOCK * 3 / 4, y), (x + SIZE_BLOCK, y),
                             (x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK / 4)))
        pygame.draw.polygon(surface, self.color3,
                            ((x + SIZE_BLOCK, y), (x + SIZE_BLOCK, y + SIZE_BLOCK / 4),
                             (x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK / 4)))
        pygame.draw.polygon(surface, self.color3,
                            ((x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK * 3 / 4),
                             (x + SIZE_BLOCK, y + SIZE_BLOCK * 3 / 4), (x + SIZE_BLOCK, y + SIZE_BLOCK)))
        pygame.draw.polygon(surface, self.color4,
                            ((x, y + SIZE_BLOCK), (x + SIZE_BLOCK / 4, y + SIZE_BLOCK * 3 / 4),
                             (x + SIZE_BLOCK / 4, y + SIZE_BLOCK)))
        pygame.draw.polygon(surface, self.color4,
                            ((x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK * 3 / 4),
                             (x + SIZE_BLOCK * 3 / 4, y + SIZE_BLOCK), (x + SIZE_BLOCK, y + SIZE_BLOCK)))

    def update(self, action):

        if action == 'left':
            result = self.check_move_left()
            if result is True:
                for index, coord_line in enumerate(self.coords):
                    for index2, coord in enumerate(coord_line):
                        self.board.board[coord[1]][coord[0]] = 0
                        self.coords[index][index2] = [coord[0] - 1, coord[1]]
                        self.board.board[coord[1]][coord[0] - 1] = 1

                for index, coord_line in enumerate(self.cube_coords):
                    for index2, coord in enumerate(coord_line):
                        self.cube_coords[index][index2][0] -= 1

                self.rect.x -= SIZE_BLOCK

        elif action == 'right':
            result = self.check_move_right()
            if result is True:
                for index, coord_line in enumerate(self.coords):
                    for index2, coord in enumerate(coord_line[::-1]):
                        index2 = len(coord_line) - index2 - 1
                        self.board.board[coord[1]][coord[0]] = 0
                        self.coords[index][index2] = [coord[0] + 1, coord[1]]
                        self.board.board[coord[1]][coord[0] + 1] = 1

                for index, coord_line in enumerate(self.cube_coords):
                    for index2, coord in enumerate(coord_line):
                        self.cube_coords[index][index2][0] += 1

                self.rect.x += SIZE_BLOCK

        elif action == 'down':
            result = self.check_move_down()
            if result is True:

                for index, coord_line in enumerate(self.coords[::-1]):
                    index = len(self.coords) - index - 1
                    for index2, coord in enumerate(coord_line):
                        self.board.board[coord[1]][coord[0]] = 0
                        self.coords[index][index2] = [coord[0], coord[1] + 1]
                        self.board.board[coord[1] + 1][coord[0]] = 1

                for index, coord_line in enumerate(self.cube_coords):
                    for index2, coord in enumerate(coord_line):
                        self.cube_coords[index][index2][1] += 1

                self.rect.y += SIZE_BLOCK
            else:
                self.update_move = False

        elif action == 'rotate':
            self.rotate_shape()

    def check_move_left(self):

        for coord_line in self.coords:
            coord = coord_line[0]
            if coord[0] == 0 or self.board.board[coord[1]][coord[0] - 1]:
                return False
        return True

    def check_move_right(self):
        for coord_line in self.coords:
            coord = coord_line[-1]
            if coord[0] == 9 or self.board.board[coord[1]][coord[0] + 1]:
                return False
        return True

    def check_move_down(self):
        print('down', self.coords)
        for coord_line in self.coords:
            for coord in coord_line:
                if coord[1] == 19 or (self.board.board[coord[1] + 1][coord[0]] and [coord[0], coord[1] + 1] not in [j for i in self.coords for j in i]):
                    print('\n')
                    return False
        return True

    def rotate_shape(self):
        self.rotate = (self.rotate + 1) % 4
        new_coords = []
        i = 0
        index = 0
        n = len(TYPES_OF_SHAPES[self.form][self.rotate])

        while i < n:
            coord_line = TYPES_OF_SHAPES[self.form][self.rotate][index]
            if sum(coord_line) != 0:
                new_coords.append([])
                index2 = 0

                n2 = len(coord_line)
                while index2 < n2:
                    coord = coord_line[index2]
                    if coord == 1:
                        new_coords[-1].append(self.cube_coords[index][index2])
                    index2 += 1
            index += 1
            i += 1

        for index, coord_line in enumerate(new_coords):
            for index2, coord in enumerate(coord_line):
                if coord[1] > 19 or coord[1] < 0 or coord[0] < 0 or coord[0] > 9:
                    self.rotate = (self.rotate - 1) % 4
                    return
                elif coord not in [j for i in self.coords for j in i] and self.board.board[coord[1]][coord[0]] == 1:
                    self.rotate = (self.rotate - 1) % 4
                    return
        for index, coord_line in enumerate(self.coords):
            for index2, coord in enumerate(coord_line):
                self.board.board[coord[1]][coord[0]] = 0

        for index, coord_line in enumerate(new_coords):
            for index2, coord in enumerate(coord_line):
                self.board.board[coord[1]][coord[0]] = 1

        self.coords = new_coords

        width_image = len(TYPES_OF_SHAPES[self.form][self.rotate][0]) * SIZE_BLOCK
        height_image = len(TYPES_OF_SHAPES[self.form][self.rotate]) * SIZE_BLOCK
        self.image = pygame.Surface((width_image, height_image), pygame.SRCALPHA)
        self.draw(0, 0, self.image)
        print(self.coords)


class Board:
    # создание поля
    def __init__(self, count_width, count_height, left, top):
        self.width = count_width
        self.height = count_height
        self.board = [[0 for j in range(10)] for i in range(20)]
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
