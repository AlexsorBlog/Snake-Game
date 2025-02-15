import pygame

def draw_snake(game_window, snake_body):
    for pos in snake_body:
        myimage = pygame.image.load(pos[-1]).convert()
        game_window.blit(myimage, pos[0])
        pygame.display.flip()
        pygame.display.update()