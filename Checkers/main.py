import pygame

pygame.init()
screen = pygame.display.set_mode((1080, 864))
clock = pygame.time.Clock()
running = True
menu = True
game_active = False
bot = False
settings = False
turn = 0
turn_end = False

capturing = False
capture_possible = False
captured = False
previous_chosen = -1
being_moved = 0
capture = []
previous_moves = []
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
        black_rects.append(pygame.Rect(140, 732 - 100 * i, 100, 100))
        white_rects.append(pygame.Rect(240, 732 - 100 * i, 100, 100))
        black_rects.append(pygame.Rect(340, 732 - 100 * i, 100, 100))
        white_rects.append(pygame.Rect(440, 732 - 100 * i, 100, 100))
        black_rects.append(pygame.Rect(540, 732 - 100 * i, 100, 100))
        white_rects.append(pygame.Rect(640, 732 - 100 * i, 100, 100))
        black_rects.append(pygame.Rect(740, 732 - 100 * i, 100, 100))
        white_rects.append(pygame.Rect(840, 732 - 100 * i, 100, 100))
    else:
        white_rects.append(pygame.Rect(140, 732 - 100 * i, 100, 100))
        black_rects.append(pygame.Rect(240, 732 - 100 * i, 100, 100))
        white_rects.append(pygame.Rect(340, 732 - 100 * i, 100, 100))
        black_rects.append(pygame.Rect(440, 732 - 100 * i, 100, 100))
        white_rects.append(pygame.Rect(540, 732 - 100 * i, 100, 100))
        black_rects.append(pygame.Rect(640, 732 - 100 * i, 100, 100))
        white_rects.append(pygame.Rect(740, 732 - 100 * i, 100, 100))
        black_rects.append(pygame.Rect(840, 732 - 100 * i, 100, 100))

def check_moves(i, class1, class2, first):
    # Returns all the legal moves for whichever piece is at i without including captures
    legal_moves = []

    if first:
        if i[0] - 1 < 0:
            if class1.board[(i[0] + 1, i[1] + 1)] != 1 and class2.board[(i[0] + 1, i[1] + 1)] != 1:
                legal_moves += [(i[0] + 1, i[1] + 1)]
            else:
                pass
        elif i[0] + 1 > 7:
            if class1.board[(i[0] - 1, i[1] + 1)] != 1 and class2.board[(i[0] - 1, i[1] + 1)] != 1:
                legal_moves += [(i[0] - 1, i[1] + 1)]
        else:
            if class1.board[(i[0] - 1, i[1] + 1)] != 1 and class2.board[(i[0] - 1, i[1] + 1)] != 1:
                legal_moves += [(i[0] - 1, i[1] + 1)]

            if class1.board[(i[0] + 1, i[1] + 1)] != 1 and class2.board[(i[0] + 1, i[1] + 1)] != 1:
                legal_moves += [(i[0] + 1, i[1] + 1)]
    else:
        if i[0] - 1 < 0:
            if class1.board[(i[0] + 1, i[1] - 1)] != 1 and class2.board[(i[0] + 1, i[1] - 1)] != 1:
                legal_moves += [(i[0] + 1, i[1] - 1)]
            else:
                pass
        elif i[0] + 1 > 7:
            if class1.board[(i[0] - 1, i[1] - 1)] != 1 and class2.board[(i[0] - 1, i[1] - 1)] != 1:
                legal_moves += [(i[0] - 1, i[1] - 1)]
            else:
                pass
        else:
            if class1.board[(i[0] - 1, i[1] - 1)] != 1 and class2.board[(i[0] - 1, i[1] - 1)] != 1:
                legal_moves += [(i[0] - 1, i[1] - 1)]

            if class1.board[(i[0] + 1, i[1] - 1)] != 1 and class2.board[(i[0] + 1, i[1] - 1)] != 1:
                legal_moves += [(i[0] + 1, i[1] - 1)]


    return legal_moves

