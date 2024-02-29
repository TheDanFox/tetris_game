import pygame
import sys
import random
import time
from pygame.locals import *


#константы
move_side = 0.15
move_down = 0.1

fps = 25
width, height = 600, 500
block = 20
field_h = 20
field_w = 10

side = int((width - field_w * block) / 2)
top_margin = height - (field_h * block) - 5

colors = ((pygame.Color("blue")), (pygame.Color("green")), (pygame.Color("red")), (pygame.Color("yellow")))

white, gray, black = (255, 255, 255), (185, 185, 185), (0, 0, 0)


fig_w, fig_h = 5, 5
empty = 'o'


figures = {'Z': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'oxooo',
                  'ooooo']],
            'S': [['ooooo',
                  'ooooo',
                  'ooxxo',
                  'oxxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'oooxo',
                  'ooooo']],
           'J': [['ooooo',
                  'oxooo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxxo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oooxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'oxxoo',
                  'ooooo']],
           'L': [['ooooo',
                  'oooxo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oxooo',
                  'ooooo'],
                 ['ooooo',
                  'oxxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo']],
           'I': [['ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'xxxxo',
                  'ooooo',
                  'ooooo']],
           'T': [['ooooo',
                  'ooxoo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'ooxoo',
                  'ooooo']],
           'O': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'oxxoo',
                  'ooooo']],
           }

#выводит информацию и название игры
def text_to_show(text):
    title_s, title_r = txt_objects(text, big_font, (pygame.Color("white")))
    title_r.center = (int(width / 2) - 3, int(width / 2) - 3)
    screen.blit(title_s, title_r)

    presskey_s, presskey_r = txt_objects('Нажмите любую клавишу, чтобы продолжить', basic_font,
                                            (pygame.Color("white")))
    presskey_r.center = (int(width / 2), int(width / 2) + 100)
    screen.blit(presskey_s, presskey_r)
    while check_keys() is None:
        pygame.display.update()
        clock.tick()


def txt_objects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def check_keys():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        pygame.event.post(event)
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None



#генерируется следующая фигура
def new_figure():
    shape = random.choice(list(figures.keys()))
    newFigure = {'shape': shape,
                 'rotation': random.randint(0, len(figures[shape]) - 1),
                 'x': int(field_w / 2) - int(fig_w / 2),
                 'y': -2,
                 'color': random.randint(0, len(colors) - 1)}
    return newFigure


#добавление фигур в поле
def add_to_field(field, fig):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                field[x + fig['x']][y + fig['y']] = fig['color']


#создание пустого поля
def empty_field():
    field = []
    for i in range(field_w):
        field.append([empty] * field_h)
    return field


def in_field(x, y):
    return x >= 0 and x < field_w and y < field_h


#следит за тем, чтобы фигура не выходила из поля, а также не накладывалась на другую
def check_position(field, fig, _x=0, _y=0):
    for x in range(fig_w):
        for y in range(fig_h):
            above_field = y + fig['y'] + _y < 0
            if above_field or figures[fig['shape']][fig['rotation']][y][x] == empty:
                continue
            if not in_field(x + fig['x'] + _x, y + fig['y'] + _y):
                return False
            if field[x + fig['x'] + _x][y + fig['y'] + _y] != empty:
                return False
    return True


#обнаруживает ряд
def complete_line(field, y):
    for x in range(field_w):
        if field[x][y] == empty:
            return False
    return True


#удаляет ряд
def clear_line(field):
    removed_lines = 0
    y = field_h - 1
    while y >= 0:
        if complete_line(field, y):
            for pushDownY in range(y, 0, -1):
                for x in range(field_w):
                    field[x][pushDownY] = field[x][pushDownY - 1]
            for x in range(field_w
                           ):
                field[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines


def coords(block_x, block_y):
    return (side + (block_x * block)), (top_margin + (block_y * block))


#рисует блоки
def draw_block(block_x, block_y, color, pixel_x=None, pixel_y=None):
    if color == empty:
        return
    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = coords(block_x, block_y)
    pygame.draw.rect(screen, colors[color], (pixel_x + 1, pixel_y + 1, block - 1,
                                             block - 1), 0, 3)


#игровое поле
def game_field(field):
    pygame.draw.rect(screen, pygame.Color("white"), (side - 4, top_margin - 4, (field_w * block) + 8,
                                                     (field_h * block) + 8),5)

    pygame.draw.rect(screen, pygame.Color("black"), (side, top_margin, block * field_w, block * field_h))
    for x in range(field_w):
        for y in range(field_h):
            draw_block(x, y, field[x][y])


def title():
    title_s = big_font.render('Игра Тетрис', True, (pygame.Color("white")))
    title_r = title_s.get_rect()
    title_r.topleft = (width - 425, 30)
    screen.blit(title_s, title_r)


#выводит текст - баллы, пауза, выход, на экране игры
def info(points):
    points_s = basic_font.render(f'Баллы: {points}', True, pygame.Color("white"))
    points_r = points_s.get_rect()
    points_r.topleft = (width - 550, 180)
    screen.blit(points_s, points_r)

    pauseb_s = basic_font.render('Пауза: пробел', True, pygame.Color("white"))
    pauseb_r = pauseb_s.get_rect()
    pauseb_r.topleft = (width - 550, 420)
    screen.blit(pauseb_s, pauseb_r)

    escb_s = basic_font.render('Выход: Esc', True, pygame.Color("white"))
    escb_r = escb_s.get_rect()
    escb_r.topleft = (width - 550, 450)
    screen.blit(escb_s, escb_r)


#рисует фигуры
def draw_figure(fig, pixelx=None, pixely=None):
    figure_draw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = coords(fig['x'], fig['y'])
    for x in range(fig_w):
        for y in range(fig_h):
            if figure_draw[y][x] != empty:
                draw_block(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))


