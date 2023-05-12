# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    from util import Stack

    DFS = Stack()
    path = []
    beenTo = []
    
    #check if we start at a goal
    if problem.isGoalState(problem.getStartState()):
        return path

    #push start position and list to track route to start
    DFS.push((problem.getStartState(), []))

    while DFS.isEmpty() != 1:
        pos, path = DFS.pop()

        #add position to places we've been
        beenTo.append(pos)

        if problem.isGoalState(pos):
            return path

        s = problem.getSuccessors(pos)
        if s: #check if s is empty
            for i in s:
                if i[0] not in beenTo: #check if we have been to either successor
                    pathToPos = path + [i[1]] #track route taken to get to successor pos
                    DFS.push((i[0], pathToPos))

    #in case that DFS empties w/ no path
    if DFS.isEmpty():
        return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    BFS = Queue()
    beenTo = []
    path = []

    if problem.isGoalState(problem.getStartState()):
        return path
    
    BFS.push((problem.getStartState(), []))

    while BFS.isEmpty() != 1:
        pos, path = BFS.pop()

        if pos in beenTo:
            continue
        beenTo.append(pos)

        if problem.isGoalState(pos):
            return path
        
        s = problem.getSuccessors(pos)
        if s:
            for i in s:
                if i[0] not in beenTo:
                    pathToPos = path + [i[1]]
                    BFS.push((i[0], pathToPos))
    
    if BFS.isEmpty():
        return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    UCS = PriorityQueue()
    beenTo = []
    path = []

    if problem.isGoalState(problem.getStartState()):
        return path

    #this time, push pos, path to pos, and cost to pos
    UCS.push((problem.getStartState(), []), 0)
    while UCS.isEmpty() != 1:
        pos, path = UCS.pop()

        if pos in beenTo:
            continue
        beenTo.append(pos)

        if problem.isGoalState(pos):
            return path

        s = problem.getSuccessors(pos)
        if s:
            for i in s:
                if i[0] not in beenTo:
                    pathToPos = path + [i[1]]
                    costToPos = problem.getCostOfActions(pathToPos)
                    UCS.push((i[0],pathToPos), costToPos)

    if UCS.isEmpty():
        return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    from util import PriorityQueue
    #from util import manhattanDistance
    AStar = PriorityQueue()
    #heuristic(child,problem)
    current = [problem.getStartState(), [], 0]

    beenTo = []
    
    if problem.isGoalState(problem.getStartState()):
        return []

    path = []
    beenTo = []

    AStar.push((problem.getStartState(),[],0),0)
    
    while AStar.isEmpty() != 1:
        pos, path, cost = AStar.pop()

        if pos in beenTo:
            continue
        beenTo.append(pos)

        if problem.isGoalState(pos):
            return path
        
        s = problem.getSuccessors(pos)
        if s:
            for i in s:
                #print(s)
                if i[0] not in beenTo:
                    pathToPos = path + [i[1]]
                    costToPos = problem.getCostOfActions(pathToPos)
                    AStar.push((i[0],pathToPos,costToPos), costToPos + heuristic(i[0],problem))
    
    if AStar.isEmpty():
        return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
