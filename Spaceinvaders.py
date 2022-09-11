import random, math
import pygame as pg
from pygame import mixer

# initialize pygame
pg.init()

# create the screen
screen = pg.display.set_mode((800, 600))

# background
background = pg.image.load('background.png')
mixer.music.load('background.mp3')
mixer.music.play(-1)

# game title6
pg.display.set_caption("Space Invaders")

# to set game icon
icon = pg.image.load('logo.png')
pg.display.set_icon(icon)

# player
playerimg = pg.image.load('spaceship.png')
playerx = 370
playery = 480
playerx_change = 0

# bullet
bulletimg = pg.image.load('bullet.png')
bulletx = 0
bullety = 480
bullety_change = 10
bulletstate = 'ready'
# ready - bullet is ready to fire
# fire - bullet is currently firing/moving

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
numenemies = 6

for i in range(numenemies):
    enemyimg.append(pg.image.load('alien.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 200))
    enemyx_change.append(3)
    enemyy_change.append(20)

scoreval = 0  # to display score
font = pg.font.Font('freesansbold.ttf', 30)

textx = 10
texty = 10

# game over text
overfont = pg.font.Font('freesansbold.ttf', 64)


def showscore(x, y):
    # to render the text and then draw it on screen
    score = font.render("Score: " + str(scoreval), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameover():
    overtext = overfont.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(overtext, (200, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))  # we are drawing the image of player onto screen


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))  # we are drawing the image of enemy onto screen


def firebullet(x, y):
    global bulletstate
    bulletstate = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(((enemyx - bulletx) ** 2) + ((enemyy - bullety) ** 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((0, 0, 0))  # to set background colour
    screen.blit(background, (0, 0))  # to add background image
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # if keystroke is pressed check whether left or right
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerx_change = -6
            if event.key == pg.K_RIGHT:
                playerx_change = 6
            if event.key == pg.K_SPACE:
                if bulletstate == 'ready':
                    bulletsound = mixer.Sound('laser.wav')
                    bulletsound.play()
                    bulletx = playerx
                    firebullet(bulletx, bullety)

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerx_change = 0

    playerx += playerx_change  # to keep moving the player based on control
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # enemy movement
    for i in range(numenemies):
        # game over
        if enemyy[i] > 440:
            for j in range(numenemies):
                enemyy[j] = 2000
            gameover()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 5
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -5
            enemyy[i] += enemyy_change[i]

        # to check for collision
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosionsound = mixer.Sound('explosion.wav')
            explosionsound.play()
            bullety = 480
            bulletstate = 'ready'
            scoreval += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 200)

        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety <= 0:
        bullety = 480  # to shoot multiple bullets
        bulletstate = 'ready'
    if bulletstate == 'fire':
        firebullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    showscore(textx, texty)
    pg.display.update()  # to update your screen