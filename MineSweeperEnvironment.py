import random
from XYEnvironment import *
from MineSweeperTile import *

class MineSweeperEnv(XYEnvironment):

    ''' PUBLIC FUNCTIONS '''

    def __init__(self, numOfRows, numOfColumns, numOfMines):
        super(MineSweeperEnv, self).__init__(numOfRows, numOfColumns)
        self.numOfMines = numOfMines
        self.generateEnv()

    # Generates MineSweeperSquare acording to the size specified in the initializer.
    def generateEnv(self):
        for row in range(self.numOfRows):
            rows = []
            for col in range(self.numOfColumns):
                mineSquare = MineSweeperTile()
                mineSquare.setPos(row, col)
                rows.append(mineSquare)
            self.map.append(rows)

    def firstMove(self, startRow, startCol):
        self.__addMinesRandomlyStartingAt(startRow, startCol)
        return self.nextMove(startRow, startCol)

    def nextMove(self, startRow, startCol):
        row = startRow
        col = startCol

        newVisibleTiles = []
        self.__revealPlay(row, col, newVisibleTiles)
        return newVisibleTiles

    def printEnvironment(self, map):
        for row in range(self.numOfRows):
            #Top Numbers
            for col in range(self.numOfColumns):
                if row is 0:
                    if col is 0:
                        print("   ", end="")
                    if col > 9:
                        print(" " + str(col), end=" ")
                    else:
                        print("  " + str(col), end=" ")
                if col is self.numOfColumns -1 :
                    if row is 0:
                        print("")
            #Row Lines
            for col in range(self.numOfColumns):
                if col is 0:
                    print("   ", end="")
                print("|---", end="")
                if col is self.numOfColumns - 1:
                    print("|")
            #RowValues
            for col in range(self.numOfColumns):
                if col is 0:
                    if row > 9:
                        print(str(row), end=" ")
                    else:
                        print(str(row), end="  ")
                mineSweeperTile = map[row][col]
                if mineSweeperTile is not None and mineSweeperTile.isVisible is True :
                    refNumber = str(mineSweeperTile.refNumber) if mineSweeperTile.refNumber > 0 else " "
                    value = "☼" if mineSweeperTile.hasAMine is True else refNumber
                else:
                    value = "■"
                if mineSweeperTile.hasFlag is True:
                    value = "▿"
                print("| " + value + " ", end="")
                if col is self.numOfColumns - 1:
                    print("|")
            #Last Row Line
            if row == self.numOfRows - 1:
                for col in range(self.numOfColumns):
                    if col is 0:
                        print("  ", end=" ")
                    print("|---", end="")
                print("|")

    def getSizeOfEnvironment(self):
        return (self.numOfRows, self.numOfColumns)

    def getNumOfMines(self):
        return self.numOfMines

    #TODO - FIND A CHEAPEST WAY TO DO THIS.
    def getNumOfHiddenTiles(self):
        result = 0
        for row in range(self.numOfRows):
            for col in range(self.numOfColumns):
                if self.map[row][col].isVisible is False:
                    result += 1
        return result

    ''' PRIVATE FUNCTIONS '''

    def __revealPlay(self, row, col, result): #result is a in-out parameter
        neighbors = self.getObjectsOfNeighborsAt(row, col)
        current = self.getObjectAt(row, col)
        if current.isVisible is True:
            return
        if current.hasAMine is True:
            result +=  self.__revealAllMines()
            return
        if current.refNumber >= 0 and current.isVisible is False:
            current.isVisible = True
            result.append(current)
            if current.refNumber > 0:
                return
        for neighbor in neighbors:
            if neighbor is not None and neighbor not in result and neighbor.isVisible is False:
                self.__revealPlay(neighbor.y, neighbor.x, result)

    def __revealAllMines(self):
        allTilesWithMines = []
        for row in range(self.numOfRows):
            for column in range(self.numOfColumns):
                mineSweeperTile = self.map[row][column]
                if mineSweeperTile.hasAMine is True:
                    mineSweeperTile.isVisible = True
                    allTilesWithMines.append(mineSweeperTile)
        return allTilesWithMines

    def __increaseByOneTheNeighborsOf(self, rowPos,
                                      colPos):  # Once a bomb is added in the environment, the niegbors update their ref number.
        neighbors = self.getObjectsOfNeighborsAt(rowPos, colPos)
        for neighbor in neighbors:
            if neighbor is not None:
                neighbor.refNumber += 1
        # self.printEnvironment()
        # print()

    def __getListOfPositionsWhereMinesAreAllowed(self, allPositions, startingPositions):
        for obj in startingPositions:
            if obj is not None:
                allPositions.remove(obj)
        return allPositions

    def __generatePositionsToPutMines(self, startRow, startCol):
        numberOfSquares = self.numOfRows * self.numOfColumns
        allPositions = list(range(numberOfSquares))
        startingPositions = self.getMapAddressOfNeighbors(startRow, startCol)
        allPositions = self.__getListOfPositionsWhereMinesAreAllowed(allPositions, startingPositions)
        positions = random.sample(allPositions, self.numOfMines)
        return positions

    def __addMinesRandomlyStartingAt(self, startRow, startCol):
        if startRow > self.numOfRows or startCol > self.numOfColumns:
            print("Error!! - The Agent cannot start outside the environment")
            return

        positionsToPutMines = self.__generatePositionsToPutMines(startRow, startCol)
        # positionsToPutMines = [4, 7, 11, 17, 20, 21, 35, 55, 77]

        for addressInMap in positionsToPutMines:
            if self.numOfRows <= self.numOfColumns:
                rowPos = addressInMap // self.numOfColumns
                colPos = addressInMap % self.numOfColumns
            else:
                rowPos = addressInMap // self.numOfColumns
                colPos = addressInMap % self.numOfColumns

            mineObj = self.map[rowPos][colPos]
            mineObj.hasAMine = True

            self.__increaseByOneTheNeighborsOf(rowPos, colPos)