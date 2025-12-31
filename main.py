import pygame
import sys

#Initiating pygame
pygame.init() #ALWAYS needs to be used in order to use pygame
pygame.display.set_caption("Pong Game")  #Caption for the window

#Game variables
WIDTH = 600
HEIGHT = 400
PADDLE_SPEED = 5
BALL_SIZE = 10
BALL_SPEED_Y = 4
BALL_SPEED_X = 4


#Objects
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
            pygame.quit()
            sys.exit()

    #Input 
    keys = pygame.key.get_pressed()

    #Movement for paddle 1
    if keys[pygame.K_w]:
        paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s]:
        paddle1.y += PADDLE_SPEED
    if keys[pygame.K_a]:
        paddle1.x -= PADDLE_SPEED
    if keys[pygame.K_d]:
        paddle1.x += PADDLE_SPEED
    
    #Movement for paddle 2
    if keys[pygame.K_UP]:
        paddle2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]:
        paddle2.y += PADDLE_SPEED
    if keys[pygame.K_LEFT]:
        paddle2.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT]:
        paddle2.x += PADDLE_SPEED
    
    #Constraints
    paddle1.clamp_ip(paddle1_boundaries)
    paddle2.clamp_ip(paddle2_boundaries)

    #Drawing
    window.fill((0, 0, 0))  # Draws the content of the screen with RGB colors
    pygame.draw.rect(window, (0, 102, 204), paddle1) # Draw paddle using RGB colors
    pygame.draw.rect(window, (153, 0, 0), paddle2)

    #Center dashed line 
    line_width = 6
    line_height = 20
    gap = 10
    center_x = WIDTH // 2 - line_width // 2
    
    for y in range(0, HEIGHT, line_height + gap): #Loop that creates tiny rectangles starting from the top and ending at the bottom
        pygame.draw.rect(window,(200, 200, 200),(center_x, y, line_width, line_height)) 

    pygame.display.flip() #Updates every frame in the entire screen
    clock.tick(60) #60 frames per second


# Testing Git sync between PC and laptop

#Yes, it did work on laptop 