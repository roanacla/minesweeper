import random
from XYEnvironment import *

class MineSweeperSquare:
    def __init__(self):
        self.hasAMine = False
        self.refNumber = 0
        self.isVisible = False

class MineSweeperEnv(XYEnvironment):

    def __init__(self, numOfRows, numOfColumns, numOfMines):
        super(MineSweeperEnv,self).__init__(numOfRows,numOfColumns)
        self.numOfMines = numOfMines
        self.generateEnv()

    # Generates MineSweeperSquare acording to the size specified in the initializer.
    def generateEnv(self):
        for row in range(self.numOfRows):
            rows = []
            for col in range(self.numOfColumns):
                rows.append(MineSweeperSquare())
            self.map.append(rows)

    def startPlaying(self, startRow, startCol):
        self.__addMinesRandomlyStartingAt(startRow, startCol)

    def __increaseByOneTheNeighborsOf(self, colPos, rowPos):  # Once a bomb is added in the environment, the niegbors update their ref number.
        neighbors = self.getObjectsOfNeighborsAt(colPos, rowPos)
        for neighbor in neighbors:
            if neighbor is not None:
                neighbor.refNumber += 1
        # self.printEnvironment()
        # print()

    def __removeStartingPositionsFromAllPositions(self, allPositions, startingPositions):
        for obj in startingPositions:
            if obj is not None:
                allPositions.remove(obj)
        return allPositions

    def __generatePositionsToPutMines(self, startRow, startCol):
        numberOfSquares = self.numOfRows * self.numOfColumns
        allPositions = list(range(numberOfSquares))
        startingPositions = self.getMapAddressOfNeighbors(startRow, startCol)
        allPositions = self.__removeStartingPositionsFromAllPositions(allPositions, startingPositions)
        positions = random.sample(allPositions, self.numOfMines)
        return positions

    def __addMinesRandomlyStartingAt(self, startRow, startCol):
        if startRow > self.numOfRows or startCol > self.numOfColumns:
            print("Error!! - The Agent cannot start outside the environment")
            return

        positionsToPutMines = self.__generatePositionsToPutMines(startRow, startCol)

        for addressInMap in positionsToPutMines:
            if self.numOfRows <= self.numOfColumns:
                rowPos = addressInMap // self.numOfColumns
                colPos = addressInMap % self.numOfColumns
            else:
                rowPos = addressInMap // self.numOfColumns
                colPos = addressInMap % self.numOfColumns

            mineObj = self.map[rowPos][colPos]
            mineObj.hasAMine = True

            self.__increaseByOneTheNeighborsOf(colPos, rowPos)

    def printEnvironment(self):
        for row in range(self.numOfRows):
            for col in range(self.numOfColumns):
                print("|---", end = "")
            print("|")
            for col in range(self.numOfColumns):
                obj = self.map[row][col]
                refNumber = str(obj.refNumber) if obj.refNumber > 0 else " "
                value = "M" if obj.hasAMine == True else refNumber
                print("| " + value + " ", end = "")
            print("|")
            if row == self.numOfRows - 1:
                for col in range(self.numOfColumns):
                    print("|---", end="")
                print("|")

env = MineSweeperEnv(9,9,10)
env.startPlaying(3,6)
env.printEnvironment()