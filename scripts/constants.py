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

COLORS = (
    (19, 252, 240), (2, 13, 235), (242, 173, 15),
    (243, 250, 4), (26, 250, 4), (155, 4, 250),
    (250, 7, 49), (237, 21, 12), (12, 237, 229),
    (237, 12, 230), (86, 237, 12), (174, 237, 12)
)


START_SHAPES = {
    1: ((1, 1, 1, 1), ),
    2: ((1, 0, 0), (1, 1, 1)),
    3: ((0, 0, 1), (1, 1, 1)),
    4: ((1, 1), (1, 1)),
    5: ((0, 1, 1), (1, 1, 0)),
    6: ((0, 1, 0), (1, 1, 1)),
    7: ((1, 1, 0), (0, 1, 1))
}

PHRASES = {
    'ru': {
        'information_rotate': 'Поворот по часовой стрелке',
        'information_shift_shape': 'Смещение фигуры',
        'accelerating_down_shape': 'Ускорение фигуры вниз',
        'start_button_prev': 'start_russian_prev.png',
        'start_button_click': 'start_russian_click.png',
        'easy_button_prev': 'easy_russian_prev.png',
        'easy_button_click': 'easy_russian_click.png',
        'normal_button_prev': 'normal_russian_prev.png',
        'normal_button_click': 'normal_russian_click.png',
        'hard_button_prev': 'hard_russian_prev.png',
        'hard_button_click': 'hard_russian_click.png',
        'score': 'Счёт',
        'lines': 'Линии',
        'level': 'Уровень',
        'next_shape': ['Следующая', 'фигура'],
        'pause': 'Пауза',
        'pause_information': ["Чтобы продолжить, нажмите на кнопку", "или нажмите Escape"],
        'home_information': ["Чтобы вернуться домой,", "нажмите на кнопку Q"],
        'finish_information': ["Вы проиграли.", "Нажмите на Enter,", "чтобы выйти"],
        'complexity_easy': 'Легко',
        'complexity_normal': 'Нормально',
        'complexity_hard': 'Трудно',
        'complexity': 'Сложность'
    },
    'eng': {
        'information_rotate': 'Clockwise rotation',
        'information_shift_shape': 'Shifting the shape',
        'accelerating_down_shape': 'Accelerating the figure downwards',
        'start_button_prev': 'start_english_prev.png',
        'start_button_click': 'start_english_click.png',
        'easy_button_prev': 'easy_english_prev.png',
        'easy_button_click': 'easy_english_click.png',
        'normal_button_prev': 'normal_english_prev.png',
        'normal_button_click': 'normal_english_click.png',
        'hard_button_prev': 'hard_english_prev.png',
        'hard_button_click': 'hard_english_click.png',
        'score': 'Score',
        'lines': 'Lines',
        'level': 'Level',
        'next_shape': ['Next', 'shape'],
        'pause': 'Pause',
        'pause_information': ["To continue, click on the button", "or press Escape"],
        'home_information': ["To return home,", "click on the Q button"],
        'finish_information': ["You've lost.", "Press Enter,", "to get out"],
        'complexity_easy': 'Easy',
        'complexity_normal': 'Normal',
        'complexity_hard': 'Hard',
        'complexity': 'Complexity'
    }

}
