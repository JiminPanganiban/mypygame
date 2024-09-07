import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLANE_WIDTH = 100
PLANE_HEIGHT = 20
BALL_RADIUS = 15
PLANE_COLOR = (0, 0, 255)  # Blue
BALL_COLOR = (255, 0, 0)   # Red
BACKGROUND_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black
FPS = 60

# Set up display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Plane and Ball Game')

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_objects(start_screen=False):
    screen.fill(BACKGROUND_COLOR)
    
    if start_screen:
        draw_text('Click Start to Begin', font, TEXT_COLOR, screen, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        draw_text('Start', font, TEXT_COLOR, screen, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
    else:
        pygame.draw.rect(screen, PLANE_COLOR, plane)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)
        draw_text(f'Score: {score}', font, TEXT_COLOR, screen, 100, 30)
        draw_text(f'High Score: {high_score}', font, TEXT_COLOR, screen, WINDOW_WIDTH - 100, 30)
    
    pygame.display.flip()

def move_ball():
    global ball, ball_dx, ball_dy, score, game_over
    
    # Move the ball
    ball.x += ball_dx
    ball.y += ball_dy
    
    # Ball collision with walls
    if ball.left < 0 or ball.right > WINDOW_WIDTH:
        ball_dx *= -1
    if ball.top < 0:
        ball_dy *= -1
    
    # Ball collision with plane
    if ball.colliderect(plane):
        ball_dy *= -1
        ball.top = plane.top - BALL_RADIUS * 2
        # Increment score
        score += 1

    # Check if ball falls below screen
    if ball.bottom > WINDOW_HEIGHT:
        game_over = True

def main():
    global plane, score, ball_dx, ball_dy, game_over, start_game, plane_speed, high_score

    game_over = False
    start_game = False
    plane.x = WINDOW_WIDTH // 2 - PLANE_WIDTH // 2
    plane.y = WINDOW_HEIGHT - PLANE_HEIGHT - 10
    ball = pygame.Rect(plane.centerx - BALL_RADIUS, plane.top - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_dx = random.choice([-5, 5])
    ball_dy = -5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN and not start_game:
                mouse_x, mouse_y = event.pos
                if WINDOW_WIDTH // 2 - 50 <= mouse_x <= WINDOW_WIDTH // 2 + 50 and WINDOW_HEIGHT // 2 + 20 <= mouse_y <= WINDOW_HEIGHT // 2 + 80:
                    start_game = True

        keys = pygame.key.get_pressed()
        if start_game:
            if keys[pygame.K_LEFT] and plane.left > 0:
                plane.x -= plane_speed
            if keys[pygame.K_RIGHT] and plane.right < WINDOW_WIDTH:
                plane.x += plane_speed
            
            move_ball()
            if game_over:
                # Check and update high score
                if score > high_score:
                    high_score = score
                draw_objects()
                draw_text('Try Again!', font, TEXT_COLOR, screen, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(2000) 
                score = 0  # Reset score
                main()
            else:
                draw_objects()
        else:
            draw_objects(start_screen=True)
        
        clock.tick(FPS)

if __name__ == "__main__":
    plane_speed = 15  # Adjusted plane speed for faster movement
    plane = pygame.Rect(WINDOW_WIDTH // 2 - PLANE_WIDTH // 2, WINDOW_HEIGHT - PLANE_HEIGHT - 10, PLANE_WIDTH, PLANE_HEIGHT)
    ball = pygame.Rect(plane.centerx - BALL_RADIUS, plane.top - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_dx = random.choice([-5, 5])
    ball_dy = -5
    score = 0
    high_score = 0
    main()
    pygame.quit()
