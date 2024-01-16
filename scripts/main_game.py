import copy
import os
import sys

import pygame
import random

import sqlite3

from constants import START_SHAPES, START_COORDINATES, PHRASES, FPS
from button import Button, GroupButtons, ComboButton
from shape import Shape, draw_shapes
from particle import Particle
from board import Board

SIZE_SCREEN = (1000, 600)
screen = pygame.display.set_mode(SIZE_SCREEN, pygame.RESIZABLE)
pygame.display.set_caption('Тетрис')
fullname = os.path.join('../data/images', 'icon.png')
image_icon = pygame.image.load(fullname)
pygame.display.set_icon(image_icon)
SIZE_BLOCK = 0

LANGUAGE = 'ru'
SOUND = 'on'
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
    full_name = os.path.join('../data/images/', name)
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


# def increase_volume(sound, limit, step):
#     if int(sound.get_volume()) != int(limit):
#         sound.set_volume(sound.get_volume() + step)

def draw_black_screen():
    black_sur = pygame.surface.Surface(SIZE_SCREEN)
    black_sur.set_alpha(200)
    black_sur.fill((0, 0, 0))
    screen.blit(black_sur, (0, 0))


def draw_frame_and_surface(x_frame, y_frame, width_frame, height_frame):
    pygame.draw.rect(screen, (255, 255, 255),
                     (x_frame, y_frame, width_frame, height_frame), 4)
    background = pygame.Surface((width_frame, height_frame))
    background.fill((255, 255, 255))
    background.set_alpha(170)
    screen.blit(background, (x_frame, y_frame))


def draw_text_in_black_screen(lines):
    min_text_x = 1000000000
    max_text_w = 0
    height = 0
    y = SIZE_SCREEN[1] // 2
    for line in lines:
        size = line[0]
        font = pygame.font.Font(None, size)
        text = font.render(line[1], True, (0, 0, 0))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = SIZE_SCREEN[0] // 2 - text_w // 2
        y -= text_h // 2
        min_text_x = min(min_text_x, text_x)
        max_text_w = max(max_text_w, text_w)
        height += text_h
    y_min = y
    draw_frame_and_surface(min_text_x - SIZE_BLOCK, y_min - SIZE_BLOCK, max_text_w + SIZE_BLOCK * 2,
                           height + SIZE_BLOCK * 2)
    for line in lines:
        size = line[0]
        font = pygame.font.Font(None, size)
        text = font.render(line[1], True, (0, 0, 0))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = SIZE_SCREEN[0] // 2 - text_w // 2
        screen.blit(text, (text_x, y))
        y += text_h


