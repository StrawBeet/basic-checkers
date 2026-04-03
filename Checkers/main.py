import pygame

pygame.init()
screen = pygame.display.set_mode((1080, 864))
clock = pygame.time.Clock()
running = True
menu = True
game_active = False
bot = False
settings = False

mouse_pos = pygame.mouse.get_pos()

brown = (54, 35, 18)
beige = (247, 232, 208)
dark_green = (25, 120, 12)

font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 100)

local_mult_surf = pygame.Surface((360, 216))
local_mult_rect = local_mult_surf.get_rect(center = (screen.get_rect().centerx, 282))
local_mult_text = font.render("Play Against a Friend", True, 'white')
local_mult_text_rect = local_mult_text.get_rect(center = local_mult_rect.center)

bot_surf = pygame.Surface((360, 216))
bot_rect = bot_surf.get_rect(center = (screen.get_rect().centerx, 576))
bot_text = font.render("Play Against a Bot", True, 'white')
bot_text_rect = bot_text.get_rect(center = bot_rect.center)
bot_surf.fill('black')

title_text = title_font.render("Checkers", True, 'black')
title_rect = title_text.get_rect(center = (screen.get_rect().centerx, 100))

white_rects = []
black_rects = []

for i in range(8):
    if i % 2 == 0:
        white_rects.append(pygame.Rect(140, 32 + 100 * i, 100, 100))
        black_rects.append(pygame.Rect(240, 32 + 100 * i, 100, 100))
        white_rects.append(pygame.Rect(340, 32 + 100 * i, 100, 100))
        black_rects.append(pygame.Rect(440, 32 + 100 * i, 100, 100))
        white_rects.append(pygame.Rect(540, 32 + 100 * i, 100, 100))
        black_rects.append(pygame.Rect(640, 32 + 100 * i, 100, 100))
        white_rects.append(pygame.Rect(740, 32 + 100 * i, 100, 100))
        black_rects.append(pygame.Rect(840, 32 + 100 * i, 100, 100))
    else:
        black_rects.append(pygame.Rect(140, 32 + 100 * i, 100, 100))
        white_rects.append(pygame.Rect(240, 32 + 100 * i, 100, 100))
        black_rects.append(pygame.Rect(340, 32 + 100 * i, 100, 100))
        white_rects.append(pygame.Rect(440, 32 + 100 * i, 100, 100))
        black_rects.append(pygame.Rect(540, 32 + 100 * i, 100, 100))
        white_rects.append(pygame.Rect(640, 32 + 100 * i, 100, 100))
        black_rects.append(pygame.Rect(740, 32 + 100 * i, 100, 100))
        white_rects.append(pygame.Rect(840, 32 + 100 * i, 100, 100))

def check_moves(i, class2, first):
    legal_moves = []

    if first:
        reverse = 0
    else:
        reverse = -1

    sign = 1 + 2 * reverse

    if (i // 4) % 2 == 0 - 3 * reverse:
        if i % 4 == 0:
            if class2.board[i + sign * 4] == 0:
                legal_moves += [i + sign * 4]
            else:
                pass
        else:
            legal_moves += [i + sign * (3 + k) for k in [0, 1] if class2.board[i + sign * (3 + k)] == 0]
    else:
        if i % 4 == 3 + 3 * reverse:
            if class2.board[i + sign * 4] == 0:
                legal_moves += [i + sign * 4]
            else:
                pass
        else:
            legal_moves += [i + sign * (4 + k) for k in [0, 1] if class2.board[i + sign * (4 + k)] == 0]

    return legal_moves


def check_captures(i, self, class2):
    legal_captures = []

    if self.first:
        reverse = 0
    else:
        reverse = -1

    sign = 1 + 2 * reverse
    if (i // 4) % 2 == 0 - 3 * reverse:
        if i % 4 == 0:
            if class2.board[i + sign * 4] == 1 and class2.board[i + sign * 9] == 0:
                legal_captures.append(i + sign * 4)
            else:
                pass
        else:
            tested = [i + sign * (3 + k / 2) for k in [0, 2] if
                                 class2.board[i + sign * (3 + k / 2)] == 1 and class2.board[i + sign * (7 + k)] == 0]
            for k in tested:
                legal_captures += k
    else:
        if i % 4 == 3 + 3 * reverse:
            if class2.board[i + sign * 4] == 1 and class2.board[i + sign * 9] == 0:
                legal_captures.append(i + sign * 4)
            else:
                pass
        else:
            tested = [i + sign * (4 + k / 2) for k in [0, 2] if
                                 class2.board[i + sign * (4 + k / 2)] == 1 and class2.board[i + sign * (7 + k)] == 0]
            for k in tested:
                legal_captures += k

    return legal_captures

class Checkers:
    def __init__(self, board, first):
        self.board = board
        self.first = first


    def legal_moves(self, class2):
        legal_moves = {}


        for i in [k for k in self.board if self.board[k] != 0]:
            legal_moves[i] = check_moves(i, class2, self.first)

        return legal_moves

    def captures(self, class2):
        legal_captures = {}

        for i in [k for k in self.board if self.board[k] != 0 and len(self.legal_moves(class2[k])) < 2]:
            legal_captures[i] = check_captures(i, self, class2)

        return legal_captures

white_board = {}
for i in range(32):
    if i < 12:
        white_board[i] = 1
    else:
        white_board[i] = 0
whiteCheckers = Checkers(white_board, True)

black_board = {}
for i in range(32):
    if i < 12:
        black_board[31 - i] = 1
    else:
        black_board[31 - i] = 0
blackCheckers = Checkers(black_board, False)

def draw_pieces(white, black):
    for i in [i for i in white if white[i] == 1]:
        pygame.draw.circle(screen, (255, 255, 255), (190 + 200 * (i % 4) + 100 * ((i // 4) % 2),782 - 100 * (i // 4)), 40)

    for i in [i for i in black if black[i] == 1]:
        pygame.draw.circle(screen, 'Black', (190 + 200 * (i % 4) + 100 * ((i // 4) % 2), 782 - 100 * (i // 4)), 40)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

    screen.fill(dark_green)
    if menu:
        if pygame.mouse.get_pressed()[0]:
            if local_mult_rect.collidepoint(mouse_pos):
                menu = False
                game_active = True
                bot = False
            elif bot_rect.collidepoint(mouse_pos):
                menu = False
                game_active = True
                bot = True

        screen.blit(local_mult_surf, local_mult_rect)
        screen.blit(local_mult_text, local_mult_text_rect)
        screen.blit(bot_surf, bot_rect)
        screen.blit(bot_text, bot_text_rect)
        screen.blit(title_text, title_rect)
    else:
        if game_active:
            for i in range(32):
                pygame.draw.rect(screen, beige, white_rects[i])
                pygame.draw.rect(screen, brown, black_rects[i])

            draw_pieces(whiteCheckers.board, blackCheckers.board)
            if not bot:
                pass
            else:
                pass
        else:
            print("Unexpected game state")
            running = False

    pygame.display.flip()
    clock.tick(60)


pygame.quit()