def next_figure(figure):
    next_s = basic_font.render('Следующая Фигура:', True, pygame.Color("white"))
    next_r = next_s.get_rect()
    next_r.topleft = (width - 175, 180)
    screen.blit(next_s, next_r)
    draw_figure(figure, pixelx=width - 125, pixely=230)


def main():
    global clock, screen, basic_font, big_font
    pygame.display.set_icon(pygame.image.load("icon.png"))
    field = empty_field()
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    down = False
    right = False
    left = False
    points = 0
    fall_speed = 0.25
    falling_figure = new_figure()
    next_fig = new_figure()
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    basic_font = pygame.font.SysFont('arial', 20)
    big_font = pygame.font.SysFont('verdana', 45)
    pygame.display.set_caption('Тетрис')
    text_to_show('Тетрис')
    while True:
        if falling_figure == None:
        #генерирует новую падающую фигуру
            falling_figure = next_fig
            next_fig = new_figure()
            last_fall = time.time()
            if not check_position(field, falling_figure):
                return
            #если нет свободного места - игра заканчивается
        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                #выход из игры
            pygame.event.post(event)
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pause = pygame.Surface((600, 500), pygame.Color("blue"))
                    pause.fill((0, 0, 255, 127))
                    screen.blit(pause, (0, 0))
                    text_to_show('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                    #остановка игры
                elif event.key == K_RIGHT:
                    right = False
                elif event.key == K_LEFT:
                    left = False
                elif event.key == K_DOWN:
                    down = False
            elif event.type == KEYDOWN:
                #перемещение вправо и влево
                if event.key == K_RIGHT and check_position(field, falling_figure, _x=1):
                    falling_figure['x'] += 1
                    right = True
                    left = False
                    last_side_move = time.time()
                elif event.key == K_LEFT and check_position(field, falling_figure, _x=-1):
                    falling_figure['x'] -= 1
                    left = True
                    right = False
                    last_side_move = time.time()
                #поворот фигуры
                elif event.key == K_UP:
                    falling_figure['rotation'] = ((falling_figure['rotation'] + 1) %
                                                  len(figures[falling_figure['shape']]))
                    if not check_position(field, falling_figure):
                        falling_figure['rotation'] = ((falling_figure['rotation'] - 1) %
                                                      len(figures[falling_figure['shape']]))
                #ускорение фигуры, нажатием вниз
                elif event.key == K_DOWN:
                    down = True
                    if check_position(field, falling_figure, _y=1):
                        falling_figure['y'] += 1
                    last_move_down = time.time()
        if (left or right) and time.time() - last_side_move > move_side:
            if left and check_position(field, falling_figure, _x=-1):
                falling_figure['x'] -= 1
            elif right and check_position(field, falling_figure, _x=1):
                falling_figure['x'] += 1
            last_side_move = time.time()
        if down and time.time() - last_move_down > move_down and check_position(field, falling_figure, _y=1):
            falling_figure['y'] += 1
            last_move_down = time.time()
        if time.time() - last_fall > fall_speed:
            if not check_position(field, falling_figure, _y=1):
                add_to_field(field, falling_figure)
                points += clear_line(field)
                fall_speed = 0.25
                falling_figure = None
            else:
                falling_figure['y'] += 1
                last_fall = time.time()
        screen.fill(pygame.Color("black"))
        title()
        game_field(field)
        info(points)
        next_figure(next_fig)
        if falling_figure != None:
            draw_figure(falling_figure)
        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()