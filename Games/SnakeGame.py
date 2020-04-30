# imports
import pygame
import random
import sys

# check for initializing errors
numpass, numfail = pygame.init()
if numfail > 0:
    print("(!) Had {0} initializing errors, exiting...".format(numfail))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized!")

# Play surface
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Snake game!')

# Colors
red = pygame.Color(255, 0, 0)  # game over
green = pygame.Color(0, 255, 0)  # snake
black = pygame.Color(0, 0, 0)  # score
white = pygame.Color(255, 255, 255)  # background
brown = pygame.Color(165, 42, 42)  # food

# FPS controller
fpsController = pygame.time.Clock()

# Important variables
scale = 10
width = 720
height = 460
snakePos = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]
foodPos = [random.randrange(1, width / 10) * scale, random.randrange(1, height / 10) * scale]
foodSpawn = True

direction = 'RIGHT'
changeto = direction

score = 0


# Game Over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (width / 2, 15)
    playSurface.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()
    pygame.quit()  # pygame exit
    sys.exit()  # console exit


# Show score
def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 24)
    Ssurf = sFont.render('Score: {0}'.format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (width / 2, 120)
    playSurface.blit(Ssurf, Srect)


# Main logic of the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # pygame exit
            sys.exit()  # console exit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeto = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeto = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # validation of direction
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    # Update snake position [x, y]
    if direction == 'RIGHT':
        snakePos[0] += scale
    if direction == 'LEFT':
        snakePos[0] -= scale
    if direction == 'UP':
        snakePos[1] -= scale
    if direction == 'DOWN':
        snakePos[1] += scale

    # Snake body mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    # Food Spawn
    if not foodSpawn:
        foodPos = [random.randrange(1, width / 10) * scale, random.randrange(1, height / 10) * scale]
        foodSpawn = True

    # Draw snake
    playSurface.fill(white)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], scale, scale))

    # Draw food
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], scale, scale))

    # Bound
    if snakePos[0] > width - scale or snakePos[0] < 0:
        gameOver()
    if snakePos[1] > height - scale or snakePos[1] < 0:
        gameOver()

    #Self hit
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()

    showScore()
    pygame.display.flip()
    fpsController.tick(10)
