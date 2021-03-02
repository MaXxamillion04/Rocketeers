
from random import randint
import pygame
class Enemy:
    def __init__(self,level,screenX,screenY):
        self.image = None
        self.X=None
        self.Y=None
        self.width=None
        self.height=None
        self.dead=False
        self.deadTimer=0
        self.remove =False
        if level == 1:
            self.spawnLevelOne(screenX,screenY)


    def spawnLevelOne(self,screenX,screenY):
        side = randint(0, 1)
        if side == 1:
            self.direction = -1
            self.X = screenX+20
        else:
            self.direction = 1
            self.X = -20

        self.Y = randint(0,screenY/2)
        self.width=60
        self.height=30
        self.image = pygame.image.load('levelOneEnemy.png')
        if self.direction > 0:
            self.image= pygame.transform.flip(self.image, True, False) 

    def animateDeath(self):
        self.deadTimer+=1
        
        if self.deadTimer > 120:
            self.image = pygame.image.load('levelOneEnemyDead4.png')
            if self.direction > 0:
                self.image = pygame.transform.flip(self.image,True,False)
            self.remove=True
        elif self.deadTimer > 80:
            self.image = pygame.image.load('levelOneEnemyDead3.png')
            if self.direction > 0:
                self.image = pygame.transform.flip(self.image,True,False)
        elif self.deadTimer> 40:
            self.image=pygame.image.load('levelOneEnemyDead2.png')
            if self.direction > 0:
                self.image = pygame.transform.flip(self.image,True,False)
        else:
            self.image=pygame.image.load('levelOneEnemyDead1.png')
            if self.direction > 0:
                self.image = pygame.transform.flip(self.image,True,False)
        



