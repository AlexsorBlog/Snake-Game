import pygame
import time
import random
from snake import draw_snake
#w

def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)


def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(f'Your Score is : {score}', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()


def wait_for_start():
    """Очікування натискання пробілу перед початком гри."""
    game_window.fill(white)
    message_font = pygame.font.SysFont('times new roman', 30)
    message_surface = message_font.render("Натисніть ПРОБІЛ для початку гри", True, black)
    message_rect = message_surface.get_rect(center=(window_x / 2, window_y / 2))
    game_window.blit(message_surface, message_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # Вихід із циклу після натискання ПРОБІЛА


if __name__ == "__main__":
    snake_speed = 10
    window_x, window_y = 720, 480

    black, white, red, green, blue = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)

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

    snake_tails = {
        "UP": "Graphics/tail_down.png",
        "DOWN": "Graphics/tail_up.png",
        "LEFT": "Graphics/tail_right.png",
        "RIGHT": "Graphics/tail_left.png"
    }

    snake_position = [random.randrange(1, (window_x // 40)) * 40,
                      random.randrange(1, (window_y // 40)) * 40]

    snake_body = [
        [list(snake_position), snake_heads["RIGHT"]],
        [[snake_position[0] - 40, snake_position[1]], snake_bodies["HORIZONTAL"]],
        [[snake_position[0] - 80, snake_position[1]], snake_bodies["HORIZONTAL"]],
        [[snake_position[0] - 120, snake_position[1]], snake_tails["RIGHT"]]
    ]

    fruit_position = [random.randrange(1, (window_x // 40)) * 40,
                      random.randrange(1, (window_y // 40)) * 40]
    started = False
    direction = 'RIGHT'
    change_to = "RIGHT"
    score = 0




    wait_for_start()  # Очікування натискання ПРОБІЛА перед стартом

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                started = True
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
            for block in snake_body[1:]:  # Перевіряємо всі частини тіла, крім голови
                 if snake_position == block[0]:  # Якщо координати голови збігаються з будь-яким сегментом тіла
                    game_over()



        direction = change_to
        cell_size = 40


        if direction == 'UP':
            snake_position[1] -= cell_size
        elif direction == 'DOWN':
            snake_position[1] += cell_size
        elif direction == 'LEFT':
            snake_position[0] -= cell_size
        elif direction == 'RIGHT':
            snake_position[0] += cell_size

        # Телепортація
        if snake_position[0] < 0:
            snake_position[0] = window_x - cell_size
        elif snake_position[0] > window_x - cell_size:
            snake_position[0] = 0

        if snake_position[1] < 0:
            snake_position[1] = window_y - cell_size
        elif snake_position[1] > window_y - cell_size:
            snake_position[1] = 0

            # Перевірка на зіткнення з тілом
            for block in snake_body[1:]:
                if snake_position == block[0]:
                    game_over()

        new_head = [list(snake_position), snake_heads[direction]]
        snake_body.insert(0, new_head)

        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 1
            fruit_position = [random.randrange(1, (window_x // 40)) * 40,
                              random.randrange(1, (window_y // 40)) * 40]
        else:
            snake_body.pop()

        # Оновлення тіла
        for i in range(1, len(snake_body) - 1):
            prev_segment = snake_body[i - 1][0]
            current_segment = snake_body[i][0]
            next_segment = snake_body[i + 1][0]

            if prev_segment[0] == next_segment[0]:
                snake_body[i][1] = snake_bodies["VERTICAL"]
            elif prev_segment[1] == next_segment[1]:
                snake_body[i][1] = snake_bodies["HORIZONTAL"]
            elif (prev_segment[0] < current_segment[0] and next_segment[1] < current_segment[1]) or \
                    (prev_segment[1] < current_segment[1] and next_segment[0] < current_segment[0]):
                snake_body[i][1] = snake_bodies["TOP_LEFT"]
            elif (prev_segment[0] > current_segment[0] and next_segment[1] < current_segment[1]) or \
                    (prev_segment[1] < current_segment[1] and next_segment[0] > current_segment[0]):
                snake_body[i][1] = snake_bodies["TOP_RIGHT"]
            elif (prev_segment[0] < current_segment[0] and next_segment[1] > current_segment[1]) or \
                    (prev_segment[1] > current_segment[1] and next_segment[0] < current_segment[0]):
                snake_body[i][1] = snake_bodies["BOTTOM_LEFT"]
            elif (prev_segment[0] > current_segment[0] and next_segment[1] > current_segment[1]) or \
                    (prev_segment[1] > current_segment[1] and next_segment[0] > current_segment[0]):
                snake_body[i][1] = snake_bodies["BOTTOM_RIGHT"]

        # Оновлення хвоста
        last_segment = snake_body[-1][0]
        second_last_segment = snake_body[-2][0]

        if last_segment[0] < second_last_segment[0]:
            snake_body[-1][1] = snake_tails["RIGHT"]
        elif last_segment[0] > second_last_segment[0]:
            snake_body[-1][1] = snake_tails["LEFT"]
        elif last_segment[1] < second_last_segment[1]:
            snake_body[-1][1] = snake_tails["DOWN"]
        elif last_segment[1] > second_last_segment[1]:
            snake_body[-1][1] = snake_tails["UP"]

        game_window.fill(white)
        game_window.blit(fruit, fruit_position)
        draw_snake(game_window, snake_body)

        show_score(black, 'times new roman', 20)
        pygame.display.update()
        fps.tick(10 + score // 5)