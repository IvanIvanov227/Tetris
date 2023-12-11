import os
import pygame
from scripts.main_window import Tetris

if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Тетрис')
    fullname = os.path.join('data', 'icon.png')
    image = pygame.image.load(fullname)
    pygame.display.set_icon(image)
    screensize = pygame.display.list_modes()
    size = width, height = screensize[1][0], screensize[1][1]
    screen = pygame.display.set_mode(size)
    game = Tetris(screen)
    game.start_game()