def check_captures(i, self, class2):
    # Returns all legal captures for whichever piece is at i
    legal_captures = []
    print("Checking captures")
    if self.first:
        if i[0] < 2:
            legal_captures += check_capture2(i, self, class2)
            if len(check_capture2(i, self, class2)) > 0:
                legal_captures += check_captures((i[0] + 2, i[1] + 2), self, class2)
        elif i[0] > 5:
            legal_captures += check_capture1(i, self, class2)
            if len(check_capture1(i, self, class2)) > 0:
                legal_captures += check_captures((i[0] - 2, i[1] + 2), self, class2)
        else:
            legal_captures += check_capture1(i, self, class2)
            if len(check_capture1(i, self, class2)):
                legal_captures += check_captures((i[0] - 2, i[1] + 2), self, class2)

            legal_captures += check_capture2(i, self, class2)
            if len(check_capture2(i, self, class2)):
                legal_captures += check_captures((i[0] + 2, i[1] + 2), self, class2)
    else:
        if i[0] < 2:
            legal_captures += check_capture4(i, self, class2)
            if len(check_capture4(i, self, class2)) > 0:
                legal_captures += check_captures((i[0] + 2, i[1] - 2), self, class2)
        elif i[0] > 5:
            legal_captures += check_capture3(i, self, class2)
            if len(check_capture3(i, self, class2)) > 0:
                legal_captures += check_captures((i[0] - 2, i[1] - 2), self, class2)
        else:
            legal_captures += check_capture3(i, self, class2)
            if len(check_capture3(i, self, class2)) > 0:
                legal_captures += check_captures((i[0] - 2, i[1] - 2), self, class2)

            legal_captures += check_capture4(i, self, class2)
            if len(check_capture4(i, self, class2)) > 0:
                legal_captures += check_captures((i[0] + 2, i[1] - 2), self, class2)

    return legal_captures

def check_capture1(i, self, class2):
    # This checks whether the piece can take to the top left
    if i[1] < 6:
        if class2.board[(i[0] - 1, i[1] + 1)] == 1:
            if self.board[(i[0] - 2, i[1] + 2)] == 0 and class2.board[(i[0] - 2, i[1] + 2)] == 0:
                return [((i[0] - 1, i[1] + 1), (i[0] - 2, i[1] + 2))]

    return []

def check_capture2(i, self, class2):
    # This checks whether the piece can take to the top right
    if i[1] < 6:
        if class2.board[(i[0] + 1, i[1] + 1)] == 1:
            if self.board[(i[0] + 2, i[1] + 2)] == 0 and class2.board[(i[0] + 2, i[1] + 2)] == 0:
                return [((i[0] + 1, i[1] + 1), (i[0] + 2, i[1] + 2))]

    return []

def check_capture3(i, self, class2):
    # This checks whether the piece can take to the bottom left
    if i[1] > 1:
        if class2.board[(i[0] - 1, i[1] - 1)] == 1:
            if self.board[(i[0] - 2, i[1] - 2)] == 0 and class2.board[(i[0] - 2, i[1] - 2)] == 0:
                return [((i[0] - 1, i[1] - 1), (i[0] - 2, i[1] - 2))]

    return []

def check_capture4(i, self, class2):
    # This checks whether the piece can take to the bottom right
    if i[1] > 1:
        if class2.board[(i[0] + 1, i[1] - 1)] == 1:
            if self.board[(i[0] + 2, i[1] - 2)] == 0 and class2.board[(i[0] + 2, i[1] - 2)] == 0:
                return [((i[0] + 1, i[1] - 1), (i[0] + 2, i[1] - 2))]

    return []

