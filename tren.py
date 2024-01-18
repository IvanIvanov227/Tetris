
TYPES_OF_SHAPES = {
    1: {
        1: ((0, 0, 0, 0), (1, 1, 1, 1), (0, 0, 0, 0), (0, 0, 0, 0)),
        2: ((0, 0, 1, 0), (0, 0, 1, 0), (0, 0, 1, 0), (0, 0, 1, 0)),
        3: ((0, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1), (0, 0, 0, 0)),
        4: ((0, 1, 0, 0), (0, 1, 0, 0), (0, 1, 0, 0), (0, 1, 0, 0))
    },
    2: {
        1: ((1, 0, 0), (1, 1, 1), (0, 0, 0)),
        2: ((0, 1, 1), (0, 1, 0), (0, 1, 0)),
        3: ((0, 0, 0), (1, 1, 1), (0, 0, 1)),
        4: ((0, 1, 0), (0, 1, 0), (1, 1, 0))
    },
    3: {
        1: ((0, 0, 1), (1, 1, 1), (0, 0, 0)),
        2: ((0, 1, 0), (0, 1, 0), (0, 1, 1)),
        3: ((0, 0, 0), (1, 1, 1), (1, 0, 0)),
        4: ((1, 1, 0), (0, 1, 0), (0, 1, 0))
    },
    4: {
        1: ((0, 1, 1, 0), (0, 1, 1, 0), (0, 0, 0, 0)),
        2: ((0, 1, 1, 0), (0, 1, 1, 0), (0, 0, 0, 0)),
        3: ((0, 1, 1, 0), (0, 1, 1, 0), (0, 0, 0, 0)),
        4: ((0, 1, 1, 0), (0, 1, 1, 0), (0, 0, 0, 0))
    },
    5: {
        1: ((0, 1, 1), (1, 1, 0), (0, 0, 0)),
        2: ((0, 1, 0), (0, 1, 1), (0, 0, 1)),
        3: ((0, 0, 0), (0, 1, 1), (1, 1, 0)),
        4: ((1, 0, 0), (1, 1, 0), (0, 1, 0))
    },
    6: {
        1: ((0, 1, 0), (1, 1, 1), (0, 0, 0)),
        2: ((0, 1, 0), (0, 1, 1), (0, 1, 0)),
        3: ((0, 0, 0), (1, 1, 1), (0, 1, 0)),
        4: ((0, 1, 0), (1, 1, 0), (0, 1, 0))
    },
    7: {
        1: ((1, 1, 0), (0, 1, 1), (0, 0, 0)),
        2: ((0, 0, 1), (0, 1, 1), (0, 1, 0)),
        3: ((0, 0, 0), (1, 1, 0), (0, 1, 1)),
        4: ((0, 1, 0), (1, 1, 0), (1, 0, 0))
    }
}


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
    for coord in self.coords[-1]:
        if coord[1] == 19 or self.board.board[coord[1] + 1][coord[0]]:
            return False
    return True


