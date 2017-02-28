import fileinput
import copy
import sys
import itertools
import time

class State(object):
    def __init__(self, string=None, containers=[], cost=0, steps=[]):
        self.cost       = cost
        self.steps      = steps
        self.containers = containers
        if string:
            self.initializeContainer(string)

    def getCost(self):
        return str(int(self.cost)) + "\n"

    def getSteps(self):
        return "; ".join(map(str, self.steps)) + "\n"

    def updateCost(self,action):
        self.cost = self.cost + 0.5 + 0.5 + abs(action[0] - action[1])

    def applyAction(self, action):
        x = self.containers[action[0]].pop()
        self.containers[action[1]].append(x)
        self.steps.append(action)
        self.updateCost(action)

    def stateFromAction(self, action):
        new_state = State(containers=copy.deepcopy(self.containers),
                    cost=self.cost,
                    steps=copy.deepcopy(self.steps))
        return new_state

    def isValidAction(self, action, height):
        return len(self.containers[action[1]]) + 1 <= height and \
            len(self.containers[action[0]]) - 1 >= 0

    def setContainer(self, containers):
        self.containers = containers

    def initializeContainer(self, string):
        for stack in string.split("; "):
            c = stack.strip("()")
            if len(c):
                c = c.split(", ")
            else:
                c = []
            self.containers.append(c)

    def __str__(self):
        return str(self.containers)

    def __hash__(self):
        return hash(str(self.containers))

    def __eq__(self, other):
        return str(self) == other


class Goal(object):
    def __init__(self, string=None, containers=[], cost=0, steps=[]):
        self.cost       = cost
        self.steps      = steps
        self.containers = containers
        self.shouldCheck = []

        if string:
            self.initializeContainer(string)

    def initializeContainer(self, string):
        for stack in string.split("; "):
            c = stack.strip("()")
            shouldCheck = True

            if len(c) and c[0] == "X":
                shouldCheck = False
            elif len(c):
                c = c.split(", ")
            else:
                c = []

            self.shouldCheck.append(shouldCheck)
            self.containers.append(c)

    def __eq__(self, other):
        is_equal = True
        for idx, stack in enumerate(self.containers):
            if self.shouldCheck[idx]:
                is_equal = is_equal and str(stack) == str(other.containers[idx])

        return is_equal


def valid_actions(state, height):
    space = tuple(range(len(state.containers)))
    possible_actions = itertools.product(space, repeat=2)
    return [action for action in possible_actions
                if state.isValidAction(action, height)]



if __name__ == '__main__':
    max_height    = -1
    frontier      = []
    explored      = set()
    goal          = None
    solutionFound = False
    input         = []

    # Read each input line
    for line in sys.stdin:
        # sys.stdout.write(line)
        line = line.strip("\n")
        input.append(line)

    for idx, line in enumerate(input):
        # Height
        if idx == 0:
            max_height = int(line)
        # Initial State
        elif idx == 1:
            frontier.append(State(string=line))
        # # Goal
        elif idx == 2:
            goal = Goal(string=line)

    # DFS
    t0 = time.time()
    while(len(frontier)):
        node = frontier.pop()
        explored.add(node)
        for action in valid_actions(node, max_height):
            new_node = node.stateFromAction(action)
            new_node.applyAction(action)
            #print str(new_node)
            if new_node not in explored:
                if goal == new_node:
                    sys.stdout.write(new_node.getCost())
                    sys.stdout.write(new_node.getSteps())
                    frontier = []
                    solutionFound = True
                    break
                else:
                    frontier.append(new_node)
    if not solutionFound:
        sys.stdout.write("No solution found\n")
    #print time.time()