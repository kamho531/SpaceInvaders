import pygame
import math
import random
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen (W, H)
screen = pygame.display.set_mode((1600, 900))

# background
background = pygame.image.load('assets/space5.png')

# title and icon
pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load('assets/ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('assets/spacefighter3.png')
playerX = 750
playerY = 700
playerX_move = 0

# enemies 
enemyImg = []
enemyX = []
enemyY = []
enemyX_move = []
enemyY_move = []
num_of_enemies = 10     # number of enemy
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('assets/alien4.png'))
    enemyX.append(random.randint(0, 1535))      # enemies appear random within range of x 
    enemyY.append(random.randint(50, 300))      # enemies appear random within range of y
    enemyX_move.append(3)
    enemyY_move.append(50)

# laser-bullet
# "ready" - can't see the bullet on the screen
# "fire" - bullet is currently moving
laserImg = pygame.image.load('assets/bullet.png')
laserX = 0 
laserY = 700     # same as playerY
laserX_move = 0
laserY_move = 30    # laser speed
laser_state = "ready"    

# score
score = 0
score_font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

# game over text
gameover_font = pygame.font.Font("freesansbold.ttf",96)
# win game text
wingame_font = pygame.font.Font("freesansbold.ttf",96)

def show_score(x, y):
    get_score = score_font.render("Score: "+str(score)+"   (100 to win)", True, (255,125,255))
    screen.blit(get_score, (x, y))

def game_over_text():
    get_text = gameover_font.render("GAME OVER", True, (125,255,125))
    screen.blit(get_text, (525, 400))

def win_game_text():
    get_win_text = wingame_font.render("You did it. You win!", True, (255, 0, 0))
    screen.blit(get_win_text, (350, 400))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x+32, y+10))  # to make sure laser shooting from the nose of the spaceship

def isCollided(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX-laserX,2)) + (math.pow(enemyY-laserY,2)))
    if distance < 27:
        return True
    else:
        return False



# game loop
screen_opening = True
while screen_opening:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # backdground image
    screen.blit(background,(0, 0))
    # playerY -= 1 move upward, += 1 move downward
    # playerX -= 1 move left, += 1 move right  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen_opening = False
   
        # if keystroke is pressed, check whether it is right or left    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_move = -3   # move left when left key pressed
            if event.key == pygame.K_RIGHT:
                playerX_move = 3    # move right when right key pressed
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":  # check if laser is fired or not
                    laser_sound = mixer.Sound('assets/laser.wav')
                    laser_sound.play()
                    laserX = playerX     # get current x coordinate of the spaceship
                    fire_laser(laserX, laserY)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_move = 0      # no movement when key is released


    # player movement
    playerX += playerX_move
    # check boundary of the player so it won't go out of the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1536:
        playerX = 1536


    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 700:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        # game win
        if score == 100:
            win_game_text()
            break
        
        
        enemyX[i] += enemyX_move[i]
        # check boundary of the enemy so it won't go out of the screen
        if enemyX[i] <= 0:
            enemyX_move[i] = 3
            enemyY[i] += enemyY_move[i]
        elif enemyX[i] >= 1536:
            enemyX_move[i] = -3
            enemyY[i] += enemyY_move[i]

        # Collision
        collision = isCollided(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explosion_sound = mixer.Sound('assets/explosion1.wav')
            explosion_sound.play()
            laserY = 700
            laser_state = "ready"
            score += 1           
            enemyX[i] = random.randint(0, 1535)
            enemyY[i] = random.randint(50, 300)

        enemy(enemyX[i], enemyY[i], i)
        

    # laser movement
    if laserY <= 0:        # reset laser-bullet to initial state to allow fire again
        laserY = 700
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_move
    
    # Collision
    collision = isCollided(enemyX[i], enemyY[i], laserX, laserY)
    if collision:
        explosion_sound = mixer.Sound('assets/explosion1.wav')
        explosion_sound.play()
        laserY = 700
        laser_state = "ready"
        score += 1
        enemyX[i] = random.randint(0, 1535)
        enemyY[i] = random.randint(50, 300)




    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
    





