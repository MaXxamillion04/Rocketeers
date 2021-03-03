

class blasterBullet:
    def __init__(self, x_start,y_start,direction):
        #direction positive = left, negative = right
        self.x=x_start
        self.x_start=x_start
        self.y=y_start
        self.dir=direction
        self.tail_dir = (10 * direction)
        self.traveled=0

