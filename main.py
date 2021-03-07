
import pygame
import platform
import enemiesClass
import blasterBullet
from random import seed

#TODO LIST:
#
#1. create Title screen to explain rules
#2. create objective -- fill ship with fuel!
#OR
#set level increase to go based on time survived
#OR
#idea workshop -- what is objective?
#
#3. add score pickups
#
#4. add powerups
#
#5. add new enemies for higher levels
#
#6. add multiple lives
#
#


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

#text and color info
font = pygame.font.SysFont("Uroob",24)
gameOverFont = pygame.font.SysFont("Uroob",64,True)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)

#Player info
playerImgRight = pygame.image.load('newplayer.png')
playerImgLeft = pygame.transform.flip(playerImgRight,True,False)
playerFacing= 0# 0 = right, 1 = left
playerWidth = 64
playerHeight = 60
playerX = screenX*.3
playerY = 20
playerDX = 0
playerDY = 0
playerInAir = True
toggleJetpackTimer = 0
jetpackOn = False
bulletColor = RED
blasterTimer=0
playerHealth = 3
#TODO:multiple lives?
playerLives = 3
gameOver = False
gameOverTimer=0
playerImgDead1Right = pygame.image.load('newplayerDead1.png')
playerImgDead1Left = pygame.transform.flip(playerImgDead1Right,True,False)
playerImgDead2Right = pygame.image.load('newplayerDead2.png')
playerImgDead2Left = pygame.transform.flip(playerImgDead2Right,True,False)
playerImgDead3Right = pygame.image.load('newplayerDead3.png')
playerImgDead3Left = pygame.transform.flip(playerImgDead3Right,True,False)
playerImgDead4Right = pygame.image.load('newplayerDead4.png')
playerImgDead4Left = pygame.transform.flip(playerImgDead4Right,True,False)

#game system info
gameTimer = 0
gameScore = 0
level = 1
seed(1)#set random seed




#player graphics logic
def drawPlayer(x,y):
    screen.blit(playerImgRight,(x,y)) if playerFacing == 1 else screen.blit(playerImgLeft,(x,y))

def drawGameOver(x,y):
    global gameTimer
    global gameOverTimer
    global playerX
    diff = gameTimer - gameOverTimer
    if diff<60:
        #draw dead1
        screen.blit(playerImgDead1Right,(x,y)) if playerFacing == 1 else screen.blit(playerImgDead1Left,(x,y))
    elif diff <120:
        #draw dead2
        screen.blit(playerImgDead2Right,(x,y)) if playerFacing == 1 else screen.blit(playerImgDead2Left,(x,y))
    elif diff< 180:
        #draw dead3
        screen.blit(playerImgDead3Right,(x,y)) if playerFacing == 1 else screen.blit(playerImgDead3Left,(x,y))
    elif diff < 240:
        #draw dead4
        screen.blit(playerImgDead4Right,(x,y)) if playerFacing == 1 else screen.blit(playerImgDead4Left,(x,y))
    else:
        img = gameOverFont.render("GAME OVER",True,RED)
        playerX = -300
        screen.blit(img,(screenX*.35,screenY*.2))
        scoreImg = font.render("Final Score:",True,BLUE)
        screen.blit(scoreImg,(screenX*.4,screenY*.3))
        scoreVal = font.render(f"{gameScore}",True,GREEN)
        screen.blit(scoreVal,(screenX*.4,screenY*.3+30))
        resetImg = font.render("Press 'r' to play again",True,RED)
        screen.blit(resetImg,(screenX*.4,screenY*.75))
        #draw game over text
        #GAME OVER
        #Final Score:
        #TODO: hi-score board
        #press r to restart
        #TODO: resetGame()