# def delete_cubes(self, list_indexes):
#     count_delete = 0
#     first_delete_index = None
#     start_position_delete = None
#     if self.coordinates is None:
#         self.coordinates = list(TYPES_OF_SHAPES[self.form][self.rotate])
#     # Удаляем координаты, если удаленные строки в фигуре
#     index = 0
#     n = len(self.coords)
#     while index < n:
#         coord_line = self.coords[index]
#         if coord_line[0][1] in list_indexes:
#             count_delete += 1
#             if first_delete_index is None:
#                 first_delete_index = coord_line[0][1]
#             if start_position_delete is None:
#                 start_position_delete = index
#             n -= 1
#             del self.coords[index]
#         else:
#             index += 1
#
#     if len(self.coords) == 0:
#         self.kill()
#         return
#     # if self.coords[-1][0][1] < list_indexes[0]:
#     #     for index, coord_line in enumerate(self.coords):
#     #         for index2, coord in enumerate(coord_line):
#     #             self.coords[index][index2][1] += len(list_indexes)
#     #     self.rect.y += SIZE_BLOCK * len(list_indexes)
#     # if start_position_delete is None or first_delete_index is None:
#     #     return
#     # Если фигура выше или ниже удаленных строк
#     if start_position_delete is None or first_delete_index is None:
#         if self.coords[-1][0][1] < list_indexes[0]:
#             for index, coord_line in enumerate(self.coords):
#                 for index2, coord in enumerate(coord_line):
#                     self.coords[index][index2][1] += len(list_indexes)
#             self.rect.y += SIZE_BLOCK * len(list_indexes)
#         return
#
#     # Если удаленная строка находится в фигуре
#     for index, coord_line in enumerate(self.coords):
#         if coord_line[0][1] < first_delete_index:
#             for index2 in range(len(self.coords[index])):
#                 self.coords[index][index2][1] += count_delete
#
#     # Дело в лишнем смещении координат. В self.coords не удаляй строки а заменяй дефолтными, чтобы self.coordinates не смещать лишнее!!!
#     for i in range(count_delete):
#         self.coordinates[i + start_position_delete] = tuple((i - i for i in range(len(self.coordinates[0]))))
#
#     for i in range(start_position_delete, 0, -1):
#         self.coordinates[i] = self.coordinates[i - 1]
#         self.coordinates[i - 1] = tuple((i - i for i in range(len(self.coordinates[0]))))
#
#     width_image = len(TYPES_OF_SHAPES[self.form][self.rotate][0]) * SIZE_BLOCK
#     height_image = len(TYPES_OF_SHAPES[self.form][self.rotate]) * SIZE_BLOCK
#     self.image = pygame.Surface((width_image, height_image), pygame.SRCALPHA)
#     self.draw(0, 0, self.image, self.coordinates)







    # def delete_cubes(self, list_indexes_delete):
    #     count_delete = 0
    #     # индекс и позиция первой удалённой линии в фигуре
    #     first_delete_index = None
    #     start_position_delete = None
    #     if self.coordinates is None:
    #         self.coordinates = list(TYPES_OF_SHAPES[self.form][self.rotate])
    #
    #     count = 0
    #     while sum(self.coordinates[0]) == 0:
    #         count += 1
    #         del self.coordinates[0]
    #
    #     # Смещение фигуры на столько линий, сколько их удалено вне её снизу.
    #     list_indexes_without_shape = [index for index in list_indexes_delete if index > self.coords[-1][0][1]]
    #     count_delete_without_shape = len(list_indexes_without_shape)
    #     self.rect.y += SIZE_BLOCK * count_delete_without_shape
    #
    #     # OK ТУТ ВСЁ
    #     # удаляем координаты, если удаленные строки в фигуре
    #     index = 0
    #     n = len(self.coords)
    #     last_delete_index = None
    #     while index < n:
    #         coord_line = self.coords[index]
    #         if coord_line[0][1] in list_indexes_delete:
    #             last_delete_index = coord_line[0][1]
    #             count_delete += 1
    #             if first_delete_index is None:
    #                 first_delete_index = coord_line[0][1]
    #             if start_position_delete is None:
    #                 start_position_delete = index
    #             n -= 1
    #             del self.coords[index]
    #         else:
    #             index += 1
    #
    #     # Если больше нет координат, то удаляем фигуру
    #     if len(self.coords) == 0:
    #         self.kill()
    #         return
    #
    #     # if last_delete_index != self.coords[-1][0][1] and self.coords[-1][0][1] + count_delete > list_indexes_delete[0]:
    #     #     self.rect.y += SIZE_BLOCK * count_delete
    #
    #     # Если фигура выше или ниже удаленных строк
    #     if start_position_delete is None or first_delete_index is None:
    #         for index, coord_line in enumerate(self.coords):
    #             for index2, coord in enumerate(coord_line):
    #                 self.coords[index][index2][1] += count_delete_without_shape
    #         return
    #
    #     # Если удалённая строка находится в фигуре
    #     index_finish = None
    #     for index, coord_line in enumerate(self.coords):
    #         if coord_line[0][1] >= first_delete_index or index == len(self.coords) - 1:
    #             index_finish = index
    #             break
    #     for index in range(index_finish):
    #         for index2 in range(len(self.coords[index])):
    #             self.coords[index][index2][1] += count_delete
    #
    #     for index, coord_line in enumerate(self.coords):
    #         for index2, coord in enumerate(coord_line):
    #             self.coords[index][index2][1] += count_delete_without_shape
    #
    #     for i in range(count_delete):
    #         self.coordinates[i + start_position_delete] = tuple((i - i for i in range(len(self.coordinates[0]))))
    #
    #     for i in range(start_position_delete, count_delete - 1, -1):
    #         self.coordinates[i] = self.coordinates[i - count_delete]
    #         self.coordinates[i - count_delete] = tuple((i - i for i in range(len(self.coordinates[0]))))
    #
    #     width_image = len(self.coordinates[0]) * SIZE_BLOCK
    #     height_image = len(self.coordinates) * SIZE_BLOCK
    #     self.image = pygame.Surface((width_image, height_image), pygame.SRCALPHA)
    #     self.draw(0, count * SIZE_BLOCK, self.image, self.coordinates)
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

color = (255, 255, 255)
rect = pygame.Rect(150, 100, 100, 100)
is_visible = True
last_toggle_time = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    current_time = pygame.time.get_ticks()
    if current_time - last_toggle_time > 500:  # меняем цвет каждые 500 миллисекунд
        is_visible = not is_visible
        last_toggle_time = current_time

    screen.fill((0, 0, 0))  # очищаем экран
    if is_visible:
        pygame.draw.rect(screen, color, rect)  # рисуем объект, если он видимый

    pygame.display.flip()
    clock.tick(60)