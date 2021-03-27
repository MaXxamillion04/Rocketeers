from random import randint

class PowerUp:
    def __init__(self, X:int, Y:int):
        self.X=X
        self.Y=Y
        self.type = randint(0,2)#up to 4
        self.type=2
        self.animateFrame=0
    
    def updateAnimateFrame(self):
        self.animateFrame+=1
        if self.animateFrame==100:
            self.animateFrame=0
        return self.animateFrame//50

    
