#Input
##height
##Initial config
##Last config

import sys
import itertools
import fileinput
import copy

#(); (); ();
#Desired stage
class Objective(object):
    #Constructor
    def __init__(self, string=None, crateA=[], cost=0, steps=[]):
        self.crateA = crateA
        self.cost = cost
        self.steps = steps
        self.shouldCheck = []
        if string: self.initializeCrate(string)
            
    def __eq__(self, other):
        is_equal = True
        for idx, stack in enumerate(self.crateA):
            if self.shouldCheck[idx]: is_equal = is_equal and str(stack) == str(other.crateA[idx])

        return is_equal
    ####
    def initializeCrate(self, string):
        for stack in string.split("; "):
            c = stack.strip("()")
            shouldCheck = True
            
            if len(c) and c[0] == "X": shouldCheck = False
            elif len(c): c = c.split(", ")
            else: c = []
            self.shouldCheck.append(shouldCheck)
            self.crateA.append(c)

##
class currentState(object):
    def __init__(self, string=None, crateA=[], cost=0, steps=[]):
        self.crateA = crateA
        self.cost = cost
        self.steps = steps
        if string: self.initializeCrate(string)
    
    def __str__(self): return str(self.crateA)

    def __hash__(self): return hash(str(self.crateA))

    def __eq__(self, other): return str(self) == other

    def getCost(self): return str(int(self.cost)) + "\n"

    def getSteps(self): return "; ".join(map(str, self.steps)) + "\n"
        
    ######
    ##Cost 0.5
    def newCost(self,action):
        self.cost = self.cost + 0.5 + 0.5 + abs(action[0] - action[1])

    def doAction(self, action):
        x = self.crateA[action[0]].pop()
        self.crateA[action[1]].append(x)
        self.steps.append(action)
        self.newCost(action)

    def moveAction(self, action):
        new_state = currentState(crateA=copy.deepcopy(self.crateA), cost=self.cost, steps=copy.deepcopy(self.steps))
        return new_state

    def validAction(self, action, height):
        return len(self.crateA[action[1]]) + 1 <= height and len(self.crateA[action[0]]) - 1 >= 0

    def initializeCrate(self, string):
        for stack in string.split("; "):
            c = stack.strip("()")
            if not len(c):
                c = []
            else:
                c = c.split(", ")
            self.crateA.append(c)

#All possible actions
def actions(state, maxHeight):
    space = tuple(range(len(state.crateA)))
    possible_actions = itertools.product(space, repeat=2)
    return [action for action in possible_actions if state.validAction(action, maxHeight)]

if __name__ == '__main__':
    maxHeight    = -1
    frontier      = []
    explored      = set()
    final          = None
    solutionFound = False
    input         = []

    for line in sys.stdin:
        line = line.strip("\n")
        input.append(line)

    for idx, line in enumerate(input):
        if idx == 0: maxHeight = int(line)
        elif idx == 1: frontier.append(currentState(string=line))
        elif idx == 2: final = Objective(string=line)


    while(len(frontier)):
        node = frontier.pop(0)
        explored.add(node)
        #Checks every possible action
        for action in actions(node, maxHeight):
            new_node = node.moveAction(action)
            new_node.doAction(action)
            if new_node not in explored:
                if final != new_node:
                    frontier.append(new_node)
                else: 
                    sys.stdout.write(new_node.getCost())
                    sys.stdout.write(new_node.getSteps())
                    frontier = []
                    solutionFound = True
                    break
    if not solutionFound: sys.stdout.write("No solution found\n")