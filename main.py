import os
import pygame
import sys

#Guarantees that it works anywhere
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

#Initiating pygame
pygame.init() #ALWAYS needs to be used in order to use pygame
pygame.display.set_caption("Mad Pong Game")  #Caption for the window
print("Game running successfully")

#Game variables
WIDTH = 1000
HEIGHT = 500
PADDLE_SPEED = 6
BALL_SIZE = 10
BALL_SPEED_Y = 7
BALL_SPEED_X = 7
SCORE1 = 0
SCORE2 = 0
SERVE_OFFSET = 20
FREE_MOVEMENT_ACTIVATION = 0
WIN_SCORE = 1
GAME_OVER = False
COLLISION_COOLDOWN = 0
MAX_BALL_Y_SPEED = 8
MAX_BALL_X_SPEED = 14

#Objects

#Fonts
try:
    font = pygame.font.Font(os.path.join(FONTS_DIR, "Extradition.ttf"), 36) #Font used for the score
    game_over_font = pygame.font.Font(os.path.join(FONTS_DIR, "Extradition-Italic.ttf"), 50) #Font used for the game over screen
except FileNotFoundError:
    font = pygame.font.SysFont(None, 36)
    game_over_font = pygame.font.SysFont(None, 50)

window = pygame.display.set_mode((WIDTH,HEIGHT))  #Setting width and height to the window
clock = pygame.time.Clock() #Used for the frame rate


#Functions

def bounce_from_paddle(ball, paddle):
    global BALL_SPEED_X, BALL_SPEED_Y

    prev_y = BALL_SPEED_Y

    # How far from center did the ball hit? (-1 to 1)
    offset = (ball.centery - paddle.centery) / (paddle.height / 2)

    # Set vertical speed based on where it hit
    BALL_SPEED_Y = int(offset * (MAX_BALL_Y_SPEED + 2))

    # Make sure it's not perfectly flat
    if BALL_SPEED_Y == 0:
        BALL_SPEED_Y = 1 if prev_y > 0 else -1

    # Bounce back horizontally AND speed up
    BALL_SPEED_X *= -1
    
    # Speed boost for center hits
    if abs(offset) < 0.3:  # If hit near center (adjust 0.3 to make the "middle" zone bigger/smaller)
        BALL_SPEED_X = int(BALL_SPEED_X * 1.2)  # 20% speed boost (adjust 1.2 to increase/decrease boost)

    # Keeps the ball speed within it's limit, so it doesn't infinitely become faster
    BALL_SPEED_Y = max(-MAX_BALL_Y_SPEED, min(BALL_SPEED_Y, MAX_BALL_Y_SPEED))
    BALL_SPEED_X = max(-MAX_BALL_X_SPEED, min(BALL_SPEED_X, MAX_BALL_X_SPEED))


