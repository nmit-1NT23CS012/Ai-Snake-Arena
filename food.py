import random

class Food:
    def __init__(self,width,height):
        # random position
        self.x = random.randint(0,width)
        self.y = random.randint(0,height)

    # return position
    def position(self):
        return (self.x,self.y)