def moves_king(i, self, class2):
    legal_moves = []

    if i[1] == 7:
        if i[0] == 0:
            if self.board[(1, i[1] - 1)] == 0 and class2.board[(1, i[1] - 1)] == 0:
                legal_moves += [(1, i[1] - 1)]
        elif i[0] == 7:
            if self.board[(6, i[1] - 1)] == 0 and class2.board[(6, i[1] - 1)] == 0:
                legal_moves += [(6, i[1] - 1)]
        else:
            if self.board[(i[0] + 1, i[1] - 1)] == 0 and class2.board[(1, i[1] - 1)] == 0:
                legal_moves += [(1, i[1] - 1)]
            if self.board[(i[0] - 1, i[1] - 1)] == 0 and class2.board[(6, i[1] - 1)] == 0:
                legal_moves += [(6, i[1] - 1)]
    elif i[1] == 0:
        if i[0] == 0:
            if self.board[(1, i[1] + 1)] == 0 and class2.board[(1, i[1] + 1)] == 0:
                legal_moves += [(1, i[1] + 1)]
        elif i[0] == 7:
            if self.board[(6, i[1] + 1)] == 0 and class2.board[(6, i[1] + 1)] == 0:
                legal_moves += [(6, i[1] + 1)]
        else:
            if self.board[(i[0] + 1, i[1] + 1)] == 0 and class2.board[(1, i[1] + 1)] == 0:
                legal_moves += [(1, i[1] + 1)]
            if self.board[(i[0] - 1, i[1] + 1)] == 0 and class2.board[(6, i[1] + 1)] == 0:
                legal_moves += [(6, i[1] + 1)]
    else:
        if i[0] == 0:
            if self.board[(1, i[1] - 1)] == 0 and class2.board[(1, i[1] - 1)] == 0:
                legal_moves += [(1, i[1] - 1)]
            if self.board[(1, i[1] + 1)] == 0 and class2.board[(1, i[1] + 1)] == 0:
                legal_moves += [(1, i[1] + 1)]
        elif i[0] == 7:
            if self.board[(6, i[1] - 1)] == 0 and class2.board[(6, i[1] - 1)] == 0:
                legal_moves += [(6, i[1] - 1)]
            if self.board[(6, i[1] + 1)] == 0 and class2.board[(6, i[1] + 1)] == 0:
                legal_moves += [(6, i[1] + 1)]
        else:
            if self.board[(i[0] + 1, i[1] - 1)] == 0 and class2.board[(1, i[1] - 1)] == 0:
                legal_moves += [(1, i[1] - 1)]
            if self.board[(i[0] - 1, i[1] - 1)] == 0 and class2.board[(6, i[1] - 1)] == 0:
                legal_moves += [(6, i[1] - 1)]
            if self.board[(i[0] + 1, i[1] + 1)] == 0 and class2.board[(1, i[1] + 1)] == 0:
                legal_moves += [(1, i[1] + 1)]
            if self.board[(i[0] - 1, i[1] + 1)] == 0 and class2.board[(6, i[1] + 1)] == 0:
                legal_moves += [(6, i[1] + 1)]

    return legal_moves

