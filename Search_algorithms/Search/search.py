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
import pdb
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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    dictionary = {}
    start = problem.getStartState()
    closed = set()
    fringe = util.Stack()
    dictionary[start] = (None, None)
    fringe.push(start)

    while not fringe.isEmpty():
        state = fringe.pop()

        if problem.isGoalState(state):
            break;

        if state not in closed:
            closed.add(state)
            for triple in problem.getSuccessors(state):
                if triple[0] not in closed:
                    fringe.push(triple[0])
                    dictionary[triple[0]] = (state, triple[1])

    ret = []
    while state != start:
        ret += [dictionary[state][1]]
        state = dictionary[state][0]
    ret.reverse()
    return ret

    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    dictionary = {}
    start = problem.getStartState()
    closed = set()
    fringe = util.Queue()
    fringe.push(start)

    while not fringe.isEmpty():
        state = fringe.pop()

        if problem.isGoalState(state):
            break;

        if state not in closed:
            closed.add(state)
            for triple in problem.getSuccessors(state):
                if triple[0] not in closed:
                    fringe.push(triple[0])
                    if triple[0] not in dictionary:
                        dictionary[triple[0]] = (state, triple[1])

    ret = []
    while state != start:
        ret += [dictionary[state][1]]
        state = dictionary[state][0]
    ret.reverse()
    return ret
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    dictionary = {}
    start = problem.getStartState()
    closed = set()
    fringe = util.PriorityQueue()
    dictionary[start] = (None, None, 0)
    fringe.push((start, 0), 0)

    while not fringe.isEmpty():
        state, accum = fringe.pop()
        if problem.isGoalState(state):
            break
        if state not in closed:
            closed.add(state)
            #triples = problem.getSuccessors(state)
            for triple in problem.getSuccessors(state):
                if triple[0] not in closed:
                    fringe.push((triple[0],triple[2] + accum), triple[2] + accum)
                    if triple[0] not in dictionary:
                        dictionary[triple[0]] = (state, triple[1], triple[2] + accum)
                    elif dictionary[triple[0]][2] > triple[2] + accum:
                        dictionary[triple[0]] = (state, triple[1], triple[2] + accum)
    ret = []
   

    while state != start:
        #print dictionary[state]
        ret += [dictionary[state][1]]
        state = dictionary[state][0]
        #counter+=1

    ret.reverse()
    return ret;

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    dictionary = {}
    start = problem.getStartState()
    closed = set()
    fringe = util.PriorityQueue()
    dictionary[start] = (None, None, 0)
    fringe.push((start, 0 + heuristic(start, problem)), 0 + heuristic(start, problem))

    while not fringe.isEmpty():
        state, accum = fringe.pop()
        if problem.isGoalState(state):
            break
        if state not in closed:
            closed.add(state)
            #triples = problem.getSuccessors(state)
            for triple in problem.getSuccessors(state):

                
                if triple[0] not in closed:

                    updatedHeuristic = triple[2] + accum - heuristic(state, problem) + heuristic(triple[0], problem)

                    fringe.push((triple[0], updatedHeuristic), 
                        updatedHeuristic)
                    if triple[0] not in dictionary:
                        dictionary[triple[0]] = (state, triple[1], updatedHeuristic)
                    elif dictionary[triple[0]][2] > updatedHeuristic:
                        dictionary[triple[0]] = (state, triple[1], updatedHeuristic)
    ret = []
   

    while state != start:
        #print dictionary[state]
        ret += [dictionary[state][1]]
        state = dictionary[state][0]
        #counter+=1

    ret.reverse()
    return ret;
    
    # dictionary = {}
    # start = problem.getStartState()
    # closed = set()
    # fringe = util.PriorityQueue()
    # fringe.push((start, 0), 0)

    # while not fringe.isEmpty():
    #     state, direction, accum = fringe.pop()
    #     if problem.isGoalState(state):
    #         break;
    #     if state not in closed:
    #         closed.add(state)
    #         triples = problem.getSuccessors(state)
    #         for triple in problem.getSuccessors(state):
    #             if triple[0] not in closed:
    #                 fringe.push((triple[0], triple[2]+accum), triple[2] + accum + heuristic(triple[0], problem))
    #                 if triple[0] not in dictionary:
    #                     dictionary[triple[0]] = (state, triple[1], triple[2] + accum)
    #                 # elif dictionary[triple[0]][2] > triple[2] + accum:
    #                 #     dictionary[triple[0]] = (state, triple[1], triple[2] + accum)

    # ret = []
    # while state != start:
    #     ret += [dictionary[state][1]]
    #     state = dictionary[state][0]
    # ret.reverse()
    # return ret


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
