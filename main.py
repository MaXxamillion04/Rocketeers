import pygame
import platform

# init pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#set icon
icon = pygame.image.load('rkt.png')
pygame.display.set_icon(icon)

#set Title
pygame.display.set_caption("Rocketeers")



#Player info
playerImg = pygame.image.load('player.png')
playerWidth = 64
playerHeight = 60
playerX = 0
playerY = 0
playerDX = 0
playerDY = 0
playerInAir = True
toggleJetpackTimer = 0
jetpackOn = False

#player graphics logic
def drawPlayer(x,y):
    screen.blit(playerImg,(x,y))

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


#TODO: logic for player falling and being on ground or platform
def playerOnGround():
    global playerDY
    playerBottom = playerY + playerHeight
    playerRight = playerX + playerWidth
    for plat in platforms:
        if playerIsAboveBelow(plat):
              if playerBottom + playerDY >= plat.Y and playerY < plat.Y:
                  playerDY = 0

#TODO: logic for player being in air jetpack on and colliding with platform
def playerBumpsHead():
    global playerDY
    playerRight = playerX + playerWidth
    for plat in platforms:
        platY = plat.Y + plat.height
        if playerIsAboveBelow(plat) : # player is within platform left-right
            if playerY > plat.Y  and playerY + playerDY < plat.Y + plat.height: #player is below platform about to intersect
                playerDY = 0 

def playerHitsWallGoingLeft():
    global playerDX
    playerBottom = playerY + playerHeight
    for plat in platforms:
        if playerIsNextTo(plat): 
            print("left: {playerX} + {playerDX} < {plat.X} + {plat.width} ")
            if playerX + playerDX < plat.X + plat.width:
                playerDX = 0

def playerHitsWallGoingRight():
    global playerDX
    playerRight = playerX + playerWidth
    playerBottom = playerY + playerHeight
    for plat in platforms:
        if playerIsNextTo(plat): #check if player is next to platform
            if playerRight + playerDX > plat.X:
                playerDX = 0

def playerIsNextTo(plat: platform.Platform):
    return playerY < plat.Y + plat.height and playerY + playerHeight > plat.Y 

def playerIsAboveBelow(plat: platform.Platform):
    playerRight = playerX + playerWidth
    return playerX < plat.X+plat.width and playerRight > plat.X
#    return ( plat.X + plat.width > playerX > plat.X ) or ( plat.X < playerRight < plat.X + plat.width )







generatePlatforms()

#Game Loop
running = True
while running:
    #event section
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    playerDX = 0
    playerDY = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: #set left momentum
        playerDX = -1
    if keys[pygame.K_d]: # set right momentum
        playerDX = 1
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



    #TODO: update playerX, playerY
    playerX += playerDX
    playerY += playerDY

    if playerX < -30:
        playerX = 800
    if playerX > 800:
        playerX = -30
    if playerY < 0:
        playerY = 0

    
    #graphics section

    # background color
    screen.fill((0,0,0))

    drawPlayer(playerX,playerY)

    drawPlatforms()



    pygame.display.update()

