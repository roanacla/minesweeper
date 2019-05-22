
from XYEnvironment import *
from MineSweeperTile import *
from MineSweeperEnvironment import *

class AgentKB(XYEnvironment):

    def __init__(self, numOfRows, numOfColumns):
        super(AgentKB, self).__init__(numOfRows, numOfColumns)
        self.map = self.__generateEmptyTiles()
        self.costOfSearch = 0
        self.searchVisited = []
        self.nextPlays = []
        self.analyzed = []
        self.safeTiles = []

    ''' PUBLIC FUNCTIONS '''

    def tell(self, newVisibleTiles):
        if not newVisibleTiles:
            return
        self.__storeTilesInGraph(newVisibleTiles)

    def askNumOfHiddenNeighborTiles(self, y, x):
        neighbors = self.getObjectsOfNeighborsAt(y,x)
        result = 0
        for neighbor in neighbors:
            if neighbor.isVisible is False or neighbor.hasFlag is True:
                result += 1
        return result

    def getNeighborTilesWithFlags(self,y,x):
        neighbors = self.getObjectsOfNeighborsAt(y, x)
        result = []
        for neighbor in neighbors:
            if neighbor.hasFlag:
                result.append(neighbor)
        return result



    def getClosestTileWithNum(self, y, x): #Depth First Search with memory
        current = self.map[y][x]
        if current.refNumber > 0 and current not in self.analyzed:
            return (current.y, current.x)
        else:
            self.searchVisited.append(current)
            neighbors = self.getObjectsOfNeighborsAt(y,x)
            neighborsToVisit = []
            for neighbor in neighbors:
                if neighbor not in self.searchVisited:
                    neighborsToVisit.append(neighbor)
            if neighborsToVisit:
                for neighbor in neighborsToVisit:
                    if neighbor.refNumber > 0:
                        return (neighbor.y, neighbor.x)
                    else:
                        self.searchVisited.append(neighbor)
                for neighbor in neighborsToVisit:
                    y = neighbor.y
                    x = neighbor.x
                    if not self.__areAllOfItsNeighborsVisited(y,x):
                        return self.getClosestTileWithNum(y, x)

    def getSafeNextPlay(self, y,x):
        mineSweeperTile = self.map[y][x]
        hiddenTiles = self.getHiddenTiles(y, x)
        tilesWithFlags = self.getNeighborTilesWithFlags(y,x)
        realRefNumber = mineSweeperTile.refNumber - len(tilesWithFlags)
        if realRefNumber is 0:
            return hiddenTiles

    ''' PRIVATE FUNCTIONS '''
    def __generateEmptyTiles(self):
        result = []
        for row in range(self.numOfRows):
            rows = []
            for col in range(self.numOfColumns):
                mineSquare = MineSweeperTile()
                mineSquare.setPos(row, col)
                rows.append(mineSquare)
            result.append(rows)
        return result

    def __areAllOfItsNeighborsVisited(self, y, x):
        neighbors = self.getObjectsOfNeighborsAt(y,x)
        for neighbor in neighbors:
            if neighbor not in self.searchVisited:
                return False
        return True

    def markAsMine(self, y, x):
        mineSweeperTile = self.map[y][x]
        mineSweeperTile.hasAMine = True
        mineSweeperTile.hasFlag = True
        mineSweeperTile.isVisible = True

    def __storeTilesInGraph(self, listOfNewTiles):
        for tile in listOfNewTiles:
            self.map[tile.y][tile.x] = tile

    def getHiddenTiles(self, y, x):
        neighbors = self.getObjectsOfNeighborsAt(y,x)
        result = []
        for neighbor in neighbors:
            if not neighbor.isVisible:
                result.append(neighbor)
        return result