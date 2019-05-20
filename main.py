from MineSweeperEnvironment import *
from MineSweeperTile import *
import sys

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

class AgentKB(XYEnvironment):

    def __init__(self, numOfRows, numOfColumns):
        super(AgentKB, self).__init__(numOfRows, numOfColumns)
        self.graph = [[None for x in range(env.numOfColumns)] for y in range(env.numOfRows)]

    def tell(self, newVisibleTiles):
        self.__storeTilesInGraph(newVisibleTiles)

    def __generateTreeStartingWith(self, mineSweeperTile):
        y = mineSweeperTile.pos[0]
        x = mineSweeperTile.pos[1]
        neighbors = self.getObjectsOfNeighborsAt(y,x)
        treeHead = Node(mineSweeperTile)
        for neighbor in neighbors:
            treeHead.add_child(neighbor)
        # for row in self.numOfRows:
            # for col in self.numOfColumns:


    def ask(self):
        print("Ask function")

    def __storeTilesInGraph(self, listOfNewTiles):
        for tile in listOfNewTiles:
            pos = tile.pos
            self.graph[pos[0]][pos[1]] = tile

class MineSweeperAgent:

    def __init__(self):
        self.movesNumber = 0
        self.goal = 0

    def setEnvironmentToPlayWith(self, mineSweeperEnv):
        self.environment = mineSweeperEnv
        self.goal = mineSweeperEnv.getNumOfMines()  # The number of mines to look for
        size = mineSweeperEnv.getSizeOfEnvironment()  # returns Tuple (numOfRows, numOfColumns)
        self.kb = AgentKB(size[0], size[1])

    def playInEnv(self, posY, posX):
        print("Agent's eyes after move: row = " + str(posY) + ", col = " + str(posX))
        if self.movesNumber is 0:
            newVisibleTiles = self.environment.firstMove(posY, posY)
            self.movesNumber += 1
        else:
            newVisibleTiles = self.environment.nextMove(posY,posX)


        self.kb.tell(newVisibleTiles)
        if len(newVisibleTiles) is not 0 and newVisibleTiles[0].hasAMine is True:
            print("\n#############################\nI'M REALLY SORRY: YOU LOST!!!\n#############################")
        if len(self.kb.map) is self.__getEnvironmentSize() - self.goal:
            print("\n###########################\nCONGRATULATIONS: YOU WON!!!\n###########################")
        self.printPerception(self.kb.graph)


    def printPerception(self, newVisibleTiles):
        env.printEnvironment(self.kb.graph)

    def __getEnvironmentSize(self):
        return self.environment.numOfColumns * self.environment.numOfRows


env = MineSweeperEnv(9,9,10)
agent = MineSweeperAgent()
env.printEnvironment(env.map)
agent.setEnvironmentToPlayWith(env)

if __name__ == '__main__':
    i = 0
    while i < agent.goal:
        y, x = input("\nEnter two numbers for y and x axis respectively with a space: ").split()
        print("You have chosen y: " + y + " and x: " + x)
        agent.playInEnv(int(y),int(x))