def captures_king(i, self, class2):
    legal_captures = []

    if i[1] < 2:
        if i[0] < 2:
            if class2.board[(i[0] + 1, i[1] + 1)] == 1:
                if self.board[(i[0] + 2, i[1] + 2)] == 0 and class2.board[(i[0] + 2, i[1] + 2)] == 0:
                    legal_captures += [((i[0] + 1, i[1] + 1), (i[0] + 2, i[1] + 2))]
                    changes_1, changes_2 = capture(self, class2, i, [(i[0] + 1, i[1] + 1)], (i[0] + 2, i[1] + 2))
                    legal_captures += captures_king((i[0] + 2, i[1] + 2), changes_1, changes_2)
        elif i[0] > 5:
            if class2.board[(i[0] - 1, i[1] + 1)] == 1:
                if self.board[(i[0] - 2, i[1] + 2)] == 0 and class2.board[(i[0] - 2, i[2] + 2)] == 0:
                    legal_captures += [((i[0] - 1, i[1] + 1), (i[0] - 2, i[1] + 2))]
                    changes_1, changes_2 = capture(self, class2, i, [(i[0] - 1, i[1] + 1)], (i[0] - 2, i[1] + 2))
                    legal_captures += captures_king((i[0] - 2, i[1] + 2), changes_1, changes_2)
        else:
            if i[0] < 2:
                if class2.board[(i[0] + 1, i[1] + 1)] == 1:
                    if self.board[(i[0] + 2, i[1] + 2)] == 0 and class2.board[(i[0] + 2, i[1] + 2)] == 0:
                        legal_captures += [((i[0] + 1, i[1] + 1), (i[1] + 2, i[1] + 2))]
                        changes_1, changes_2 = capture(self, class2, i, [(i[0] + 1, i[1] + 1)], (i[0] + 2, i[1] + 2))
                        legal_captures += captures_king((i[0] + 2, i[1] + 2), changes_1, changes_2)

                if class2.board[(i[0] - 1, i[1] + 1)] == 1:
                    if self.board[(i[0] - 2, i[1] + 2)] == 0 and class2.board[(i[0] - 2, i[2] + 2)] == 0:
                        legal_captures += [((i[0] - 1, i[1] + 1), (i[0] - 2, i[1] + 2))]
                        changes_1, changes_2 = capture(self, class2, i, [(i[0] - 1, i[1] + 1)], (i[0] - 2, i[1] + 2))
                        legal_captures += captures_king((i[0] - 2, i[1] + 2), changes_1, changes_2)

    elif i[1] > 5:
        if i[0] < 2:
            if class2.board[(i[0] + 1, i[1] - 1)] == 1:
                if self.board[(i[0] + 2, i[1] - 2)] == 0 and class2.board[(i[0] + 2, i[1] - 2)] == 0:
                    legal_captures += [((i[0] + 1, i[1] - 1), (i[0] + 2, i[1] - 2))]
                    changes_1, changes_2 = capture(self, class2, i, [(i[0] + 1, i[1] - 1)], (i[0] + 2, i[1] - 2))
                    legal_captures += captures_king((i[0] + 2, i[1] - 2), changes_1, changes_2)
        elif i[0] > 5:
            if class2.board[(i[0] - 1, i[1] - 1)] == 1:
                if self.board[(i[0] - 2, i[1] - 2)] == 0 and class2.board[(i[0] - 2, i[1] - 2)] == 0:
                    legal_captures += [((i[0] - 1, i[1] - 1), (i[0] - 2, i[1] - 2))]
                    changes_1, changes_2 = capture(self, class2, i, [(i[0] - 1, i[1] - 1)], (i[0] - 2, i[1] - 2))
                    legal_captures += captures_king((i[0] - 2, i[1] - 2), changes_1, changes_2)
        else:
            if class2.board[(i[0] + 1, i[1] - 1)] == 1:
                if self.board[(i[0] + 2, i[1] - 2)] == 0 and class2.board[(i[0] + 2, i[1] - 2)] == 0:
                    legal_captures += [((i[0] + 1, i[1] - 1), (i[0] + 2, i[1] - 2))]
                    changes_1, changes_2 = capture(self, class2, i, [(i[0] + 1, i[1] - 1)], (i[0] + 2, i[1] - 2))
                    legal_captures += captures_king((i[0] + 2, i[1] - 2), changes_1, changes_2)

            if class2.board[(i[0] - 1, i[1] - 1)] == 1:
                if self.board[(i[0] - 2, i[1] - 2)] == 0 and class2.board[(i[0] - 2, i[1] - 2)] == 0:
                    legal_captures += [((i[0] - 1, i[1] - 1), (i[0] - 2, i[1] - 2))]
                    changes_1, changes_2 = capture(self, class2, i, [(i[0] - 1, i[1] - 1)], (i[0] - 2, i[1] - 2))
                    legal_captures += captures_king((i[0] - 2, i[1] - 2), changes_1, changes_2)

    else:
        if class2.board[(i[0] + 1, i[1] + 1)] == 1:
            if self.board[(i[0] + 2, i[1] + 2)] == 0 and class2.board[(i[0] + 2, i[1] + 2)] == 0:
                legal_captures += [((i[0] + 1, i[1] + 1), (i[1] + 2, i[1] + 2))]
                changes_1, changes_2 = capture(self, class2, i, [(i[0] + 1, i[1] + 1)], (i[0] + 2, i[1] + 2))
                legal_captures += captures_king((i[0] + 2, i[1] + 2), changes_1, changes_2)

        if class2.board[(i[0] - 1, i[1] + 1)] == 1:
            if self.board[(i[0] - 2, i[1] + 2)] == 0 and class2.board[(i[0] - 2, i[2] + 2)] == 0:
                legal_captures += [((i[0] - 1, i[1] + 1), (i[0] - 2, i[2] + 2))]
                changes_1, changes_2 = capture(self, class2, i, [(i[0] - 1, i[1] + 1)], (i[0] - 2, i[1] + 2))
                legal_captures += captures_king((i[0] - 2, i[1] + 2), changes_1, changes_2)

        if class2.board[(i[0] + 1, i[1] - 1)] == 1:
            if self.board[(i[0] + 2, i[1] - 2)] == 0 and class2.board[(i[0] + 2, i[1] - 2)] == 0:
                legal_captures += [((i[0] + 1, i[1] - 1), (i[0] + 2, i[1] - 2))]
                changes_1, changes_2 = capture(self, class2, i, [(i[0] + 1, i[1] - 1)], (i[0] + 2, i[1] - 2))
                legal_captures += captures_king((i[0] + 2, i[1] - 2), changes_1, changes_2)

        if class2.board[(i[0] - 1, i[1] - 1)] == 1:
            if self.board[(i[0] - 2, i[1] - 2)] == 0 and class2.board[(i[0] - 2, i[1] - 2)] == 0:
                legal_captures += [((i[0] - 1, i[1] - 1), (i[0] - 2, i[1] - 2))]
                changes_1, changes_2 = capture(self, class2, i, [(i[0] - 1, i[1] - 1)], (i[0] - 2, i[1] - 2))
                legal_captures += captures_king((i[0] - 2, i[1] - 2), changes_1, changes_2)

    return legal_captures


