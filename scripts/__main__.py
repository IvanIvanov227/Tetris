import pygame
from main_game import Tetris

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    game = Tetris()
    game.start_game()
