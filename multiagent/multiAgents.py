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
import sys
from game import Agent

# Call: python pacman.py --frameTime 0.5 -p MinimaxAgent -l testClassic -a depth=2

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
        total_score = 0.0
        oldFood = currentGameState.getFood()
        for x in xrange(oldFood.width):
          for y in xrange(oldFood.height):
            if (oldFood[x][y]):
              d = manhattanDistance((x,y),newPos)
              if (d==0):
                total_score+=100
              else:
                total_score+=1.0/(d*d)

        for ghost in newGhostStates:
          d = manhattanDistance(ghost.getPosition(), newPos)
          if (d<=1):
            if(ghost.scaredTimer!=0):
              total_score+=2000
            else:
              total_score-=200
        return total_score
        #return successorGameState.getScore()

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
        """

        "Teacher solution"
        ""
        def terminalTest(gameState, depth):
            return gameState.isWin() or gameState.isLose() or depth == 0

        def utility(gameState):
            return self.evaluationFunction(gameState)

        def result(gameState, agent, action):
            return gameState.generateSuccessor(agent, action)

        def max_value(gameState, agent, depth):
            if terminalTest(gameState, depth): return utility(gameState)

            v = -sys.maxint
            for a in gameState.getLegalActions(agent):
               v = max(v, min_value(result(gameState, agent, a), 1, depth))
            return v

        def min_value(gameState, agent, depth):
            if terminalTest(gameState, depth): return utility(gameState)

            v = sys.maxint
            for a in gameState.getLegalActions(agent):
               if (agent == gameState.getNumAgents()-1):
                   v = min(v, max_value(result(gameState, agent, a), 0, depth-1))
               else:
                   v = min(v, min_value(result(gameState, agent, a), agent+1, depth))
            return v

        v = -sys.maxint
        actions = []
        for a in gameState.getLegalActions(0):
            u = min_value(result(gameState, 0, a), 1, self.depth)
            if u == v: actions.append(a)
            elif u >= v: v = u; actions = [a]

        return random.choice(actions)
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def terminalTest(gameState, depth):
            return gameState.isWin() or gameState.isLose() or depth == 0

        def utility(gameState):
            return self.evaluationFunction(gameState)

        def result(gameState, agent, action):
            return gameState.generateSuccessor(agent, action)

        def max_value(gameState, agent, depth, alpha, betha):
            if terminalTest(gameState, depth): return utility(gameState)

            v = -sys.maxint
            for a in gameState.getLegalActions(agent):
               v = max(v, min_value(result(gameState, agent, a), 1, depth, alpha, betha))

               if v > betha: return v
               alpha = max(alpha, v)
            return v

        def min_value(gameState, agent, depth, alpha, betha):
            if terminalTest(gameState, depth): return utility(gameState)

            v = sys.maxint
            for a in gameState.getLegalActions(agent):
               if (agent == gameState.getNumAgents()-1):
                   v = min(v, max_value(result(gameState, agent, a), 0, depth-1, alpha, betha))
               else:
                   v = min(v, min_value(result(gameState, agent, a), agent+1, depth, alpha, betha))

               if v < alpha: return v
               betha = min(betha, v)
            return v

        v = -sys.maxint
        actions = []
        for a in gameState.getLegalActions(0):
            u = min_value(result(gameState, 0, a), 1, self.depth, v, sys.maxint)
            if u == v: actions.append(a)
            elif u >= v: v = u; actions = [a];

        return random.choice(actions)

        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        def terminalTest(gameState, depth):
            return gameState.isWin() or gameState.isLose() or depth == 0

        def utility(gameState):
            return self.evaluationFunction(gameState)

        def result(gameState, agent, action):
            return gameState.generateSuccessor(agent, action)

        def max_value(gameState, agent, depth):
            if terminalTest(gameState, depth): return utility(gameState)

            v = -sys.maxint
            for a in gameState.getLegalActions(agent):
               v = max(v, min_value(result(gameState, agent, a), 1, depth))
            return v

        def min_value(gameState, agent, depth):
            if terminalTest(gameState, depth): return utility(gameState)

            v = []
            for a in gameState.getLegalActions(agent):
               if (agent == gameState.getNumAgents()-1):
                   v.append(max_value(result(gameState, agent, a), 0, depth-1))
               else:
                   v.append(min_value(result(gameState, agent, a), agent+1, depth))

            return sum(v) / float(len(v))

        v = -sys.maxint
        actions = []
        for a in gameState.getLegalActions(0):
            u = min_value(result(gameState, 0, a), 1, self.depth)
            if u == v: actions.append(a)
            elif u >= v: v = u; actions = [a]

        return random.choice(actions)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    total_score = 0.0
    oldFood = currentGameState.getFood()
    for x in xrange(oldFood.width):
      for y in xrange(oldFood.height):
        if (oldFood[x][y]):
          d = manhattanDistance((x,y),newPos)
          if (d==0):
            total_score+=100
          else:
            total_score+=1.0/(d*d)

    for ghost in newGhostStates:
      d = manhattanDistance(ghost.getPosition(), newPos)
      if (d<=1):
        if(ghost.scaredTimer!=0):
          total_score+=2000
        else:
          total_score-=200

    #print total_score, currentGameState.getScore()
    return total_score + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
