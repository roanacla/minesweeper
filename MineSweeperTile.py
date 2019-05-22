class MineSweeperTile:
    def __init__(self):
        self.hasAMine = False
        self.refNumber = 0
        self.isVisible = False
        self.y = -1
        self.x = -1
        self.hasFlag = False

    def setPos(self,row,col):
        self.y = row
        self.x = col