from XYEnvironment import *
from MineSweeperTile import *
from MineSweeperEnvironment import *
from MineSweeperAgentKB import *

class MineSweeperAgent:

    def __init__(self):
        self.movesNumber = 0
        self.goal = 0
        self.startY = 0
        self.startX = 0
        self.newVisibleTiles = []

    def startPlaying(self, y, x):
        i = 0
        typeOfReasoning = 0
        while i < self.goal:
            self.playInEnv(int(y), int(x), typeOfReasoning)
            pos = self.kb.getClosestTileWithNum(y, x)
            if pos is None:
                typeOfReasoning += 1
                if typeOfReasoning == 2:
                    self.kb.analyzed = []
                    self.kb.searchVisited = []
                    typeOfReasoning = 0
                    y = 0
                    x = 0
                self.printPerception(self.kb.map)
                self.verifyGameState()
                enter = input("\nPress enter to continue: ")
                if typeOfReasoning == 0:
                    print("Use reasoning to mark all possible Tiles")
                if typeOfReasoning == 1:
                    print("Use reasoning to reveal all safe Tiles")
            else:
                y = pos[0]
                x = pos[1]

    def setEnvironmentToPlayWith(self, mineSweeperEnv):
        self.environment = mineSweeperEnv
        self.goal = mineSweeperEnv.getNumOfMines()  # The number of mines to look for
        size = mineSweeperEnv.getSizeOfEnvironment()  # returns Tuple (numOfRows, numOfColumns)
        self.kb = AgentKB(size[0], size[1])

    def getNextMove(self, posY, posX):
        nextMove = self.kb.getClosestTileWithNum(posY,posX)
        return nextMove

    def revealSafeTiles(self):
        for tile in self.kb.analyzed:
            nextPlays = self.kb.getSafeNextPlay(tile.y, tile.x)
            if nextPlays is not None and nextPlays:
                for nextPlay in nextPlays:
                    self.playInEnv(nextPlay.y, nextPlay.x, 0)

    def markMinesWithFlags(self, y, x): #REASONING 1
        mineSweeperTile = self.kb.map[y][x]
        if mineSweeperTile.refNumber is not 0:
            numOfHiddenTiles = self.kb.askNumOfHiddenNeighborTiles(y, x)
            if mineSweeperTile.refNumber == numOfHiddenTiles:
                hiddenTiles = self.kb.getHiddenTiles(y, x)
                for hidden in hiddenTiles:
                    self.kb.markAsMine(hidden.y, hidden.x)
                    # self.__reduceNeighborsByOne(hidden.y, hidden.x)

    def playInEnv(self, posY, posX, typeOfReasoning):
        if typeOfReasoning is 0:
            self.markMinesWithFlags(posY, posX)
        if typeOfReasoning is 1:
            self.revealSafeTiles()

        if self.movesNumber is 0:
            self.newVisibleTiles = self.environment.firstMove(posY, posX)
            self.movesNumber += 1
        else:
            self.newVisibleTiles = self.environment.nextMove(posY, posX)

        self.kb.tell(self.newVisibleTiles)
        tile = self.kb.getObjectAt(posY,posX)
        self.kb.analyzed.append(tile)

    def verifyGameState(self):
        if len(self.newVisibleTiles) is not 0 and self.newVisibleTiles[0].hasAMine is True:
            print("\n#############################\nI'M THE AGENT AND I LOST :(\n#############################")
        if self.environment.getNumOfHiddenTiles() is self.environment.numOfMines:
            print("\n###########################\nI'M THE AGENT AND I WON!!!\n###########################")

    # def __searchNextPos(self):

    def printPerception(self, newVisibleTiles):
        self.environment.printEnvironment(self.kb.map)