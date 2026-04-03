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

previous_chosen = -1
being_moved = -1
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

def check_moves(i, class1, class2, first):
    # Returns all the legal moves for whichever piece is at i without including captures
    legal_moves = []

    if first:
        reverse = 0
    else:
        reverse = -1

    sign = 1 + 2 * reverse

    if (i // 4) % 2 == 0 - reverse:
        if i % 4 == 0 - 3 * reverse:
            if class2.board[i + sign * 4] == 0 and class1.board[i + sign * 4] == 0:
                legal_moves += [i + sign * 4]
            else:
                pass
        else:
            legal_moves += [i + sign * (3 + k) for k in [0, 1] if class2.board[i + sign * (3 + k)] == 0 and class1.board[i + sign * (3 + k)] == 0]
    else:
        if i % 4 == 3 + 3 * reverse:
            if class2.board[i + sign * 4] == 0 and class1.board[i + sign * 4] == 0:
                legal_moves += [i + sign * 4]
            else:
                pass
        else:
            legal_moves += [i + sign * (4 + k) for k in [0, 1] if class2.board[i + sign * (4 + k)] == 0 and class1.board[i + sign * (4 + k)] == 0]

    return legal_moves

def check_captures(i, self, class2):
    # Returns all legal captures for whichever piece is at i
    legal_captures = []

    if self.first:
        reverse = 0
    else:
        reverse = -1

    sign = 1 + 2 * reverse
    if (i // 4) % 2 == 0 - 3 * reverse:
        if i % 4 == 0:
            if class2.board[i + sign * 4] == 1 and class2.board[i + sign * 9] == 0 and self.board[i + sign * 9] == 0:
                new = i + sign * 4
                legal_captures += [[new, new + sign * 5]]
                legal_captures[len(legal_captures) - 1] += check_captures(new, self, class2)
            else:
                return []
        else:
            tested = [i + sign * (3 + k / 2) for k in [0, 2] if
                                 class2.board[i + sign * (3 + k / 2)] == 1 and class2.board[i + sign * (7 + k)] == 0 and self.board[i + sign * (7 + k) == 0]]
            for k in tested:
                legal_captures += [[k, 2 * k - i + sign]]
                legal_captures[len(legal_captures) - 1] += check_captures(2 * k - i + sign, self, class2)

    else:
        if i % 4 == 3 + 3 * reverse:
            if class2.board[i + sign * 4] == 1 and class2.board[i + sign * 7] == 0 and self.board[i + sign * 7] == 0:
                new = i + sign * 4
                legal_captures += new
                legal_captures += check_captures(new, self, class2)
            else:
                return []
        else:
            tested = [i + sign * (4 + k / 2) for k in [0, 2] if
                                 class2.board[i + sign * (4 + k / 2)] == 1 and class2.board[i + sign * (9 + k)] == 0 and self.board[i + sign * (9 + k)] == 0]
            for k in tested:
                legal_captures += k

    return legal_captures

class Checkers:
    # This class will be used to keep track of all the white and black pieces on the board
    def __init__(self, board, first):
        self.board = board
        self.first = first


    def legal_moves(self, class2):
        legal_moves = {}


        for i in [k for k in self.board if self.board[k] != 0]:
            legal_moves[i] = check_moves(i, self, class2, self.first)

        for i in range(32):
            if i not in legal_moves.copy().keys():
                legal_moves[i] = []

        return legal_moves

    def captures(self, class2):
        legal_captures = {}

        for i in [k for k in self.board if self.board[k] != 0 and len([j for j in self.legal_moves(class2) if self.legal_moves(class2)[j] != []]) < 2]:
            legal_captures[i] = check_captures(i, self, class2)

        for i in [k for k in range(32) if k not in legal_captures.copy().keys()]:
            legal_captures[i] = []

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
    # Draws all the checkers pieces that are on the board
    for i in [i for i in white if white[i] == 1]:
        pygame.draw.circle(screen, 'White', (190 + 200 * (i % 4) + 100 * ((i // 4) % 2),782 - 100 * (i // 4)), 40)
        pygame.draw.circle(screen, 'Black', (190 + 200 * (i % 4) + 100 * ((i // 4) % 2),782 - 100 * (i // 4)), 40, 1)

    for i in [i for i in black if black[i] == 1]:
        pygame.draw.circle(screen, 'Black', (190 + 200 * (i % 4) + 100 * ((i // 4) % 2), 782 - 100 * (i // 4)), 40)
        pygame.draw.circle(screen, 'White', (190 + 200 * (i % 4) + 100 * ((i // 4) % 2), 782 - 100 * (i // 4)), 40, 1)

def draw_moves(white, black, square):
    moves = [i for i in white.captures(black) if white.captures(black)[i] != []]
    print(moves)
    # The code below draws the possible moves if you clicked on a piece
    if white.board[square] == 1:
        if len(moves) == 0:
            moves = white.legal_moves(black)
            for i in [k for k in moves[square] if moves[square] != []]:
                pygame.draw.circle(screen, (0, 0, 255, 180), (190 + 200 * (i % 4) + 100 * ((i // 4) % 2), 782 - 100 * (i // 4)), 20)
                pygame.draw.circle(screen, 'White', (190 + 200 * (i % 4) + 100 * ((i // 4) % 2), 782 - 100 * (i // 4)), 20,
                                   1)
        else:
            for i in moves[square]:
                pygame.draw.circle(screen, (0, 0, 255, 180), (190 + 200 * (i % 4) + 100 * ((i // 4) % 2),
                                                              782 - 100 * (i // 4)), 20)
                pygame.draw.circle(screen, 'White', (190 + 200 * (i % 4) + 100 * ((i // 4) % 2),
                                                     782 - 100 * (i // 4)), 20,
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
    color1.board[moved] = 0
    for i in captured:
        color2.board[i] = 0
    color1.board[move_to] = 1
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
                        being_moved = 28 - 4 * (i // 4) + i % 4
                        for k in previous_moves:
                            #The equation below comes from the fact that the pieces are numbered from left
                            #to right starting from the bottom of the board while the black_rects list is
                            #numbered starting from the top left"""
                            pygame.draw.rect(screen, brown, black_rects[28 - 4 * (k // 4) + k % 4])
                        if turn % 2 == 0:
                            draw_moves(whiteCheckers, blackCheckers, 28 - 4 * (i // 4) + i % 4)
                        else:
                            draw_moves(blackCheckers, whiteCheckers, 28 - 4 * (i // 4) + i % 4)

                    else:
                        if previous_moves == []:
                            pass

                if not bot:
                    if turn % 2 == 0:
                        if pygame.mouse.get_pressed()[0]:
                            for k in previous_moves:
                                if black_rects[28 - 4 * (k // 4) + k % 4].scale_by(0.7).collidepoint(mouse_pos):
                                    whiteCheckers = move(whiteCheckers, previous_chosen, k)
                                    pygame.draw.rect(screen, brown, black_rects[28 - 4 * (previous_chosen // 4) + previous_chosen % 4])
                                    draw_pieces(whiteCheckers.board, blackCheckers.board)
                                    turn_end = True
                                else:
                                    pass
                            if being_moved >= 0:
                                previous_moves = whiteCheckers.legal_moves(blackCheckers).copy()[being_moved]
                            else:
                                pass
                            previous_chosen = being_moved
                            if turn_end:
                                print("Turn end")
                                previous_moves = []
                                previous_chosen = -1
                                turn = (turn + 1) % 2
                                turn_end = False
                                draw_board()
                    else:
                        if pygame.mouse.get_pressed()[0]:
                            print(previous_moves)
                            for k in previous_moves:
                                if black_rects[28 - 4 * (k // 4) + k % 4].scale_by(0.7).collidepoint(mouse_pos):
                                    blackCheckers = move(blackCheckers, previous_chosen, k)
                                    pygame.draw.rect(screen, brown, black_rects[28 - 4 * (previous_chosen // 4) + previous_chosen % 4])
                                    draw_pieces(whiteCheckers.board, blackCheckers.board)
                                    turn_end = True
                                else:
                                    pass
                            if being_moved >= 0:
                                previous_moves = blackCheckers.legal_moves(whiteCheckers).copy()[being_moved]
                            else:
                                pass
                            previous_chosen = being_moved
                            if turn_end:
                                print("Turn end")
                                previous_moves = []
                                previous_chosen = -1
                                turn = (turn + 1) % 2
                                turn_end = False
                                draw_board()

                else:
                    turn = (turn + 1) % 2
        else:
            print("Unexpected game state")
            running = False

    pygame.display.flip()
    clock.tick(60)


pygame.quit()