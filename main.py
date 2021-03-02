import pygame
import platform
import enemiesClass
from random import seed

# init pygame
pygame.init()

screenX = 800
screenY = 600
#create the screen
screen = pygame.display.set_mode((screenX,screenY))

#set icon
icon = pygame.image.load('rkt.png')
pygame.display.set_icon(icon)

#set Title
pygame.display.set_caption("Rocketeers")



#Player info
playerImgRight = pygame.image.load('player.png')
playerImgLeft = pygame.transform.flip(playerImgRight,True,False)
playerFacing= 0# 0 = right, 1 = left
playerWidth = 64
playerHeight = 60
playerX = 0
playerY = 0
playerDX = 0
playerDY = 0
playerInAir = True
toggleJetpackTimer = 0
jetpackOn = False

#game system info
gameTimer = 0
level = 1
seed(1)#set random seed

#enemyInfoi
enemyMoveX=.5
enemyMoveY=.075

#debug info
font = pygame.font.SysFont(None,24)


#player graphics logic
def drawPlayer(x,y):
    
    screen.blit(playerImgRight,(x,y)) if playerFacing == 1 else screen.blit(playerImgLeft,(x,y))

platformImg = pygame.image.load('platform.png')
platforms = []
def generatePlatforms():
    platforms.clear()
    platforms.append(platform.Platform(0,570,800))
    platforms.append(platform.Platform(160,300,160))
    platforms.append(platform.Platform(560,200,160))


#Platform graphics logic
def drawPlatforms():
    for plat in platforms:
        platX = plat.X
        while(platX<plat.X+plat.width):
            f"{platX},{plat.Y}"
            screen.blit(platformImg,(platX,plat.Y))
            platX += 20

enemies = []
def generateEnemy():
    enemies.append(enemiesClass.Enemy(level,screenX,screenY))


def drawEnemies():
    for e in enemies:
        screen.blit(e.image,(e.X,e.Y))

def enemyCollidePlatform(enemy:enemiesClass.Enemy,plat:platform.Platform) -> bool:
    #only check collision with top of platforms
    if enemy.X < plat.X+plat.width and enemy.X+enemy.width > plat.X: #enemy above platform
        if enemy.Y+enemy.height > plat.Y and enemy.Y < plat.Y:
            return True
    return False

    
    


#logic for player falling and being on ground or platform
def playerOnGround():
    global playerDY
    playerBottom = playerY + playerHeight
    playerRight = playerX + playerWidth
    for plat in platforms:
        if playerIsAboveBelow(plat):
              if playerBottom + playerDY >= plat.Y and playerY < plat.Y:
                  playerDY = 0

#logic for player being in air jetpack on and colliding with platform
def playerBumpsHead():
    global playerDY
    playerRight = playerX + playerWidth
    for plat in platforms:
        platY = plat.Y + plat.height
        if playerIsAboveBelow(plat) : # player is within platform left-right
            if playerY > plat.Y  and playerY + playerDY < plat.Y + plat.height: #player is below platform about to intersect
                playerDY = 0 

#TODO: game is counting collision when player is on left side of platform, even far from it
#possibly needs some kind of distance check
def playerHitsWallGoingLeft():
    global playerDX
    playerBottom = playerY + playerHeight
    for plat in platforms:
        if playerIsNextTo(plat): 
            if playerX + playerDX < plat.X + plat.width and playerX > plat.X:
                playerDX = 0

def playerHitsWallGoingRight():
    global playerDX
    playerRight = playerX + playerWidth
    playerBottom = playerY + playerHeight
    for plat in platforms:
        if playerIsNextTo(plat): #check if player is next to platform
            if playerRight + playerDX > plat.X and playerRight < plat.X + plat.width:
                playerDX = 0

def playerIsNextTo(plat: platform.Platform):
    return playerY < plat.Y + plat.height and playerY + playerHeight > plat.Y 

def playerIsAboveBelow(plat: platform.Platform):
    playerRight = playerX + playerWidth
    return playerX < plat.X+plat.width and playerRight > plat.X
#    return ( plat.X + plat.width > playerX > plat.X ) or ( plat.X < playerRight < plat.X + plat.width )



def drawDebugText():
    img = font.render(f"{gameTimer}",True,pygame.Color(0,0,255))
    screen.blit(img,(20,20))
#timer debug display



generatePlatforms()
#Game Loop
running = True
while running:
    gameTimer+=1


    #event section
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    playerDX = 0
    playerDY = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: #set left momentum
        playerFacing = 0
        playerDX = -1
    if keys[pygame.K_d]: # set right momentum
        playerDX = 1
        playerFacing = 1

    if toggleJetpackTimer == 0:
        if keys[pygame.K_w]: # toggle jetpack
            jetpackOn = not jetpackOn
            toggleJetpackTimer = 120
    else:
        toggleJetpackTimer -= 1
        
    if jetpackOn:
        playerDY = -0.5
        playerBumpsHead()# checks vertical collision
    else:
        playerDY = 0.5
        playerOnGround()# checks collision with ground
    
    playerHitsWallGoingRight() if playerDX>0 else playerHitsWallGoingLeft()


    #enemy section
    
    cleanUpDead = []
    for enemy in enemies:
        if enemy.dead==True:
            enemy.animateDeath()
            if enemy.remove:
                cleanUpDead.append(enemy)

        else:

            enemy.X+=enemy.direction*enemyMoveX
            if enemy.X > screenX:
                enemy.X = -50
            if enemy.X < -50:
                enemy.X = screenX
            enemy.Y+=enemyMoveY
            for plat in platforms:
                if enemyCollidePlatform(enemy,plat):
                    enemy.dead=True

    if gameTimer %200 == 0:
        #generate and clean up enemies
        for enemy in cleanUpDead:
            enemies.remove(enemy)
        if len(enemies) < 7 + level:
            generateEnemy()
        #TODO: player collision / death & animation
        #TODO: platform collision and death of enemy
        #TODO: bullet collision and death of enemy plus score






    #TODO: update playerX, playerY to be modified by accelerators rather than velocity modifiers
    playerX += playerDX
    playerY += playerDY

    if playerX < -30:
        playerX = screenX
    if playerX > screenX:
        playerX = -30
    if playerY < 0: # fall off bottom?
        playerY = 0

    
    #graphics section

    # background color
    screen.fill((0,0,0))

    drawPlayer(playerX,playerY)

    drawPlatforms()

    drawDebugText()

    drawEnemies()


    pygame.display.update()