# -------------------- PLAY SCENE --------------------
def play_scene():
    global SCORE1, SCORE2, BALL_SPEED_X, BALL_SPEED_Y, GAME_OVER, COLLISION_COOLDOWN, PADDLE_SPEED

    SCORE1 = 0
    SCORE2 = 0
    GAME_OVER = False
    COLLISION_COOLDOWN = 0
    BALL_SPEED_X = 7
    BALL_SPEED_Y = 7
    speed_message_printed = False


    paddle1 = pygame.Rect(20, HEIGHT // 2 - 40, 10, 80) #Creating paddle 1
    paddle2 = pygame.Rect(WIDTH - 30, HEIGHT // 2 - 40, 10, 80) #Creating paddle 2

    paddle1_boundaries = pygame.Rect(
        0,          # left edge
        0,          # top edge
        (WIDTH //2) - 1,  # The width of the rectangle = 499
        HEIGHT
    )

    paddle2_boundaries = pygame.Rect(
        (WIDTH // 2) + 1,   # left edge   x = 501
        0,          # top edge
        (WIDTH // 2) - 1,# The width of the rectangle
        HEIGHT # The height of the rectangle 
    )

    ball = pygame.Rect(
        WIDTH // 2 - BALL_SIZE // 2,
        HEIGHT // 2 - BALL_SIZE // 2,
        BALL_SIZE,
        BALL_SIZE
    ) #Creating pong ball

    #Loop game
    while True: #Loop to keep the game running; checking for events constantly 
        for event in pygame.event.get():              
            if event.type == pygame.QUIT:
                print("Game over!")
                pygame.quit()
                sys.exit()

        #Input 
        keys = pygame.key.get_pressed()

        #Movement for paddle 1
        if keys[pygame.K_w]:
            paddle1.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            paddle1.y += PADDLE_SPEED
        if SCORE1 >= FREE_MOVEMENT_ACTIVATION: #Activates free movement feature
            if keys[pygame.K_a]:
                paddle1.x -= PADDLE_SPEED
            if keys[pygame.K_d]:
                paddle1.x += PADDLE_SPEED
        
        #Movement for paddle 2
        if keys[pygame.K_UP]:
            paddle2.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            paddle2.y += PADDLE_SPEED
        if SCORE2 >= FREE_MOVEMENT_ACTIVATION: #Activates free movement feature
            if keys[pygame.K_LEFT]:
                paddle2.x -= PADDLE_SPEED
            if keys[pygame.K_RIGHT]:
                paddle2.x += PADDLE_SPEED
        
        #Increases paddle speed when BALL_SPEED_X is equals or greater than 9
        if abs(BALL_SPEED_X) >= 9:
            PADDLE_SPEED = 8  # Faster paddles
            if not speed_message_printed:  
                print("Ball is going faster now!!!!")
                speed_message_printed = True
        else:
            PADDLE_SPEED = 6  # Normal speed
            speed_message_printed = False

        #Movement for ball
        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        #Constraints
        paddle1.clamp_ip(paddle1_boundaries) #boundaries for paddle 1
        paddle2.clamp_ip(paddle2_boundaries) #Boundaries for paddle 2
        
        #Ball Wall Collision
        if ball.top <= 0 or ball.bottom >= HEIGHT:#Makes the ball go in the opposite direction once it collides with the top or bottom walls
            BALL_SPEED_Y *= -1 
        
        #Ball Paddle Collision
        if COLLISION_COOLDOWN > 0:  #Condition to prevent phasing through the paddles 
            COLLISION_COOLDOWN -= 1

        if COLLISION_COOLDOWN == 0 and ball.colliderect(paddle1): #Collision for paddle1
            ball.left = paddle1.right
            bounce_from_paddle(ball, paddle1)
            COLLISION_COOLDOWN = 5

        if COLLISION_COOLDOWN == 0 and ball.colliderect(paddle2): #Collision for paddle2
            ball.right = paddle2.left
            bounce_from_paddle(ball, paddle2)
            COLLISION_COOLDOWN = 5

        #Scoring
        if ball.left <= 0:
            SCORE2 += 1

            # Serve to Player 1 (loser)

            #Resets paddle1's position
            paddle1.left = 20  #Moves paddle1 to x = 20
            paddle1.top = HEIGHT // 2 - 40 #Centers paddle

            #Resets paddle2's position
            paddle2.left = WIDTH - 30  #Moves paddle2 to x = 570
            paddle2.top = HEIGHT // 2 - 40 #Centers paddle

            #Resets ball in front of the paddle1
            ball.left = paddle1.right + SERVE_OFFSET
            ball.centery = paddle1.centery
            
            BALL_SPEED_X = abs(BALL_SPEED_X)  # move right

        if ball.right >= WIDTH:
            SCORE1 += 1

            # Serve to Player 2 (loser)
            
            #Resets paddle1's position
            paddle1.left = 20  #Moves paddle1 to x = 20
            paddle1.top = HEIGHT // 2 - 40 #Centers paddle

            #Resets paddle2's position
            paddle2.left = WIDTH - 30  #Moves paddle2 to x = 570
            paddle2.top = HEIGHT // 2 - 40 #Centers paddle

            #Resets ball in front of paddle2
            ball.right = paddle2.left - SERVE_OFFSET
            ball.centery = paddle2.centery

            BALL_SPEED_X = -abs(BALL_SPEED_X)  # move left

        #Game ending
        if not GAME_OVER and (SCORE1 >= WIN_SCORE or SCORE2 >= WIN_SCORE):
            return game_over_scene()

        #Drawing
        window.fill((0, 0, 0))  # Draws the content of the screen with RGB colors
        pygame.draw.rect(window, (0, 102, 204), paddle1) # Draw paddle 1 using RGB colors "blue"
        pygame.draw.rect(window, (153, 0, 0), paddle2) #Draw paddle 2 "red"
        pygame.draw.rect(window, (255, 165, 0), ball)  # Draw ball "orange"
        score_text = font.render(f"{SCORE1}   {SCORE2}", True, (255, 255, 255)) #Converts text into a surface (Score)
        window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20)) #Places the text(surface) we created on the object that is calling it (window)

        #Center dashed line 
        line_width = 6
        line_height = 20
        gap = 10
        center_x = WIDTH // 2 - line_width // 2
        
        for y in range(0, HEIGHT, line_height + gap): #Loop that creates tiny rectangles starting from the top and ending at the bottom
            pygame.draw.rect(window,(200, 200, 200),(center_x, y, line_width, line_height)) 

        pygame.display.flip() #Updates every frame in the entire screen
        clock.tick(60) #60 frames per second


# -------------------- GAME OVER SCENE --------------------
def game_over_scene():
    global GAME_OVER
    GAME_OVER = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                return play_scene  # NEW: restart game

        window.fill((0, 0, 0))
        game_over_text = game_over_font.render(f"GAME OVER!!!", True, (210, 43, 43))
        window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(60)


# -------------------- SCENE MANAGER (NEW) --------------------
def main():
    current_scene = play_scene
    while current_scene:
        current_scene = current_scene()


if __name__ == "__main__":
    main()
