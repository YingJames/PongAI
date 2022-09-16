import pygame
from ball import Ball
from paddle import Paddle
pygame.init() 

# constants
WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PongAI")

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("futura", 50)
WINNING_SCORE = 5


def draw(window, paddles, ball, left_score, right_score):
    window.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    window.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width()//2, 20))
    window.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(window)

    # dashed line in the middle
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(WINDOW)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):

    # ball will bounce back at opposite direction touching top and bot of screen
    if (ball.y + ball.radius >= HEIGHT):
        ball.y_vel *= -1
    elif (ball.y - ball.radius <= 0):
        ball.y_vel *= -1

    # hitting the left paddle
    if (ball.x_vel < 0):
        if (ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height):
            if ((ball.x - ball.radius) <= (left_paddle.x + left_paddle.width)):
                ball.x_vel = ball.flip(ball.x_vel)

                # change y_vel based on where the ball hits the paddle
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL 
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1

    else:
    # hitting the right paddle
        if (ball.x_vel > 0):
            if (ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height):
                if ((ball.x + ball.radius) >= right_paddle.x):
                    ball.x_vel = ball.flip(ball.x_vel)

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL 
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = y_vel * -1

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if (keys[pygame.K_w] and (left_paddle.y - left_paddle.VEL >= 0)):
        left_paddle.move(up=True)
    if (keys[pygame.K_s] and (left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT)):
        left_paddle.move(up=False)

    if (keys[pygame.K_UP] and (right_paddle.y - right_paddle.VEL >= 0)):
        right_paddle.move(up=True)
    if (keys[pygame.K_DOWN] and (right_paddle.y + right_paddle.VEL +right_paddle.height <= HEIGHT)):
        right_paddle.move(up=False)

def main(): 

    run = True
    clock = pygame.time.Clock()

    # draws paddle at the edges of the screen
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH //2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        # regulate game to 60fps
        clock.tick(FPS)
        
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score) 

        for event in pygame.event.get():
            # when player clicks close window btn
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if (ball.x < 0):
            right_score += 1
            ball.reset(ball.x)
        elif (ball.x > WIDTH):
            left_score += 1
            ball.reset(ball.x)

        won = False
        if (left_score >= WINNING_SCORE):
            won = True
            win_text = "Left Player Won!"

        elif (right_score >= WINNING_SCORE):
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset(0)
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()