# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        currentPos = currentGameState.getPacmanPosition()
        currentFood = currentGameState.getFood()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = currentFood.asList()
        minFood = 100
        minGhost = 100
        
        #find closest Ghost
        for g in newGhostStates:
            dist = manhattanDistance(newPos,g.getPosition())
            if dist == 0:
                return -2
            elif dist < minGhost:
                minGhost = dist

        if newPos in foodList and minGhost > 1:
            return 3
        
        #find closest food
        for f in foodList:
            dist = manhattanDistance(newPos, f)
            if dist < minFood:
                minFood = dist

        if minFood == 0:
            minFood = 999
            
        eval = float(1/minFood) - float(1/minGhost)

        if newPos != currentPos:
            return float(eval)
        else:
            return float(eval) - 0.5

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state
        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #To solve min nodes for ghosts
        def minValue(gameState, depth, agentIndex):
            value = 999
            
            #terminal node check
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            ghostActions = gameState.getLegalActions(agentIndex)
            
            for action in ghostActions:
                newGhost = gameState.generateSuccessor(agentIndex, action)
                
                #pacman moves after final ghost
                if agentIndex == numGhosts:
                    value = min (value, maxValue(newGhost, depth))  
                else:
                    #any ghost that isnt the last one will seek to continue minimizing
                    value = min(value,minValue(newGhost,depth,agentIndex+1))
                    
            return value
        
        #To solve max nodes for pacman
        def maxValue(gameState, depth):
            value = -999
            cDepth = depth + 1 #every pac move increases depth
            
            #terminal node check
            if gameState.isWin() or gameState.isLose() or cDepth == self.depth:
                return self.evaluationFunction(gameState)

            pacActions = gameState.getLegalActions(0)
            
            for p in pacActions:
                newPac = gameState.generateSuccessor(0, p)
                value = max (value, minValue(newPac, cDepth, 1))
                
            return value
        
        ## ACTUAL PROGRAM ##
        legalActions = gameState.getLegalActions(0)
        currentValue = -999
        actionToTake = ''
        numGhosts = gameState.getNumAgents() - 1
        
        for action in legalActions:
            newState = gameState.generateSuccessor(0, action)
            
            #Begin recursion -> pacman already moved above, so ghosts first
            value = minValue(newState, 0, 1)

            #check if new state is "better"
            if value > currentValue:
                actionToTake = action
                currentValue = value
                
        return actionToTake

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # function for max nodes
        def maxValue(gameState, depth, alpha, beta):
            value = -999
            cDepth = depth + 1

            if gameState.isWin() or gameState.isLose() or cDepth == self.depth:
                return self.evaluationFunction(gameState)
            
            actions = gameState.getLegalActions(0)
            alpha2 = alpha
            
            for action in actions:
                newPac = gameState.generateSuccessor(0, action)
                value = max (value, minValue(newPac, cDepth, 1, alpha2, beta))
                
                #snip snip
                if value > beta:
                    return value
                
                alpha2 = max(alpha2, value)
                
            return value
        
        # function for min nodes
        def minValue(gameState, depth, agentIndex, alpha, beta):
            value = 999
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            ghostActions = gameState.getLegalActions(agentIndex)
            beta2 = beta
            
            for action in ghostActions:
                newGhost = gameState.generateSuccessor(agentIndex, action)
                
                if agentIndex == numGhosts:
                    value = min (value, maxValue(newGhost, depth, alpha, beta2))
                    
                    #snip snip
                    if value < alpha:
                        return value
                    beta2 = min(beta2, value)
                else:
                    value = min(value, minValue(newGhost, depth, agentIndex + 1, alpha, beta2))
                    
                    #snip snip
                    if value < alpha:
                        return value
                    
                    beta2 = min(beta2, value)
            
            return value

        ## ACTUAL PROGRAM ##
        alpha = -999
        beta = 999
        currentValue = -999
        actionToTake = ''
        legalActions = gameState.getLegalActions(0)
        numGhosts = gameState.getNumAgents() - 1
        
        for action in legalActions:
            newState = gameState.generateSuccessor(0, action)
            score = minValue(newState, 0, 1, alpha, beta)

            if score > currentValue:
                actionToTake = action
                currentValue = score
   
            #snip snip
            if score > beta:
                return actionToTake
            
            alpha = max(alpha, score)
        
        return actionToTake


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
        #To solve max nodes for pacman, should not change from minimax
        def maxValue(gameState, depth):
            value = -999
            cDepth = depth + 1 #every pac move increases depth
            
            #terminal node check
            if gameState.isWin() or gameState.isLose() or cDepth == self.depth:
                return self.evaluationFunction(gameState)

            pacActions = gameState.getLegalActions(0)
            
            for p in pacActions:
                newPac = gameState.generateSuccessor(0, p)
                value = max (value, expectiMax(newPac, cDepth, 1))
                
            return value
        
        #honestly looks like min, but takes average of all prior values instead of mid
        def expectiMax (gameState, depth, agentIndex):
            #check for terminal nodes
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            ghostActions = gameState.getLegalActions(agentIndex)
            total = 0
            numActions = 0

            for g in ghostActions:
                newGhost = gameState.generateSuccessor(agentIndex, g)

                if agentIndex == numGhosts:
                    value = maxValue(newGhost, depth)
                else:
                    value = expectiMax(newGhost, depth, agentIndex+1)

                total = total + value
                numActions = numActions + 1
            
            return float(total) / float(numActions)
        
        ## ACTUAL PROGRAM ##
        legalActions = gameState.getLegalActions(0)
        currentValue = -999
        actionToTake = ''
        numGhosts = gameState.getNumAgents() -1

        for action in legalActions:
            newState = gameState.generateSuccessor(0,action)

            value = expectiMax(newState, 0, 1)

            if value > currentValue:
                actionToTake = action
                currentValue = value

        return actionToTake

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    food = currentGameState.getFood()
    foodList = food.asList()
    GhostStates = currentGameState.getGhostStates()
    pos = currentGameState.getPacmanPosition()
    distFromFood = 0
    distFromGhost = 0

    #get a rough estimate for how far pacman is from ALL FOOD
    for pellet in foodList:
        distFromFood += manhattanDistance(pos,pellet)

    #rough estimate for pacman's distance from ALL GHOSTS
    for ghost in GhostStates:
        distFromGhost += manhattanDistance(pos, ghost.getPosition())

    if distFromFood == 0:
        return 999
    else:
        eval = currentGameState.getScore() + 1/distFromFood - distFromGhost

    return eval

# Abbreviation
better = betterEvaluationFunction