class Checkers:
    # This class will be used to keep track of all the white and black pieces on the board
    def __init__(self, board, first):
        self.board = board
        self.first = first


    def legal_moves(self, class2):
        legal_moves = {}

        for i in [k for k in self.board if self.board[k] != 0 and self.board[k] != -1]:
            legal_moves[i] = check_moves(i, self, class2, self.first)

        for i in [k for k in self.board if self.board[k] == 0]:
            legal_moves[i] = []

        return legal_moves

    def captures(self, class2):
        legal_captures = {}

        changed = False

        for i in [k for k in self.board if self.board[k] == 1]:
            legal_captures[i] = check_captures(i, self, class2)

        for i in [k for k in self.board if self.board[k] != 1]:
            legal_captures[i] = []

        return legal_captures

white_board = {}
for i in range(8):
    for k in range(8):
        if k % 2 == 0 and i % 2 == 1:
            white_board[(i,k)] = -1
        elif k % 2 == 1 and i % 2 == 0:
            white_board[(i,k)] = -1
        else:
            if k * 8 + i < 23:
                white_board[(i,k)] = 1
            else:
                white_board[(i,k)] = 0
whiteCheckers = Checkers(white_board, True)

black_board = {}
for i in range(8):
    for k in range(8):
        if k % 2 == 0 and i % 2 == 1:
            black_board[(i,k)] = -1
        elif k % 2 == 1 and i % 2 == 0:
            black_board[(i,k)] = -1
        else:
            if k * 8 + i > 39:
                black_board[(i,k)] = 1
            else:
                black_board[(i,k)] = 0
blackCheckers = Checkers(black_board, False)

def promote():
    for i in whiteCheckers.board:
        if i[1] == 7 and whiteCheckers.board[i] == 1:
            whiteCheckers.board[i] = 3

    for i in blackCheckers.board:
        if i[1] == 0 and whiteCheckers.board[i] == 1:
            blackCheckers.board[i] = 3

