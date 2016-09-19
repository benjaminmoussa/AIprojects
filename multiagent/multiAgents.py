# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"
    oldFood = currentGameState.getFood()
    oldgs = currentGameState.getGhostStates()
    oldpos = currentGameState.getPacmanPosition()
    oldScaredTimes = [ghostState.scaredTimer for ghostState in oldgs]
    distd = 0
    dist = 0
    ret = 0
    adlist = []
    adlist1 =[]
    aodlist = []
    aodlist1 = []
    for x in newGhostStates:
        if x.scaredTimer > 0:
            distd += manhattanDistance(x.getPosition(), newPos)
            adlist1.append(manhattanDistance(x.getPosition(), newPos))
        else:
            dist += manhattanDistance(x.getPosition(), newPos)
            adlist.append(manhattanDistance(x.getPosition(), newPos))
    dist1 = 0
    dist1d = 0
    for x in oldgs:
        if x.scaredTimer > 0:
            dist1d += manhattanDistance(x.getPosition(), oldpos)
            aodlist1.append(manhattanDistance(x.getPosition(), oldpos))
        else:
            dist1 += manhattanDistance(x.getPosition(), oldpos)
            aodlist.append(manhattanDistance(x.getPosition(), oldpos))
    minN = 1000000
    minO = 1000000
    cN = 100000
    cO = 100000
    for x in adlist:
        if x < minN:
            minN = x
    for x in aodlist:
        if x <minO:
            minO = x
    for x in adlist1:
        if x < cN:
           cN = x
    for x in aodlist1:
        if x < cN:
            cO= x
    
    
  
    fdist = 0
    k1 = oldFood.width
    k2 = oldFood.height
    k3 = newFood.width
    k4 = newFood.height
    for x in successorGameState.getCapsules():
        fdist += manhattanDistance(x, newPos)
    odist = 0
    for x in currentGameState.getCapsules():
        odist += manhattanDistance(x, oldpos)
    ofood = 0
    for x in range(0, k1):
        for y in range(0, k2):
            if oldFood[x][y]:
               ofood +=  manhattanDistance((x,y), oldpos)
    nfood = 0
    for x in range(0, k3):
        for y in range(0, k4):
            if newFood[x][y]:
                nfood += manhattanDistance((x,y), newPos)

    if dist > dist1:
        ret += 1
    if distd < dist1d:
        ret += 1
    if ofood > nfood:
        ret += 2
    if odist > fdist:
        ret += 1
    if cO > cN:
        ret += 2
    
    if minN > minO:
        ret += 4
    ret += successorGameState.getScore() - currentGameState.getScore()

    
    return ret

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)


class Node(object):
  def __init__(self, object):
    self.direction = object
    self.index = None
    self.parent = None
    self.score = 0
    self.depth = 0
    self.state = None
    self.c1 = None
    self.c2 = None
    self.c3 = None
    self.c4 = None










