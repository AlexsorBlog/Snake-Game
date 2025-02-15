# importing libraries
import pygame
import time
import random
#111111111111111111111111
from snake import draw_snake

# def draw_snake():
#     for pos in snake_body:
#         pygame.draw.rect(game_window, green,
#                          pygame.Rect(pos[0], pos[1], 10, 10))

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)

    score_surface = score_font.render('Score : ' + str(score), True, color)

    score_rect = score_surface.get_rect()

    game_window.blit(score_surface, score_rect)


def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)

    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)

    game_over_rect = game_over_surface.get_rect()

    game_over_rect.midtop = (window_x / 2, window_y / 4)

    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    time.sleep(2)

    pygame.quit()

    quit()

if __name__ == "__main__":
    snake_speed = 10

    # Window size
    window_x = 720
    window_y = 480

    # defining colors
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    pygame.init()

    pygame.display.set_caption('Snake Game')
    game_window = pygame.display.set_mode((window_x, window_y))

    fps = pygame.time.Clock()

    fruit = pygame.image.load("Graphics/apple.png").convert()

    snake_heads = {
        "UP": "Graphics/head_up.png",
        "DOWN": "Graphics/head_down.png",
        "LEFT": "Graphics/head_left.png",
        "RIGHT": "Graphics/head_right.png"
    }

    snake_bodies = {
        "BOTTOM_LEFT": "Graphics/body_bottomleft.png",
        "BOTTOM_RIGHT": "Graphics/body_bottomright.png",
        "HORIZONTAL": "Graphics/body_horizontal.png",
        "TOP_LEFT": "Graphics/body_topleft.png",
        "TOP_RIGHT": "Graphics/body_topright.png",
        "VERTICAL": "Graphics/body_vertical.png"
    }
    # snake_body = "Graphics/body_horizontal.png"

    snake_position = [random.randrange(1, (window_x // 40)) * 40,
                      random.randrange(1, (window_y // 40)) * 40]

    snake_body = [[snake_position, snake_heads["RIGHT"]],
                  [[snake_position[0]-40, snake_position[1]], snake_bodies["HORIZONTAL"]],
                  [[snake_position[0]-80, snake_position[1]], snake_bodies["HORIZONTAL"]],
                  [[snake_position[0]-120, snake_position[1]], snake_bodies["HORIZONTAL"]]
                  ]

    fruit_position = [random.randrange(1, (window_x // 40)) * 40,
                      random.randrange(1, (window_y // 40)) * 40]
    fruit_spawn = True
    started = False
    direction = 'RIGHT'
    change_to = "RIGHT"

    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                started = True
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                    snake_body[0][-1] = snake_heads[change_to]
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                    snake_body[0][-1] = snake_heads[change_to]
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                    snake_body[0][-1] = snake_heads[change_to]
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                    snake_body[0][-1] = snake_heads[change_to]

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_position[1] -= 40
        if direction == 'DOWN':
            snake_position[1] += 40
        if direction == 'LEFT':
            snake_position[0] -= 40
        if direction == 'RIGHT':
            snake_position[0] += 40
        for i in range(len(snake_body) - 1, 0, -1):
            if i == 1:
                new_coordinates = snake_position
                if (snake_body[i][0][0] > new_coordinates[0] or snake_body[i][0][0] < new_coordinates[0]) and \
                        snake_body[i][0][1] == new_coordinates[1]:
                    body_direction = "HORIZONTAL"
                elif (snake_body[i][0][1] > new_coordinates[1] or snake_body[i][0][1] < new_coordinates[1]) and \
                        snake_body[i][0][0] == new_coordinates[0]:
                    body_direction = "VERTICAL"
                elif ((snake_body[i][0][0] < new_coordinates[0] and snake_body[i][0][1] > new_coordinates[1]) or (snake_body[i][0][0] > new_coordinates[0] and snake_body[i][0][1] < new_coordinates[1])) and (direction == "UP" or direction=="LEFT"):
                    body_direction = "TOP_LEFT"
                elif ((snake_body[i][0][0] < new_coordinates[0] and snake_body[i][0][1] < new_coordinates[1]) or (snake_body[i][0][0] > new_coordinates[0] and snake_body[i][0][1] > new_coordinates[1])) and (direction == "DOWN" or direction=="LEFT"):
                    body_direction = "BOTTOM_LEFT"
                elif (snake_body[i][0][0] > new_coordinates[0] and snake_body[i][0][1] > new_coordinates[1]) or (snake_body[i][0][0] < new_coordinates[0] and snake_body[i][0][1] < new_coordinates[1]):
                    body_direction = "TOP_RIGHT"
                elif (snake_body[i][0][0] > new_coordinates[0] and snake_body[i][0][1] < new_coordinates[1]) or (snake_body[i][0][0] < new_coordinates[0] and snake_body[i][0][1] > new_coordinates[1]):
                    body_direction = "BOTTOM_RIGHT"
                snake_body[i][0] = snake_body[0][0]
                snake_body[i][1] = snake_bodies[body_direction]
            else:
                snake_body[i] = list(snake_body[i - 1])

        snake_body[0] = [list(snake_position), snake_heads[direction]]

        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 1
            fruit_position = [random.randrange(1, (window_x // 40)) * 40,
                              random.randrange(1, (window_y // 40)) * 40]
            snake_body.append(snake_body[-1])

        game_window.fill(white)

        game_window.blit(fruit,
            [fruit_position[0], fruit_position[1]])

        draw_snake(game_window, snake_body)
        if started==False:
            pass
        else:
            if snake_position[0] < 0 or snake_position[0] > window_x - 40:
                game_over()
            if snake_position[1] < 0 or snake_position[1] > window_y - 40:
                game_over()
            for block in snake_body:
                if snake_body[0] == block:
                    pass
                elif snake_position[0] == block[0][0] and snake_position[1] == block[0][1]:
                    print(block)
                    game_over()
        show_score(1, black, 'times new roman', 20)

        pygame.display.update()

        fps.tick(snake_speed)
