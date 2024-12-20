import pygame
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300 
PLAY_HEIGHT = 600
BLOCK_SIZE = 30

TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    rows = 20  
    columns = 10  

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))


def draw_grid(surface, row, col):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y
    for i in range(row):
        pygame.draw.line(surface, GRAY, (sx, sy+ i*30), (sx + PLAY_WIDTH, sy + i * 30)) 
        for j in range(col):
            pygame.draw.line(surface, GRAY, (sx + j * 30, sy), (sx + j * 30, sy + PLAY_HEIGHT)) 


def clear_rows(grid, locked, score):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
            score += 10
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return score


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, WHITE)

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy- 30))


def draw_window(surface, score):
    surface.fill(BLACK)
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, WHITE)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j* 30, TOP_LEFT_Y + i * 30, 30, 30), 0)

    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, WHITE, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)


    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}',1,WHITE)
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    surface.blit(label,(sx+10,sy-70))



def main():
    global grid
    score = 0
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    last_fall_time = time.time()
    fall_speed = 0.27
    holding_down = False


    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if time.time() - last_fall_time >= fall_speed:
            last_fall_time = time.time()
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                if event.key == pygame.K_DOWN:
                    holding_down = True

                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece,grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    holding_down = False


        if holding_down:
            fall_speed = 0.08
            if time.time() - last_fall_time >= fall_speed:
                last_fall_time = time.time()
                current_piece.y += 1
                if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True
        else:
            fall_speed = 0.27


        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score = clear_rows(grid, locked_positions, score)


        draw_window(win, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, WHITE, win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    pygame.font.init()
    run = True
    while run:
        win.fill(BLACK)
        draw_text_middle('Press any key to begin.', 60, WHITE, win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
                run = False
    pygame.font.quit()
    pygame.quit()


pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
main_menu()
