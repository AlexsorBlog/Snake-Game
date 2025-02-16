import pygame

def draw_snake(game_window, snake_body):
    for segment in snake_body:
        image = pygame.image.load(segment[-1]).convert_alpha()
        game_window.blit(image, segment[0])