def draw_pieces(white, black):
    # Draws all the checkers pieces that are on the board
    for i in [i for i in white if white[i] == 1]:
        pygame.draw.circle(screen, 'White', (190 + 100 * i[0], 782 - 100 * i[1]), 40)
        pygame.draw.circle(screen, 'Black', (190 + 100 * i[0], 782 - 100 * i[1]), 40, 1)

    for i in [i for i in black if black[i] == 1]:
        pygame.draw.circle(screen, 'Black', (190 + 100 * i[0], 782 - 100 * i[1]), 40)
        pygame.draw.circle(screen, 'White', (190 + 100 * i[0], 782 - 100 * i[1]), 40, 1)

    for i in [i for i in white if white[i] == 3]:
        pygame.draw.circle(screen, 'White', (190 + 100 * i[0], 782 - 100 * i[1]), 40)
        pygame.draw.circle(screen, 'Black', (190 + 100 * i[0], 782 - 100 * i[1]), 40, 1)
        pygame.draw.circle(screen, 'Black', (190 + 100 * i[0], 782 - 100 * i[1]), 10, 5)

    for i in [i for i in black if black[i] == 3]:
        pygame.draw.circle(screen, 'Black', (190 + 100 * i[0], 782 - 100 * i[1]), 40)
        pygame.draw.circle(screen, 'White', (190 + 100 * i[0], 782 - 100 * i[1]), 40, 1)
        pygame.draw.circle(screen, 'White', (190 + 100 * i[0], 782 - 100 * i[1]), 10, 5)

def draw_moves(white, black, square):
    moves = white.captures(black)[square]
    # The code below draws the possible moves if you clicked on a piece
    if white.board[square] == 1:
        if len([k for k in white.captures(black) if white.captures(black)[k] != []]) == 0:
            moves = white.legal_moves(black)[square]
            for i in moves:
                pygame.draw.circle(screen, (0, 0, 255, 180), (190 + 100 * i[0], 782 - 100 * i[1]), 20)
                pygame.draw.circle(screen, 'White', (190 + 100 * i[0], 782 - 100 * i[1]), 20,
                                   1)
        elif len(moves) > 0:
            for i in moves:
                pygame.draw.circle(screen, (0, 0, 255, 180), (190 + 100 * i[1][0],
                                                              782 - 100 * i[1][1]), 20)
                pygame.draw.circle(screen, 'White', (190 + 100 * i[1][0],
                                                     782 - 100 * i[1][1]), 20,
                                   1)

def draw_board():
    for i in range(32):
        pygame.draw.rect(screen, beige, white_rects[i])
        pygame.draw.rect(screen, brown, black_rects[i])
    draw_pieces(whiteCheckers.board, blackCheckers.board)

def move(color, moved, move_to):
    """Moved indicated the piece moved while move indicates where it moves to"""
    color.board[moved] = 0
    color.board[move_to] = 1
    return color

def capture(color1, color2, moved, captured, move_to):
    """Moved indicates the piece moves, captures is a list indicating all the captured pieces, move_to indicates
    where the piece moves, color1 represents the color whose turn it is and color2 represents the other player"""
    capturing = True

    color2.board[captured] = 0
    color1.board[move_to] = color1.board[moved]
    color1.board[moved] = 0

    possibilities = color1.captures(color2)[move_to]

    while capturing:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    capturing = False

        if len(color1.captures(color2)[move_to]) == 0:
            capturing = False
        else:
            draw_moves(color1, color2, move_to)
            if pygame.mouse.get_pressed()[0]:
                for i in range(32):
                    pass

    return color1, color2



