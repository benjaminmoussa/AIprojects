# bustersAgents.py
# ----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference

class BustersAgent:
  "An agent that tracks and displays its beliefs about ghost positions."
  
  def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None ):
    inferenceType = util.lookup(inference, globals())
    self.inferenceModules = [inferenceType(a) for a in ghostAgents]
    
  def registerInitialState(self, gameState):
    "Initializes beliefs and inference modules"
    import __main__
    self.display = __main__._display
    for inference in self.inferenceModules: inference.initialize(gameState)
    self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
    self.firstMove = True
    
  def observationFunction(self, gameState):
    "Removes the ghost states from the gameState"
    agents = gameState.data.agentStates
    gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
    return gameState

  def getAction(self, gameState):
    "Updates beliefs, then chooses an action based on updated beliefs."
    for index, inf in enumerate(self.inferenceModules):
      if not self.firstMove: inf.elapseTime(gameState)
      self.firstMove = False
      inf.observeState(gameState)
      self.ghostBeliefs[index] = inf.getBeliefDistribution()
    self.display.updateDistributions(self.ghostBeliefs)
    return self.chooseAction(gameState)

  def chooseAction(self, gameState):
    "By default, a BustersAgent just stops.  This should be overridden."
    return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
  "An agent controlled by the keyboard that displays beliefs about ghost positions."
  
  def __init__(self, index = 0, inference = "ExactInference", ghostAgents = None):
    KeyboardAgent.__init__(self, index)
    BustersAgent.__init__(self, index, inference, ghostAgents)
    
  def getAction(self, gameState):
    return BustersAgent.getAction(self, gameState)
    
  def chooseAction(self, gameState):
    return KeyboardAgent.getAction(self, gameState)

from distanceCalculator import Distancer
from game import Actions
from game import Directions

class GreedyBustersAgent(BustersAgent):
  "An agent that charges the closest ghost."
  
  def registerInitialState(self, gameState):
    "Pre-computes the distance between every two points."
    BustersAgent.registerInitialState(self, gameState)
    self.distancer = Distancer(gameState.data.layout, False)
    
  def chooseAction(self, gameState):
    """
    First computes the most likely position of each ghost that 
    has not yet been captured, then chooses an action that brings 
    Pacman closer to the closest ghost (in maze distance!).
    
    To find the maze distance between any two positions, use:
    self.distancer.getDistance(pos1, pos2)
    
    To find the successor position of a position after an action:
    successorPosition = Actions.getSuccessor(position, action)
    
    livingGhostPositionDistributions, defined below, is a list of
    util.Counter objects equal to the position belief distributions
    for each of the ghosts that are still alive.  It is defined based
    on (these are implementation details about which you need not be
    concerned):

      1) gameState.getLivingGhosts(), a list of booleans, one for each
         agent, indicating whether or not the agent is alive.  Note
         that pacman is always agent 0, so the ghosts are agents 1,
         onwards (just as before).

      2) self.ghostBeliefs, the list of belief distributions for each
         of the ghosts (including ghosts that are not alive).  The
         indices into this list should be 1 less than indices into the
         gameState.getLivingGhosts() list.
     
    """
    import operator
    
    livingGhosts = gameState.getLivingGhosts()
    
    pacmanPosition = gameState.getPacmanPosition()
    legal = [a for a in gameState.getLegalPacmanActions()]
    livingGhosts = gameState.getLivingGhosts()
    livingGhostPositionDistributions = [beliefs for i,beliefs
                                        in enumerate(self.ghostBeliefs)
                                        if livingGhosts[i+1]]
    "*** YOUR CODE HERE ***"
    #self.distancer.getDistance(pos1, pos2)
    #gameState.getLivingGhosts()
    #self.ghostBeliefs
    #step1, look at distributions and get most likely ghost position for each ghost
    ghostlist = []
    #create list of list that for each index is distance(from pacman), location
    #so that later we can easily find the shortest distance which is thus the closest ghost
    for x in livingGhostPositionDistributions:
        #intialize mostlikely  position, distance, and prob variables, will update as you iterate through distribution
        pos = 0
        prob = 0
        dis = 0
        #dis is the distance from pacman's current position to the ghosts most likely position
        for key, value in x.items():
            if value > prob:
                #prob of this location is higher than the latest greatest prob of a location found before
                pos = key
                #because this is the highest prob we have seen so far, so update highest prob location to the key which is the location
                prob = value
                #update highest probability seen so far
                dis = self.distancer.getDistance(key, pacmanPosition)
                #update the most likely distance aka the distance between pacman's current position and the current most likely location which is the key
        ghostlist.append((dis, pos))
    #sort ghost positions by smallest distance
    #ghostlist.sort(key=lambda x: x[0])
    #print(ghostlist)
    
    ghostlist.sort(key=lambda x: x[0])
    #closest location is in the first index of the 2d list, then the 2nd index of that inner list
    closest = ghostlist[0][1]
    #print(ghostlist)
    #print(closest)
    #get next pacman move, that brings you closest to the ghost
    moves = []
    #do something similar to above. Make list of moves [dist to closest ghost location, move]
    for x in legal:
        #print(x in legal)
        #print(x)
        if x != "Stop":
            #new position given current location and move
            newpos = Actions.getSuccessor(pacmanPosition, x)
            #print(newpos)
            #distance of new position and the closest ghost
            dist = self.distancer.getDistance(closest, newpos)
            #print(dist)
            #print(dist)
            #print(moves)
            moves.append((dist, x))
            #print(moves)
    #sort based on first index
    #moves.sort(key=lambda x: x[0])
    #print("meow")
    #print(moves)
    #sorted(moves, key=operator.itemgetter(0))
    moves.sort(key=lambda x: x[0])
    #lowest distance move is the first index
    #print(moves)
    newmove = moves[0][1]
    #print(newmove)
    return newmove
