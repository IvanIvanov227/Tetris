import pygame


class Board:
    # создание поля
    def __init__(self, count_width, count_height, left, top, cell_size):
        self.width = count_width
        self.height = count_height
        self.board = [[j - j for j in range(10 + i - i)] for i in range(20)]
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        x, y = 0, 0
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (181, 178, 5),
                                 (self.left + x, self.top + y, self.cell_size, self.cell_size), 1)

                x += self.cell_size
            y += self.cell_size
            x = 0