#TODO: draw player health bar
def drawPlayerHealth():
    img = font.render("Shields:",True,pygame.Color(0,0,255))
    screen.blit(img,(230,10))
    color=(255,0,0)
    if playerHealth == 3:
        color = (0,255,0)
    elif playerHealth == 2:
        color = (255,255,0)
    elif playerHealth == 1:
        color = (255,0,0)
    if playerHealth > 0:
        for i in range(3):
            if i < playerHealth:
                pygame.draw.rect(screen,color,(300+(i*50),10,30,10),True)
            else:
                pygame.draw.rect(screen,(127,127,127),(300+(i*50),10,30,10),False)
    else:
        if gameTimer%160 > 100 and gameOver == False:
            img = font.render("Critical",True,pygame.Color(225,0,30))
            screen.blit(img,(300,10))

def drawJetpackIndicator():
    img = font.render("Jetpack:",True,pygame.Color(255,255,255))
    screen.blit(img,(screenX*.6,10))
    if jetpackOn:
        img = font.render("On",True,pygame.Color(0,225,0))
    else:
        img = font.render("Off", True, pygame.Color(225,10,0))
    screen.blit(img,(screenX*.6+70,10))

def playerHurt():
    global playerHealth
    global gameOver
    global gameOverTimer
    global gameTimer
    if playerHealth > 0:
        playerHealth -= 1
    else:
        gameOver = True
        gameOverTimer = gameTimer
        print("set gameover")



platformImg = pygame.image.load('platform.png')
platforms = []
def generatePlatforms():
    platforms.clear()
    platforms.append(platform.Platform(-40,screenY-30,screenX + 80))
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

#TODO: logic to check collision with player hitbox
def enemyCollidePlayer(enemy:enemiesClass.Enemy) -> bool:
    #just going to check all four corners for collision
    playerRight = playerX+playerWidth
    playerBottom = playerY + playerHeight
    if (
            (playerX<enemy.X<playerRight and playerY<enemy.Y<playerBottom) or \
            (playerX<enemy.X+enemy.width<playerRight and playerY<enemy.Y<playerBottom) or \
            (playerX<enemy.X+enemy.width<playerRight) and playerY<enemy.Y+enemy.height<playerBottom) or \
            (playerX<enemy.X<playerRight and playerY<enemy.Y+enemy.height<playerBottom
        ):
        return True
    else:
        return False

def enemyCollideBullet(enemy:enemiesClass.Enemy, bullet:blasterBullet.blasterBullet) -> bool:
    return enemy.X < bullet.x < enemy.X+enemy.width and enemy.Y < bullet.y < enemy.Y+enemy.height

    
bullets = []
def drawBlasterBullets():
    secondColor = bulletColor + pygame.Color(0,122,88,0)
    thirdColor = secondColor + pygame.Color(155,0,155,0)
    for bul in bullets:
        pygame.draw.line(screen,thirdColor,(bul.x,bul.y),(bul.x+bul.tail_dir,bul.y))
        pygame.draw.line(screen,secondColor,(bul.x+(bul.tail_dir*1.2),bul.y),(bul.x+(bul.tail_dir*2.5),bul.y))
        pygame.draw.line(screen,bulletColor,(bul.x+(bul.tail_dir*2.7),bul.y),(bul.x+(bul.tail_dir*3.8),bul.y))

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

def increaseScore(amount: int):
    global gameScore
    gameScore += amount

def drawDebugText():
    img = font.render(f"{gameTimer}",True,pygame.Color(0,0,255))
    screen.blit(img,(20,10))
#timer debug display

def drawScoreText():
    img = font.render(f"Score: {gameScore}",True,pygame.Color(255,0,67))
    screen.blit(img,(screenX - screenX/6,10))

#TODO:title screen and game-start
#restart game method returns all global variables to initial state to start anew
def restartGame():
    global level,gameScore,gameTimer,gameOver,gameOverTimer,playerX,playerY,playerInAir
    global toggleJetpackTimer,playerHealth,blasterTimer,jetpackOn
    global enemies
    global bullets
    level = 1
    gameScore = 0
    gameTimer = 0
    gameOver = False
    gameOverTimer=0
    playerX = screenX*.3
    playerY = 20
    playerInAir = True
    toggleJetpackTimer = 0
    jetpackOn = False
    playerHealth=3
    blasterTimer=0
    enemies.clear()    
    bullets.clear()



