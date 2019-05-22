from MineSweeperEnvironment import *
from MineSweeperTile import *
from MineSweeperAgent import *
import sys



env = MineSweeperEnv(9,9,8) #(YSize, XSize, #Mines)
agent = MineSweeperAgent()
agent.setEnvironmentToPlayWith(env)

print("\nHere is the initial state of the game:")
env.printEnvironment(env.map)
yPos, xPos = input("\nEnter two numbers for y and x axis respectively with a space, the agent will do the rest: ").split()
y = int(yPos)
x = int(xPos)
if __name__ == '__main__':
    agent.startPlaying(int(y),int(x))
    # while i < agent.goal:
    #     y, x = input("\nEnter two numbers for y and x axis respectively with a space: ").split()
    #     print("You have chosen y: " + y + " and x: " + x)
    #     agent.playInEnv(int(y),int(x))
    #     agent.printPerception(agent.kb.map)