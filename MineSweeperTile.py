class MineSweeperTile:
    def __init__(self):
        self.hasAMine = False
        self.refNumber = 0
        self.isVisible = False
        self.pos = (-1,-1)

    def setPos(self,row,col):
        self.pos = (row,col)