class Tetris:
    """Главный класс игры"""

    def __init__(self):
        self.button_open_black_screen = None
        self.connect = sqlite3.connect('../data/rating.sqlite')
        self.cur = self.connect.cursor()
        self.sound_main = None
        self.start_buttons = dict()
        self.main_game = None
        self.coords_letters = None
        self.time_draw_particle = 0
        self.new_shape = True
        self.time_key_pressed = 0
        self.sleep_key_pressed = None
        self.start_flag = True
        self.image_block = None
        self.down_click = None
        self.up_click = None
        self.level = 'easy'
        self.action = None
        self.activity_window = None

    def start_game(self):
        """Начало игры"""
        clock = pygame.time.Clock()
        screen_image = load_image('screen.png', size=(SIZE_SCREEN[0], SIZE_SCREEN[1]))
        self.load_data()
        keys = None
        self.sound_main = pygame.mixer.Sound('../data/music/main_music.mp3')
        self.sound_main.set_volume(0.1)
        self.sound_main.play()
        while True:
            if not pygame.mixer.get_busy():
                self.sound_main.play()

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
                if event.type == pygame.VIDEORESIZE:
                    self.screen_resize(event)
                    screen_image = load_image('screen.png', size=(SIZE_SCREEN[0], SIZE_SCREEN[1]))

            self.key_pressed_check(keys)

            screen.blit(screen_image, (0, 0))
            self.draw_game(self.action)
            self.action = None
            pygame.display.flip()
            clock.tick(FPS)

    def screen_resize(self, event):
        global screen, SIZE_BLOCK, SIZE_SCREEN, image_block, group_buttons
        SIZE_SCREEN = (event.w, event.h)
        screen = pygame.display.set_mode(SIZE_SCREEN, pygame.RESIZABLE)
        pygame.display.set_icon(image_icon)

        while 24 * SIZE_BLOCK > SIZE_SCREEN[1]:
            SIZE_BLOCK -= 1
        while 24 * SIZE_BLOCK < SIZE_SCREEN[1]:
            SIZE_BLOCK += 1
        y = SIZE_SCREEN[1] // 4 - SIZE_BLOCK * 2 // 2
        self.image_block = load_image('cube.png', -1, (SIZE_BLOCK, SIZE_BLOCK))
        for index, coord in enumerate(self.coords_letters):
            self.coords_letters[index][0] = SIZE_SCREEN[0] // 2 + (-3 + index) * SIZE_BLOCK
            self.coords_letters[index][1] = y

        buttons_start_sprites.empty()
        self.start_buttons = dict()
        group_buttons = []
        self.load_buttons()

    def key_pressed_check(self, keys):
        if self.action is None and self.new_shape and not self.start_flag:
            if self.time_key_pressed >= 1:
                if keys[pygame.K_LEFT]:
                    self.action = 'left'
                elif keys[pygame.K_RIGHT]:
                    self.action = 'right'
                elif keys[pygame.K_DOWN]:
                    self.action = 'down'
                self.time_key_pressed = 0
            self.time_key_pressed += self.sleep_key_pressed

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
            if (self.main_game is not None and not self.main_game.open_home and
                    self.main_game.main_game_buttons['pause_button'].be):
                self.main_game.main_game_buttons['pause_button'].image = (
                    self.main_game.main_game_buttons['pause_button'].click_image)
                self.main_game.set_pause()

        elif event.key == pygame.K_q:
            if self.main_game is not None and self.main_game.open_home:
                self.return_home()

        elif event.key == pygame.K_RETURN:
            if self.main_game is not None and self.main_game.finish:
                self.return_home()

    def return_home(self):
        global screen
        shape_sprites.empty()
        buttons_main_sprites.empty()

        self.start_flag = True
        for index, group in enumerate(group_buttons):
            if self.main_game.main_game_buttons['pause_button'] in group.buttons:
                del group_buttons[index]
                break
        for name in self.start_buttons:
            if self.start_buttons[name].be is False:
                self.start_buttons[name].be = True
            else:
                self.start_buttons[name].be = False
        self.main_game = None
        self.button_open_black_screen = None
        self.activity_window = None
        if SOUND != 'off':
            self.sound_main.set_volume(0.1)

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
        self.start_buttons['easy_button'].image = self.start_buttons['easy_button'].click_image
        self.start_buttons['easy_button'].name_new_image = 'click'

    def load_buttons(self):
        global group_buttons
        # Кнопка старта
        start_image_1 = load_image('start_russian_prev.png', colorkey=-1, size=(5 * SIZE_BLOCK, SIZE_BLOCK * 2.5))
        start_image_2 = load_image('start_russian_click.png', colorkey=-1, size=(5 * SIZE_BLOCK, SIZE_BLOCK * 2.5))
        start_button = Button((SIZE_SCREEN[0] // 2 - 2.5 * SIZE_BLOCK,
                               SIZE_SCREEN[1] // 2 + SIZE_BLOCK * 6), start_image_1, start_image_2, start_image_1,
                              buttons_start_sprites,
                              self.click_start_button, 'default_button_click.mp3')
        self.start_buttons['start_button'] = start_button
        up_button = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 4, SIZE_SCREEN[1] // 2 - SIZE_BLOCK * 4),
                           load_image('up.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                           load_image('up.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                           load_image('up.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                           buttons_start_sprites)
        left_button = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 4, SIZE_SCREEN[1] // 2 - SIZE_BLOCK * 2),
                             load_image('left.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                             load_image('left.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                             load_image('left.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                             buttons_start_sprites)
        right_button = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 2, SIZE_SCREEN[1] // 2 - SIZE_BLOCK * 2),
                              load_image('right.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                              load_image('right.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                              load_image('right.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                              buttons_start_sprites)
        down_button = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 4, SIZE_SCREEN[1] // 2 + SIZE_BLOCK // 10),
                             load_image('down.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                             load_image('down.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                             load_image('down.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2)),
                             buttons_start_sprites)
        self.start_buttons['up_button'] = up_button
        self.start_buttons['left_button'] = left_button
        self.start_buttons['right_button'] = right_button
        self.start_buttons['down_button'] = down_button

        easy_img = load_image(PHRASES['ru']['easy_button_prev'], size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        normal_img = load_image(PHRASES['ru']['normal_button_prev'], size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        hard_img = load_image(PHRASES['ru']['hard_button_prev'], size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        easy_img2 = load_image(PHRASES['ru']['easy_button_click'], size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        normal_img2 = load_image(PHRASES['ru']['normal_button_click'], size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        hard_img2 = load_image(PHRASES['ru']['hard_button_click'], size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        easy = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 5, SIZE_BLOCK * 16), easy_img, easy_img2, easy_img2,
                      buttons_start_sprites,
                      lambda: self.click_level('easy'), 'default_button_click.mp3')

        normal = Button((SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 1.8, SIZE_BLOCK * 16),
                        normal_img, normal_img2, normal_img2, buttons_start_sprites, lambda: self.click_level('normal'),
                        'default_button_click.mp3')
        hard = Button((SIZE_SCREEN[0] // 2 + SIZE_BLOCK * 1.5, SIZE_BLOCK * 16), hard_img, hard_img2, hard_img2,
                      buttons_start_sprites,
                      lambda: self.click_level('hard'), 'default_button_click.mp3')
        self.start_buttons['easy_button'] = easy
        self.start_buttons['normal_button'] = normal
        self.start_buttons['hard_button'] = hard

        language_image_russian = load_image('russian.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 1.5))
        language_image_english = load_image('english.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 1.5))
        sound_image = load_image('sound.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 1.5))
        not_sound_image = load_image('not_sound.png', size=(SIZE_BLOCK * 2, SIZE_BLOCK * 1.5))
        records_image = load_image('records.png', -1, size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2))

        language_button = ComboButton((SIZE_BLOCK, SIZE_SCREEN[1] - SIZE_BLOCK * 4 - 10),
                                      language_image_russian, language_image_english,
                                      buttons_start_sprites, self.set_language,
                                      'default_button_click.mp3')

        sound_button = ComboButton((SIZE_BLOCK, SIZE_SCREEN[1] - SIZE_BLOCK * 2),
                                   sound_image, not_sound_image, buttons_start_sprites,
                                   self.set_sound, 'default_button_click.mp3')

        records_button = Button((SIZE_SCREEN[0] - SIZE_BLOCK * 2 - 10, SIZE_BLOCK // 2), records_image, records_image,
                                records_image, buttons_start_sprites, self.records_draw, 'default_button_click.mp3')
        self.start_buttons['language_button'] = language_button
        self.start_buttons['sound_button'] = sound_button
        self.start_buttons['records_button'] = records_button

        group_buttons.append(GroupButtons([language_button]))
        group_buttons.append(GroupButtons([sound_button]))
        group_buttons.append(GroupButtons([records_button]))

        group_buttons.append(GroupButtons([easy, normal, hard]))
        group_buttons.append(GroupButtons([start_button]))

    def records_draw(self):
        if self.button_open_black_screen is not None:
            for name in self.start_buttons:
                if self.start_buttons[name] != self.button_open_black_screen:
                    if self.start_buttons[name].be is False:
                        self.start_buttons[name].be = True
                    else:
                        self.start_buttons[name].be = False
            self.button_open_black_screen = None
            self.activity_window = None

        else:
            self.activity_window = self.draw_record_menu
            self.button_open_black_screen = self.start_buttons['records_button']
            for name in self.start_buttons:
                if self.start_buttons[name] != self.button_open_black_screen:
                    if self.start_buttons[name].be is False:
                        self.start_buttons[name].be = True
                    else:
                        self.start_buttons[name].be = False

    def draw_record_menu(self):
        best_level = int(self.cur.execute('SELECT best_level FROM best_results WHERE id = 1').fetchone()[0])
        best_score = int(self.cur.execute('SELECT best_score FROM best_results WHERE id = 1').fetchone()[0])
        more_lines = int(self.cur.execute('SELECT more_lines FROM best_results WHERE id = 1').fetchone()[0])
        more_shape = int(self.cur.execute('SELECT more_shape FROM best_results WHERE id = 1').fetchone()[0])
        size = SIZE_SCREEN[0] // 100 * 4
        size2 = SIZE_SCREEN[0] // 100 * 3
        lines = (
            (size, PHRASES[LANGUAGE]['records']),
            (size2, f" "),
            (size2, f"{PHRASES[LANGUAGE]['score']}      {best_score}"),
            (size2, f" "),
            (size2, f"{PHRASES[LANGUAGE]['level']}      {best_level}"),
            (size2, f" "),
            (size2, f"{PHRASES[LANGUAGE]['lines']}      {more_lines}"),
            (size2, f" "),
            (size2, f"{PHRASES[LANGUAGE]['shapes']}       {more_shape}")
        )
        draw_text_in_black_screen(lines)

    def set_language(self, number):
        global LANGUAGE
        if number == '1':
            LANGUAGE = 'ru'
        else:
            LANGUAGE = 'eng'
        self.update_languages_buttons()

    def update_languages_buttons(self):
        self.start_buttons['easy_button'].prev_image = load_image(PHRASES[LANGUAGE]['easy_button_prev'],
                                                                  size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        self.start_buttons['easy_button'].current_image = load_image(PHRASES[LANGUAGE]['easy_button_click'],
                                                                     size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        self.start_buttons['easy_button'].click_image = load_image(PHRASES[LANGUAGE]['easy_button_click'],
                                                                   size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))

        self.start_buttons['normal_button'].prev_image = load_image(PHRASES[LANGUAGE]['normal_button_prev'],
                                                                    size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        self.start_buttons['normal_button'].current_image = load_image(PHRASES[LANGUAGE]['normal_button_click'],
                                                                       size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        self.start_buttons['normal_button'].click_image = load_image(PHRASES[LANGUAGE]['normal_button_click'],
                                                                     size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))

        self.start_buttons['hard_button'].prev_image = load_image(PHRASES[LANGUAGE]['hard_button_prev'],
                                                                  size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        self.start_buttons['hard_button'].current_image = load_image(PHRASES[LANGUAGE]['hard_button_click'],
                                                                     size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))
        self.start_buttons['hard_button'].click_image = load_image(PHRASES[LANGUAGE]['hard_button_click'],
                                                                   size=(SIZE_BLOCK * 3.2, SIZE_BLOCK * 1.5))

        self.start_buttons['start_button'].prev_image = load_image(PHRASES[LANGUAGE]['start_button_prev'],
                                                                   size=(SIZE_BLOCK * 5, SIZE_BLOCK * 2.5))
        self.start_buttons['start_button'].current_image = load_image(PHRASES[LANGUAGE]['start_button_click'],
                                                                      size=(SIZE_BLOCK * 5, SIZE_BLOCK * 2.5))
        self.start_buttons['start_button'].click_image = load_image(PHRASES[LANGUAGE]['start_button_prev'],
                                                                    size=(SIZE_BLOCK * 5, SIZE_BLOCK * 2.5))

        self.start_buttons['easy_button'].update_image()
        self.start_buttons['normal_button'].update_image()
        self.start_buttons['hard_button'].update_image()
        self.start_buttons['start_button'].update_image()

    def set_sound(self, number):
        global SOUND
        if number == '1':
            SOUND = 'on'
        else:
            SOUND = 'off'
        if SOUND == 'off':
            self.sound_main.set_volume(0.0)
        else:
            self.sound_main.set_volume(0.1)

    def click_start_button(self):
        global screen
        self.start_flag = False
        self.main_game = MainGame(self.level, self)

        for name in self.start_buttons:
            if self.start_buttons[name].be is False:
                self.start_buttons[name].be = True
            else:
                self.start_buttons[name].be = False
        if self.level == 'easy':
            self.sleep_key_pressed = 0.2
        elif self.level == 'normal':
            self.sleep_key_pressed = 0.3
        else:
            self.sleep_key_pressed = 0.4

    def click_level(self, name_level):
        self.level = name_level

    def draw_game(self, action):
        """Рисование самого дизайна игры"""
        particle_sprites.draw(screen)
        self.update_particles()
        self.draw_field()
        self.check_click_button()

        if self.start_flag:
            self.draw_letters()
            self.draw_instruction()
            buttons_start_sprites.draw(screen)
            self.draw_autor()

        else:
            buttons_main_sprites.draw(screen)
            self.main_game.draw()
            self.main_game.update_shapes(action)
            self.draw_autor()

        if self.button_open_black_screen not in (None, True):
            draw_black_screen()
            screen.blit(self.button_open_black_screen.image,
                        (self.button_open_black_screen.rect.x, self.button_open_black_screen.rect.y))

        if self.activity_window is not None:
            self.activity_window()

    def update_particles(self):
        """Обновление снежинок"""
        self.time_draw_particle += 0.01

        if self.time_draw_particle >= 1:
            self.time_draw_particle = 0
            Particle(random.random() * SIZE_SCREEN[0], SIZE_SCREEN[1],
                     random.randint(15, 30), random.randint(2, 4), particle_sprites)

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

    def check_click_button(self):
        for group in group_buttons:
            current_button = group.check_do_select_buttons_for_group(self.up_click, self.down_click, SOUND)
            if current_button is not None:
                self.up_click, self.down_click = None, None
                for button in group.buttons:
                    if button != current_button:
                        button.image = button.prev_image
                        button.name_new_image = 'prev'

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
        size = int(SIZE_SCREEN[0] // 100 * 1.5)
        font = pygame.font.Font(None, size)
        text = font.render(PHRASES[LANGUAGE]['information_rotate'], True, (226, 235, 231))
        up_button = self.start_buttons['up_button']
        right_button = self.start_buttons['right_button']
        down_button = self.start_buttons['down_button']

        text_x = up_button.rect.x + up_button.rect.w
        text_y = up_button.rect.y + up_button.rect.h // 2
        screen.blit(text, (text_x, text_y))

        text2 = font.render(PHRASES[LANGUAGE]['information_shift_shape'], True, (226, 235, 231))
        text_x2 = right_button.rect.x + right_button.rect.w
        text_y2 = right_button.rect.y + right_button.rect.h // 2
        screen.blit(text2, (text_x2, text_y2))

        text3 = font.render(PHRASES[LANGUAGE]['accelerating_down_shape'], True, (226, 235, 231))
        text_x3 = down_button.rect.x + down_button.rect.w

        text_y3 = down_button.rect.y + down_button.rect.h // 2
        screen.blit(text3, (text_x3, text_y3))

    def draw_autor(self):
        font = pygame.font.Font(None, int(SIZE_SCREEN[0] // 100 * 1.5))
        text = font.render('@alexsivkov', True, (226, 235, 231))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = SIZE_SCREEN[0] - text_w - 10
        text_y = SIZE_SCREEN[1] - text_h - 10
        screen.blit(text, (text_x, text_y))


class MainGame:
    def __init__(self, level, parent=None):
        self.connect = sqlite3.connect('../data/rating.sqlite')
        self.cur = self.connect.cursor()
        self.finish_music = False
        self.main_game_buttons = dict()
        self.open_home = None
        self.parent = parent
        self.top = (SIZE_SCREEN[1] - 21 * SIZE_BLOCK) // 2
        self.left = SIZE_SCREEN[0] // 2 - SIZE_BLOCK * 5
        self.board = Board(10, 20, self.left, self.top, SIZE_BLOCK)
        self.score = 0
        self.shape_now = None
        self.shape_future = None
        self.update_shape = True
        self.activity = True
        self.time_update_shape = 0
        self.start_game = True
        self.count_lines = 0
        self.count_levels = 0
        self.level = level
        self.finish = False
        if level == 'easy':
            self.v_level = 0.02
        elif level == 'normal':
            self.v_level = 0.03
        else:
            self.v_level = 0.04
        self.count_shapes = 0
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
        self.board.render(screen)
        self.draw_information()
        self.draw_field_next_shape()
        if self.update_shape and not self.finish:
            self.check_results()
            self.count_shapes += 1
            if not self.start_game:
                self.parent.new_shape = False
            self.start_game = False

            self.update_shape = False
            if self.shape_now is not None:
                self.shape_now.kill()
                self.shape_now = self.shape_future
            else:
                self.shape_now = Shape(self.count_levels, shape_sprites, SIZE_SCREEN, SIZE_BLOCK, parent=self)
            self.shape_future = Shape(self.count_levels, shape_sprites, SIZE_SCREEN, SIZE_BLOCK, parent=self)

            self.shape_now.rect.x = self.left + SIZE_BLOCK * START_COORDINATES[self.shape_now.form][0]
            self.shape_now.rect.y = self.top
            self.shape_now.set_coord_board()
            self.shape_now.set_coord_cube_board()
            result = self.check_continuation_game()
            if not result:
                self.finish = True
                self.finish_game()

            self.shape_now.draw_start(0, 0, self.shape_now.image)

            count_width = len(START_SHAPES[self.shape_future.form][0])
            count_height = len(START_SHAPES[self.shape_future.form])

            font = pygame.font.Font(None, int(SIZE_SCREEN[0] // 100 * 2.5))
            text2 = font.render(PHRASES[LANGUAGE]['next_shape'][1], True, (240, 239, 224)).get_height()

            x = self.left + 12 * SIZE_BLOCK
            y = self.top * 2 + text2 + 5
            x_center = x + SIZE_BLOCK * 3
            y_center = y + SIZE_BLOCK * 3
            self.shape_future.rect.x = x_center - SIZE_BLOCK * count_width // 2
            self.shape_future.rect.y = y_center - SIZE_BLOCK * count_height // 2
            self.shape_future.draw_start(0, 0, self.shape_future.image)

        shape_sprites.draw(screen)
        self.draw_fall_shapes()

    def check_results(self):
        best_score = int(self.cur.execute('SELECT best_score FROM best_results WHERE id = 1').fetchone()[0])
        best_level = int(self.cur.execute('SELECT best_level FROM best_results WHERE id = 1').fetchone()[0])
        more_lines = int(self.cur.execute('SELECT more_lines FROM best_results WHERE id = 1').fetchone()[0])
        more_shape = int(self.cur.execute('SELECT more_shape FROM best_results WHERE id = 1').fetchone()[0])

        if self.score > best_score:
            self.cur.execute('UPDATE best_results SET best_score = ? WHERE id = 1', (self.score,))
        if self.count_levels > best_level:
            self.cur.execute('UPDATE best_results SET best_level = ? WHERE id = 1', (self.count_levels,))
        if self.count_lines > more_lines:
            self.cur.execute('UPDATE best_results SET more_lines = ? WHERE id = 1', (self.count_lines,))
        if self.count_shapes > more_shape:
            self.cur.execute('UPDATE best_results SET more_shape = ? WHERE id = 1', (self.count_shapes,))

        self.connect.commit()

    def finish_game(self):
        for name in self.main_game_buttons:
            if self.main_game_buttons[name].be is False:
                self.main_game_buttons[name].be = True
            else:
                self.main_game_buttons[name].be = False
        self.parent.activity_window = self.finish_draw

    def finish_draw(self):
        draw_black_screen()
        size = int(SIZE_SCREEN[0] // 100 * 4)
        lines = (
            (size, PHRASES[LANGUAGE]['finish_information'][0]),
            (size, PHRASES[LANGUAGE]['finish_information'][1]),
            (size, PHRASES[LANGUAGE]['finish_information'][2])
        )
        draw_text_in_black_screen(lines)

        if not self.finish_music:
            self.finish_music_func()

    def finish_music_func(self):
        if SOUND == 'on':
            self.parent.sound_main.set_volume(0.0)
            sound = pygame.mixer.Sound('../data/music/game_lost.mp3')
            sound.play()
        self.finish_music = True

    def check_continuation_game(self):
        for coord_line in self.board.board:
            for coord in coord_line:
                if coord == 2:
                    return False
        return True

    def draw_information_home(self):
        size = int(SIZE_SCREEN[0] // 100 * 4)
        lines = (
            (size, PHRASES[LANGUAGE]['home_information'][0]),
            (size, PHRASES[LANGUAGE]['home_information'][1])
        )
        draw_text_in_black_screen(lines)

    def draw_information_pause(self):
        size1 = int(SIZE_SCREEN[0] // 100 * 4)
        size2 = int(SIZE_SCREEN[0] // 100 * 3)
        lines = (
            (size1, PHRASES[LANGUAGE]['pause']),
            (size2, PHRASES[LANGUAGE]['pause_information'][0]),
            (size2, PHRASES[LANGUAGE]['pause_information'][1])
        )

        draw_text_in_black_screen(lines)

    def draw_fall_shapes(self):
        board_copy = copy.deepcopy(self.board.board)
        for index, coord_line in enumerate(board_copy):
            for index2, coord in enumerate(coord_line):
                if [index2, index] in [j for i in self.shape_now.coords for j in i]:
                    board_copy[index][index2] = 0
        draw_shapes(self.left, self.top, screen, board_copy,
                    [self.color1, self.color2, self.color3, self.color4], SIZE_BLOCK)

    def draw_information(self):
        size = int(SIZE_SCREEN[0] // 100 * 2.5)
        font = pygame.font.Font(None, size)
        text = font.render(f"{PHRASES[LANGUAGE]['score']}: {self.score}", True, (232, 229, 62))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = self.left - text_w - SIZE_BLOCK * 3
        text_y = self.top
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (166, 164, 40), (text_x - 10, text_y - 10,
                                                  text_w + 20, text_h + 20), 4)

        text2 = font.render(f"{PHRASES[LANGUAGE]['lines']}: {self.count_lines}", True, (232, 229, 62))
        text_w2 = text2.get_width()
        text_h2 = text2.get_height()
        text_x2 = self.left - text_w2 - SIZE_BLOCK * 3
        text_y2 = self.top + text_h + 50
        screen.blit(text2, (text_x2, text_y2))
        pygame.draw.rect(screen, (166, 164, 40), (text_x2 - 10, text_y2 - 10,
                                                  text_w2 + 20, text_h2 + 20), 4)

        text3 = font.render(f"{PHRASES[LANGUAGE]['level']}: {self.count_levels}", True, (232, 229, 62))
        text_w3 = text3.get_width()
        text_h3 = text3.get_height()
        text_x3 = self.left - text_w3 - SIZE_BLOCK * 3
        text_y3 = self.top + text_h + 100 + text_h2

        screen.blit(text3, (text_x3, text_y3))
        pygame.draw.rect(screen, (166, 164, 40), (text_x3 - 10, text_y3 - 10,
                                                  text_w3 + 20, text_h3 + 20), 4)
        string = f"{PHRASES[LANGUAGE]['complexity']}: {PHRASES[LANGUAGE][f'complexity_{self.level}']}"
        text4 = font.render(string, True, (232, 229, 62))
        text_w4 = text4.get_width()
        text_h4 = text4.get_height()
        text_x4 = self.left - text_w4 - SIZE_BLOCK * 3
        text_y4 = self.top + text_h + 150 + text_h2 + text_h3

        screen.blit(text4, (text_x4, text_y4))
        pygame.draw.rect(screen, (166, 164, 40), (text_x4 - 10, text_y4 - 10,
                                                  text_w4 + 20, text_h4 + 20), 4)

    def draw_field_next_shape(self):
        size = int(SIZE_SCREEN[0] // 100 * 2.5)
        font = pygame.font.Font(None, size)

        text = font.render(PHRASES[LANGUAGE]['next_shape'][0], True, (240, 239, 224))
        text_x = self.left + 12 * SIZE_BLOCK
        text_y = self.top
        screen.blit(text, (text_x, text_y))

        text2 = font.render(PHRASES[LANGUAGE]['next_shape'][1], True, (240, 239, 224))
        text2_h = text2.get_height()
        text2_x = text_x
        text2_y = self.top + text_y
        screen.blit(text2, (text2_x, text2_y))
        pygame.draw.rect(screen, (240, 239, 224),
                         (self.left + 12 * SIZE_BLOCK, text2_y + text2_h + 5, 6 * SIZE_BLOCK, 6 * SIZE_BLOCK), 4)
        x = self.left + 12 * SIZE_BLOCK
        y = text2_y + text2_h + 5
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
        pause_button = Button((x, y), image_pause, image_pause, image_pause2, buttons_main_sprites, self.set_pause,
                              'default_button_click.mp3')

        image_home = load_image('home.png', -1, size=(SIZE_BLOCK * 2, SIZE_BLOCK * 2))
        x = SIZE_SCREEN[0] - image_home.get_width() * 2 - 45
        home_button = Button((x, y), image_home, image_home, image_home, buttons_main_sprites, self.go_to_home,
                             'default_button_click.mp3')
        self.main_game_buttons['pause_button'] = pause_button
        self.main_game_buttons['home_button'] = home_button
        group_buttons.append(GroupButtons([pause_button, home_button]))

    def update_shapes(self, action):
        if self.parent.activity_window is None:
            if self.shape_now.update_move:
                self.shape_now.move(action)
                self.time_update_shape += self.v_level
                if self.time_update_shape >= self.shape_now.v and self.shape_now.update_move:
                    self.time_update_shape = 0
                    self.shape_now.move('down')

            else:
                if SOUND == 'on':
                    sound = pygame.mixer.Sound('../data/music/shape_fall.mp3')
                    sound.play()
                self.update_shape = True
                self.checking_lines()

    def checking_lines(self):
        while True:
            list_indexes = []
            for index, line in enumerate(self.board.board):
                if sum(line) == 10:
                    list_indexes.append(index)

            if list_indexes:
                self.scoring_points(len(list_indexes))
                self.scoring_levels(len(list_indexes))

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

    def scoring_points(self, count_lines):
        if SOUND == 'on':
            sound = pygame.mixer.Sound('../data/music/high_score.mp3')
            sound.set_volume(0.5)
            self.parent.sound_main.set_volume(0.0)
            sound.play()
        if count_lines == 1:
            self.score += 40 * (self.count_levels + 1)
        elif count_lines == 2:
            self.score += 100 * (self.count_levels + 1)
        elif count_lines == 3:
            self.score += 300 * (self.count_levels + 1)
        elif count_lines == 4:
            self.score += 1200 * (self.count_levels + 1)
        if SOUND == 'on':
            self.parent.sound_main.set_volume(0.1)

    def scoring_levels(self, count_lines):
        for i in range(count_lines):
            self.count_lines += 1
            if self.count_lines % 10 == 0:
                self.count_levels += 1

    def set_pause(self):
        if self.activity:
            self.parent.activity_window = self.draw_information_pause
            self.activity = False
            self.parent.button_open_black_screen = self.main_game_buttons['pause_button']
            for name in self.main_game_buttons:
                if self.main_game_buttons[name] != self.parent.button_open_black_screen:
                    if self.main_game_buttons[name].be is False:
                        self.main_game_buttons[name].be = True
                    else:
                        self.main_game_buttons[name].be = False

        else:
            for name in self.main_game_buttons:
                if self.main_game_buttons[name] != self.parent.button_open_black_screen:
                    if self.main_game_buttons[name].be is False:
                        self.main_game_buttons[name].be = True
                    else:
                        self.main_game_buttons[name].be = False
            self.parent.activity_window = None
            self.activity = True
            self.parent.button_open_black_screen = None
            self.main_game_buttons['pause_button'].image = self.main_game_buttons['pause_button'].prev_image

    def go_to_home(self):
        if self.open_home:
            for name in self.main_game_buttons:
                if self.main_game_buttons[name] != self.parent.button_open_black_screen:
                    if self.main_game_buttons[name].be is False:
                        self.main_game_buttons[name].be = True
                    else:
                        self.main_game_buttons[name].be = False
            self.parent.activity_window = None
            self.parent.button_open_black_screen = None
            self.open_home = False
        else:
            self.parent.activity_window = self.draw_information_home
            self.parent.button_open_black_screen = self.main_game_buttons['home_button']
            self.activity = True
            self.open_home = True
            for name in self.main_game_buttons:
                if self.main_game_buttons[name] != self.parent.button_open_black_screen:
                    if self.main_game_buttons[name].be is False:
                        self.main_game_buttons[name].be = True
                    else:
                        self.main_game_buttons[name].be = False
