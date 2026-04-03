import pygame

pygame.init()
screen = pygame.display.set_mode((1080, 864))
clock = pygame.time.Clock()
running = True
menu = True
game_active = False

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((25,120,12))

    screen.blit(local_mult_surf, local_mult_rect)
    screen.blit(local_mult_text, local_mult_text_rect)
    screen.blit(bot_surf, bot_rect)
    screen.blit(bot_text, bot_text_rect)
    screen.blit(title_text, title_rect)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()