generatePlatforms()
#Game Loop
running = True
while running:

    if gameOver:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            restartGame()
            pass

    #event section
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gameTimer+=1
    if not gameOver:
        #TODO: move this within subroutine for player input
        #INPUT: key/movement/shooting section
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
        
        if blasterTimer == 0:
            if keys[pygame.K_RCTRL]:
                if playerFacing == 0:
                    bullets.append(blasterBullet.blasterBullet(playerX,playerY+25,-1))
                else:
                    bullets.append(blasterBullet.blasterBullet(playerX+playerWidth,playerY+25,1))
                blasterTimer=90
        else:
            blasterTimer-=1

        if jetpackOn:
            playerDY = -0.5
            playerBumpsHead()# checks vertical collisions
        else:
            playerDY = 0.5
            playerOnGround()# checks collision with ground
        
        playerHitsWallGoingRight() if playerDX>0 else playerHitsWallGoingLeft()


    deadBullets = []
    #move bullet section
    for bul in bullets:
        bul.x += bul.dir*1.8
        if bul.x > screenX:
            bul.x = -10
        if bul.x <-10:
            bul.x = screenX+10
        bul.traveled +=1.8
        if bul.traveled > screenX*.75:
            deadBullets.append(bul)
        else:
            for plat in platforms:
                if plat.X < bul.x < plat.X+plat.width and plat.Y < bul.y < plat.Y+plat.height:
                    deadBullets.append(bul)
        #bullet collision with platforms
        #final way bullets die is below, colliding with enemies


    #enemy section
    
    cleanUpDead = []
    for enemy in enemies:
        if enemy.dead==True:
            enemy.animateDeath()
            if enemy.remove:
                cleanUpDead.append(enemy)

        else:
            #TODO: move this movement logic within enemy so it can be different based on level
            enemy.move()
            if enemy.X > screenX:
                enemy.X = -50
            if enemy.X < -50:
                enemy.X = screenX
            for plat in platforms:
                if enemyCollidePlatform(enemy,plat):
                    enemy.dead=True
            for bul in bullets:
                if enemyCollideBullet(enemy,bul):
                    increaseScore(level * 100)
                    enemy.dead=True
                    deadBullets.append(bul)
            #TODO: bullet collision and death of enemy plus score
            if enemyCollidePlayer(enemy):
                playerHurt()
                enemy.dead=True
            #TODO:collide with player, begin player death sequence


    if gameTimer %200 == 0:
        #generate and clean up enemies
        for enemy in cleanUpDead:
            enemies.remove(enemy)
        if len(enemies) < 7 + level:
            generateEnemy()

    #TODO: player death & animation

    






    #cleanup bullet section
    for bul in deadBullets:
        if bul in bullets:
            bullets.remove(bul)

    #TODO: update playerX, playerY to be modified by accelerators rather than velocity modifiers
    if not gameOver:
        #TODO: move this within subroutine movePlayer()
        playerX += playerDX
        playerY += playerDY

        if playerX < -30:
            playerX = screenX
        if playerX > screenX:
            playerX = -30
        if playerY < 30: # hits "roof"
            playerY = 30

    
    #graphics section

    # background color
    screen.fill((0,0,0))


    #draw actors
    if not gameOver:
        drawPlayer(playerX,playerY)
    else:
        drawGameOver(playerX,playerY)

    drawBlasterBullets()

    drawEnemies()
    #draw text and UI
    drawDebugText()

    drawScoreText()

    drawPlayerHealth()

    drawJetpackIndicator()
    
    drawPlatforms()


    pygame.display.update()