class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def recurse(self, ghost, gameState, depth):
    from game import Directions
    from util import Queue
    from util import Stack
    place = Queue()
    place1 = Stack()
    root = Node("start")
    place.push(root)
    place1.push(root)
    root.state = gameState
    state = root.state
    while True:
        root = place.pop()
        if root.index == 0:  #ghosts
            state = root.state
            for z in state.getLegalActions(ghost):
                if z is not "Stop":
                    #print(z)
                    print(z, ghost)
                    tempstate1 = state.generateSuccessor(ghost, z)
                    temp1 = Node(z)
                    temp1.index = ghost
                    temp1.state = tempstate1
                    temp1.depth = root.depth
                    temp1.parent = root
                    if temp1.depth == depth:
                        temp1.score = self.scoreEvaluationFunction(tempstate1)
                    #print(temp1.index, temp1.direction, temp1.score,temp1.depth, temp1.parent.direction, temp1.parent.index, temp1.parent.depth)
                    place.push(temp1)
                    place1.push(temp1)
    
        else:
            #print("meow, mix")
            if root.depth == depth:
                break
            for x in root.state.getLegalActions(0):
                if x is not "Stop":
                    temp = Node(x)
                    temp.index = 0
                    temp.parent = root
                    if root.depth == 0:
                        temp.depth = 1
                    else:
                        temp.depth = root.depth +1
                    temp.state = root.state.generateSuccessor(0, x)
                    #print("meow, mix")
                    place.push(temp)
                    place1.push(temp)
    root = None
    oldpar = None
    score = None
    bscore = []
    score1 =[]
    while True:
        root = place1.pop()
        #print(root.index, root.direction, root.score,root.depth)
        if root.parent is None:
            break
        if oldpar is None:
            oldpar = root.parent
        if root.index != 0:
            if root.parent is oldpar:
                if root.score != 0:
                    score1.append(root.score)
                    #score = root.score
                    oldpar.score = min(score1)
            else:
                del score1[:]
                oldpar = root.parent
                score1.append(root.score)
                oldpar.score = min(score1)
        else:
            if root.parent is oldpar:
                if root.score != 0:
                    bscore.append(root.score)
                    oldpar.score = max(bscore)
            else:
                del bscore[:]
                oldpar = root.parent
                bscore.append(root.score)
                oldpar.score = max(bscore)
    return root.score
        
  def getAction(self, gameState):
    """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        
        Here are some method calls that might be useful when implementing minimax.
        
        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
        
        Directions.STOP:
        The stop direction, which is always legal
        
        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
        
        gameState.getNumAgents():
        Returns the total number of agents in the game
        """
    "*** YOUR CODE HERE ***"
    from game import Directions
    from util import Stack
    place = Stack()
    lastagent = gameState.getNumAgents()-1
    
    def minimaxvalue(ghost, depth, gameState):
        bmove = None
        moves = gameState.getLegalActions(ghost)
        numbmove = len(moves)
        if numbmove is 0: return self.evaluationFunction(gameState)
        score1 = None
        for x in moves:
            state = gameState.generateSuccessor(ghost, x)
            if x is not "Stop":
                if ghost != lastagent:
                    score = minimaxvalue(ghost+1, depth, state)
                    if score1 is None:
                        score1 = score
                        bmove = x
                    elif score < score1:
                        score1 = score
                        bmove = x
                else:
                    score = minimaxdecision(depth+1, state)
                    if score1 is None:
                        score1 = score
                        bmove = x
                    elif score < score1:
                        score1 = score
                        bmove = x
        place.push(bmove)
        return score1
    
    def minimaxdecision(depth, gameState):
        if depth is self.depth: return self.evaluationFunction(gameState)
        bmove = None
        moves = gameState.getLegalActions(0)
        numbmove = len(moves)
        if numbmove is 0: return self.evaluationFunction(gameState)
        score1 = None
        for x in moves:
            if x is not "Stop":
                state = gameState.generateSuccessor(0, x)
                score = minimaxvalue(1, depth, state)
                if score1 is None:
                    score1 = score
                    bmove = x
                elif score > score1:
                    score1 = score
                    bmove = x
        place.push(bmove)
        return score1
    
    s = minimaxdecision(0, gameState)
    print("meow")
    print(s)
    final = place.pop()
    print(final)
    return final

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
    Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    from util import Stack
    place = Stack()
    lastagent = gameState.getNumAgents()-1
    
    def minimaxvalue(ghost, depth, gameState, a, b):
        bmove = None
        moves = gameState.getLegalActions(ghost)
        numbmove = len(moves)
        if numbmove is 0: return self.evaluationFunction(gameState)
        score1 = None
        for x in moves:
            if a > b:
                place.push(bmove)
                return score1
            if x is not "Stop":
                state = gameState.generateSuccessor(ghost, x)
                if ghost != lastagent:
                    score = minimaxvalue(ghost+1, depth, state, a, b)
                    if score1 is None:
                        score1 = score
                        bmove = x
                        if score < b:
                            b = score
            
                    elif score < score1:
                        score1 = score
                        bmove = x
                        if score < b:
                            b = score
                else:
                    score = minimaxdecision(depth+1, state, a, b)
                    if score1 is None:
                        score1 = score
                        bmove = x
                        if score < b:
                            b = score
                    elif score < score1:
                        score1 = score
                        bmove = x
                        if score < b:
                            b = score
        
        place.push(bmove)
        return score1

    def minimaxdecision(depth, gameState, a, b):
        if depth is self.depth: return self.evaluationFunction(gameState)
        bmove = None
        moves = gameState.getLegalActions(0)
        numbmove = len(moves)
        if numbmove is 0: return self.evaluationFunction(gameState)
        score1 = None
        for x in moves:
            if a > b:
                place.push(bmove)
                return score1
            if x is not "Stop":
                state = gameState.generateSuccessor(0, x)
                score = minimaxvalue(1, depth, state, a, b)
                if score1 is None:
                    score1 = score
                    bmove = x
                    if score > a:
                        a = score
            
                elif score > score1:
                    score1 = score
                    bmove = x
                    if score > a:
                        a = score
        place.push(bmove)
        return score1
    
    s = minimaxdecision(0, gameState, -1000000, 1000000)
    print("meow")
    print(s)
    final = place.pop()
    print(final)
    return final

        

    util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    from util import Stack
    place = Stack()
    lastagent = gameState.getNumAgents()-1
    
    def minimaxvalue(ghost, depth, gameState):
        bmove = None
        moves = gameState.getLegalActions(ghost)
        numbmove = len(moves)
        if numbmove is 0: return self.evaluationFunction(gameState)
        score1 = None
        expectedval = 0
        for x in moves:
            state = gameState.generateSuccessor(ghost, x)
            if x is not "Stop":
                if ghost != lastagent:
                
                    score = minimaxvalue(ghost+1, depth, state)
                    #if score1 is None:
                    #score1 = score
                
                    #elif score < score1:
                    #score1 = score
                    #bmove = x
                    average = (score/numbmove)
                    expectedval += average
                else:
                    score = minimaxdecision(depth+1, state)
                    #if score1 is None:
                    #score1 = score
                    #bmove = x
                    #elif score < score1:
                    #score1 = score
                    bmove = x
                    average = (score/numbmove)
                    expectedval += average
    
        place.push(bmove)
        return expectedval
    
    def minimaxdecision(depth, gameState):
        if depth is self.depth: return self.evaluationFunction(gameState)
        bmove = None
        moves = gameState.getLegalActions(0)
        numbmove = len(moves)
        if numbmove is 0: return self.evaluationFunction(gameState)
        score1 = None
        for x in moves:
            if x is not "Stop":
                state = gameState.generateSuccessor(0, x)
                score = minimaxvalue(1, depth, state)
                if score1 is None:
                    score1 = score
                    bmove = x
                elif score > score1:
                    score1 = score
                    bmove = x
        place.push(bmove)
        return score1
    
    s = minimaxdecision(0, gameState)
    print("meow")
    print(s)
    final = place.pop()
    print(final)
    return final

    
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

