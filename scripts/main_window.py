import pygame


class Tetris:
    def __init__(self, screen):
        self.screen = screen

    def start_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
        pygame.quit()
