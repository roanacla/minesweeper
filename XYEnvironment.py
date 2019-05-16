class XYEnvironment(object):

    def __init__(self, numOfRows, numOfColumns):
        self.numOfRows = numOfRows
        self.numOfColumns = numOfColumns
        self.map = [] #hold any type of object

    def getObjectsOfNeighborsAt(self, xPos, yPos):
        x = xPos
        y = yPos
        upLeft = self.map[y - 1][x - 1] if (y - 1) >= 0 and (x - 1) >= 0 else None
        up = self.map[y - 1][x] if (y - 1) >= 0 and (x) >= 0 else None
        upRight = self.map[y - 1][x + 1] if (y - 1) >= 0 and (x + 1) < self.numOfColumns else None

        left = self.map[y][x - 1] if (y) >= 0 and (x - 1) >= 0 else None
        right = self.map[y][x + 1] if (y) >= 0 and (x + 1) < self.numOfColumns else None

        bottomLeft = self.map[y + 1][x - 1] if (y + 1) < self.numOfRows and (x - 1) >= 0 else None
        bottom = self.map[y + 1][x] if (y + 1) < self.numOfRows and (x) >= 0 else None
        bottomRight = self.map[y + 1][x + 1] if (y + 1) < self.numOfRows and (x + 1) < self.numOfColumns else None

        return [upLeft, up, upRight, left, right, bottomLeft, bottom, bottomRight]

    def getMapAddressOfNeighbors(self, startRow, startCol):
        addressInMap = (startRow - 1) * self.numOfRows + startCol - 1

        if addressInMap >= (self.numOfColumns * self.numOfRows):
            print("Error!! - map address out of boundaries")
            return None

        if self.numOfRows <= self.numOfColumns:
            rowPos = addressInMap // self.numOfColumns
            colPos = addressInMap % self.numOfColumns
        else:
            rowPos = addressInMap // self.numOfColumns
            colPos = addressInMap % self.numOfColumns

        upLeftValue = (rowPos - 1) * self.numOfColumns + colPos - 1
        upValue = (rowPos - 1) * self.numOfColumns + colPos
        upRightValue = (rowPos - 1) * self.numOfColumns + colPos + 1

        leftValue = rowPos * self.numOfColumns + colPos - 1
        rightValue = rowPos * self.numOfColumns + colPos + 1

        bottomLeftValue = (rowPos + 1) * self.numOfColumns + colPos - 1
        bottomValue = (rowPos + 1) * self.numOfColumns + colPos
        bottomRightValue = (rowPos + 1) * self.numOfColumns + colPos + 1

        upLeft = None if colPos == 0 or rowPos == 0 else upLeftValue
        up = None if rowPos == 0 else upValue
        upRight = None if colPos == self.numOfColumns - 1 or rowPos == 0 else upRightValue

        left = None if colPos == 0 else leftValue
        right = None if colPos == self.numOfColumns - 1 else rightValue

        bottomLeft = None if colPos == 0 or rowPos == self.numOfRows - 1 else bottomLeftValue
        bottom = None if rowPos == self.numOfRows - 1 else bottomValue
        bottomRight = None if rowPos == self.numOfRows - 1 or colPos == self.numOfColumns - 1 else bottomRightValue

        return [upLeft, up, upRight, left, addressInMap, right, bottomLeft, bottom, bottomRight]