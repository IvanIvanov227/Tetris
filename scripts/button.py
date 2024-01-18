import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, coord, prev_image, current_image, click_image, group_sprites, action=None, music=None):
        super().__init__(group_sprites)
        if music is not None:
            self.sound = pygame.mixer.Sound(f'../data/music/{music}')
            self.sound.set_volume(1)
        else:
            self.sound = None
        self.be = True
        self.action = action
        self.prev_image = prev_image
        self.current_image = current_image
        self.click_image = click_image
        self.image = prev_image
        self.name_new_image = 'prev'
        self.rect = pygame.Rect(coord[0], coord[1], self.image.get_width(), self.image.get_height())

    def check_do_select(self, up_click, down_click, sound_condition):
        x = self.rect.x
        y = self.rect.y
        w = self.image.get_width()
        h = self.image.get_height()
        if self.be:
            if up_click is not None and down_click is not None and \
                    x <= down_click[0] <= x + w and y <= down_click[1] <= h + y and \
                    not (x <= up_click[0] <= x + w and y <= up_click[1] <= y + h):
                self.image = self.prev_image
                self.name_new_image = 'prev'
            elif up_click is not None and down_click is not None and (
                    x <= down_click[0] <= x + w and
                    y <= down_click[1] <= h + y):
                if self.sound is not None and sound_condition == 'on':
                    self.sound.play()
                self.image = self.click_image
                self.name_new_image = 'click'
                if self.action is not None:
                    self.action()
                return True

            elif down_click is not None and \
                    x <= down_click[0] <= x + w and \
                    y <= down_click[1] <= h + y:
                self.name_new_image = 'current'
                self.image = self.current_image

    def update_image(self):
        if self.name_new_image == 'prev':
            self.image = self.prev_image
        elif self.name_new_image == 'current':
            self.image = self.current_image
        else:
            self.image = self.click_image


class ComboButton(pygame.sprite.Sprite):
    def __init__(self, coord, first_image, second_image, group_sprites, action=None, music=None):
        super().__init__(group_sprites)
        if music is not None:
            self.sound = pygame.mixer.Sound(f'../data/music/{music}')
            self.sound.set_volume(1)
        else:
            self.sound = None
        self.be = True
        self.action = action
        self.prev_image = first_image
        self.second_image = second_image
        self.image = self.prev_image
        self.name_new_image = 'prev'
        self.rect = pygame.Rect(coord[0], coord[1], self.image.get_width(), self.image.get_height())

    def check_do_select(self, up_click, down_click, sound_condition):
        x = self.rect.x
        y = self.rect.y
        w = self.image.get_width()
        h = self.image.get_height()
        if self.be:
            if up_click is not None and down_click is not None and (
                    x <= down_click[0] <= x + w and
                    y <= down_click[1] <= h + y):
                if self.sound is not None and sound_condition == 'on':
                    self.sound.play()
                if self.name_new_image == 'prev':
                    self.image = self.second_image
                    self.name_new_image = 'second'
                else:
                    self.image = self.prev_image
                    self.name_new_image = 'prev'
                if self.action is not None:
                    self.action(self.name_new_image)
                return True

    def update_image(self):
        if self.name_new_image == 'prev':
            self.image = self.prev_image
        else:
            self.image = self.second_image


class GroupButtons:
    def __init__(self, buttons):
        self.buttons = buttons

    def check_do_select_buttons_for_group(self, up_click, down_click, sound_condition):
        current_button = None
        for button in self.buttons:
            result = button.check_do_select(up_click, down_click, sound_condition)
            if result is True:
                current_button = button
                break
            else:
                ...
                # flag = False
                # for b in self.buttons:
                #     if b.image == b.click_image:
                #         flag = True
                #         break
                # if not flag:
                #     button.image = button.click_image
        return current_button
