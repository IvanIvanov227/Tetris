import pygame
import random


class Tetris:
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.list_snow = []
        self.fps = 60
        self.time_draw_snow = 0

    def start_game(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill('black')
            # Рисование снежинок
            self.draw_snow()
            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()

    def draw_snow(self):
        self.time_draw_snow += 0.01
        if self.time_draw_snow >= 1:
            self.time_draw_snow = 0
            self.list_snow.append([random.random() * self.size[0], self.size[1],
                                   random.randint(15, 30), random.randint(2, 4)])
        for index, snow in enumerate(self.list_snow):
            self.list_snow[index][1] -= snow[2] / self.fps
            snow = self.list_snow[index]
            pygame.draw.rect(self.screen, 'white', (snow[0], snow[1], snow[3], snow[3]))