screen.fill(dark_green) # So that the screen isn't filled too many times every second
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()


    if menu:
        # The code below draws and provides functionality to the main menu of the game
        screen.blit(local_mult_surf, local_mult_rect)
        screen.blit(local_mult_text, local_mult_text_rect)
        screen.blit(bot_surf, bot_rect)
        screen.blit(bot_text, bot_text_rect)
        screen.blit(title_text, title_rect)

        if pygame.mouse.get_pressed()[0]:
            if local_mult_rect.collidepoint(mouse_pos):
                menu = False
                game_active = True
                bot = False
            elif bot_rect.collidepoint(mouse_pos):
                menu = False
                game_active = True
                bot = True

            screen.fill(dark_green)
            draw_board()

    else:
        if game_active:
            if pygame.mouse.get_pressed()[0]:
                for i in range(32):
                    # Checks whether the mouse collides with where a piece could be. There cannot be any pieces on the white squares
                    if black_rects[i].scale_by(0.8).collidepoint(mouse_pos):
                        if (i // 4) % 2 == 0:
                            being_moved = ((i % 4) * 2, i // 4)
                        else:
                            being_moved = ((i % 4) * 2 + 1, i // 4)
                        print("Being moved:", being_moved)
                        for k in previous_moves:
                            if k[1] % 2 == 0:
                                pygame.draw.rect(screen, brown, black_rects[int((k[0] / 2) + 4 * k[1])])
                            else:
                                pygame.draw.rect(screen, brown, black_rects[int((k[0] - 1) / 2 + 4 * k[1])])
                        if turn % 2 == 0:
                            draw_moves(whiteCheckers, blackCheckers, being_moved)
                        else:
                            draw_moves(blackCheckers, whiteCheckers, being_moved)

                    else:
                        if previous_moves == []:
                            pass

                if not bot:
                    if turn % 2 == 0:
                        if pygame.mouse.get_pressed()[0]:
                            for k in previous_moves:
                                if black_rects[int((k[0] - k[0] % 2) / 2 + 4 * k[1])].scale_by(0.7).collidepoint(mouse_pos):
                                    if capture:
                                        whiteCheckers, blackCheckers = capture(whiteCheckers, blackCheckers, previous_chosen, )
                                    else:
                                        whiteCheckers = move(whiteCheckers, previous_chosen, k)
                                        pygame.draw.rect(screen, brown, black_rects[int((previous_chosen[0] - previous_chosen[0] % 2) / 2 + 4 * previous_chosen[1])])
                                        draw_pieces(whiteCheckers.board, blackCheckers.board)
                                        turn_end = True
                                else:
                                    pass
                            if being_moved:
                                for j in whiteCheckers.captures(blackCheckers).copy()[being_moved]:
                                    capture = j[0:len(j) - 1]
                                    previous_moves = j[-1:]
                                if len(previous_moves) == 0:
                                    previous_moves = whiteCheckers.legal_moves(blackCheckers).copy()[being_moved]
                                else:
                                    capture_possible = True
                            else:
                                pass
                            previous_chosen = being_moved
                            if turn_end:
                                print("Turn end")
                                captured, capture_possible = False, False
                                capture = []
                                previous_moves = []
                                previous_chosen = -1
                                turn = (turn + 1) % 2
                                turn_end = False
                                promote()
                                draw_board()
                    else:
                        if pygame.mouse.get_pressed()[0]:
                            for k in previous_moves:
                                if black_rects[int((k[0] - k[0] % 2) / 2 + 4 * k[1])].scale_by(0.7).collidepoint(mouse_pos):
                                    blackCheckers = move(blackCheckers, previous_chosen, k)
                                    pygame.draw.rect(screen, brown, black_rects[int((previous_chosen[0] - previous_chosen[0] % 2) / 2 + 4 * previous_chosen[1])])
                                    draw_pieces(whiteCheckers.board, blackCheckers.board)
                                    turn_end = True
                                else:
                                    pass
                            if being_moved:
                                for j in whiteCheckers.captures(blackCheckers).copy()[being_moved]:
                                    capture = j[0:len(j) - 1]
                                    previous_moves = j[-1:]
                                if len(previous_moves) == 0:
                                    previous_moves = whiteCheckers.legal_moves(blackCheckers).copy()[being_moved]
                                else:
                                    capture_possible = True
                            else:
                                pass
                            previous_chosen = being_moved
                            if turn_end:
                                print("Turn end")
                                capture = []
                                captured, capture_possible = False, False
                                previous_moves = []
                                previous_chosen = -1
                                turn = (turn + 1) % 2
                                turn_end = False
                                promote()
                                draw_board()

                else:
                    turn = (turn + 1) % 2
        else:
            print("Unexpected game state")
            running = False

    pygame.display.flip()
    clock.tick(60)


pygame.quit()