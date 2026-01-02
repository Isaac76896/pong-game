import pygame
import sys

#Initiating pygame
pygame.init() #ALWAYS needs to be used in order to use pygame
pygame.display.set_caption("Pong Game")  #Caption for the window
print("Game running successfully")

#Game variables
WIDTH = 600
HEIGHT = 400
PADDLE_SPEED = 5
BALL_SIZE = 10
BALL_SPEED_Y = 5
BALL_SPEED_X = 5
SCORE1 = 0
SCORE2 = 0
SERVE_OFFSET = 20
FREE_MOVEMENT_ACTIVATION = 3

#Objects
font = pygame.font.SysFont(None, 36) #Font for score display
paddle1 = pygame.Rect(20, HEIGHT // 2 - 40, 10, 80) #Creating paddle 1
paddle2 = pygame.Rect(WIDTH - 30, HEIGHT // 2 - 40, 10, 80) #Creating paddle 2
paddle1_boundaries = pygame.Rect(
    0,          # left edge
    0,          # top edge
    300,        # width → up to x = 299
    HEIGHT
)

paddle2_boundaries = pygame.Rect(
    301,        # left edge
    0,          # top edge
    WIDTH - 301,# width → from x = 301 to right edge
    HEIGHT
)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,HEIGHT // 2 - BALL_SIZE // 2,BALL_SIZE,BALL_SIZE) #Creating pong ball
window = pygame.display.set_mode((WIDTH,HEIGHT))  #Setting width and height to the window
clock = pygame.time.Clock() #Used for the frame rate


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
    if ball.colliderect(paddle1):
        ball.left = paddle1.right
        BALL_SPEED_X *= -1

    if ball.colliderect(paddle2):
        ball.right = paddle2.left
        BALL_SPEED_X *= -1
    
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



    #Drawing
    window.fill((0, 0, 0))  # Draws the content of the screen with RGB colors
    pygame.draw.rect(window, (0, 102, 204), paddle1) # Draw paddle 1 using RGB colors "blue"
    pygame.draw.rect(window, (153, 0, 0), paddle2) #Draw paddle 2 "red"
    pygame.draw.rect(window, (255, 165, 0), ball)  # Draw ball "orange"
    score_text = font.render(f"{SCORE1}   {SCORE2}", True, (255, 255, 255)) #Converts text into a surface
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


