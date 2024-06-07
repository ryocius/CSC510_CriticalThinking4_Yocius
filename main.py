import sys
import time
from simpleai.search import astar, greedy, SearchProblem


class EightPuzzle(SearchProblem):
    # Determine the possible next steps for this iteration
    def actions(self, state):
        board = stringToList(state)
        rowE, colE = findLocation(board, 'E')

        actions = []
        if rowE > 0:
            actions.append(board[rowE - 1][colE])
        if rowE < 2:
            actions.append(board[rowE + 1][colE])
        if colE > 0:
            actions.append(board[rowE][colE - 1])
        if colE < 2:
            actions.append(board[rowE][colE + 1])

        return actions

    # Execute the various next steps
    def result(self, state, action):
        rows = stringToList(state)
        rowE, colE = findLocation(rows, 'E')
        rowN, colN = findLocation(rows, action)

        rows[rowE][colE], rows[rowN][colN] = rows[rowN][colN], rows[rowE][colE]
        return listToString(rows)

    # Compare the step taken to see if it reached the goal
    def is_goal(self, state):
        return state == GOAL

    # Unused but required by SimpleAI library
    def cost(self, state1, action, state2):
        return 1

    # calculate the distance that still needs to be traveled to determine the next action to take
    def heuristic(self, state):
        rows = stringToList(state)
        distance = 0

        for number in '12345678E':
            rowN, colN = findLocation(rows, number)
            rowGoal, colGoal = goalPositions[number]
            distance += abs(rowN - rowGoal) + abs(colN - colGoal)

        return distance

# End State
GOAL = '''1-2-3
4-5-6
7-8-E'''

# Initial State
INITIAL = '''4-1-2
7-5-3
8-E-6'''


def listToString(list_):
    return '\n'.join(['-'.join(row) for row in list_])


def stringToList(string_):
    return [row.split('-') for row in string_.split('\n')]


def findLocation(rows, value):
    for i, row in enumerate(rows):
        for j, element in enumerate(row):
            if element == value:
                return i, j


# cache locations
goalPositions = {}
rowGoal = stringToList(GOAL)
for number in '12345678E':
    goalPositions[number] = findLocation(rowGoal, number)




# Take and validate input from the user
def takeInput():
    print("Select an Option:")
    print("1: Run using the Greedy Best First Search")
    print("2: Run using the A* Search")
    print("3: Compare the Greedy Best First Search and A* Search search")
    print("4: Exit")
    try:
        value = int(input("Enter 1, 2, 3, or 4\n"))
        if value in range(1, 5):
            return value
        else:
            print("Please enter a number value")
            takeInput()
    except:
        print("Please enter a number value")
        takeInput()

def main():
    # Solve the puzzle using the Greedy search algorithm
    startA = time.time()
    resultA = greedy(EightPuzzle(INITIAL))
    endA = time.time()
    elapsedA = (endA - startA)

    # Solve the puzzle using the A* search algorithm
    startB = time.time()
    resultB = astar(EightPuzzle(INITIAL))
    endB = time.time()
    elapsedB = (endB - startB)

    while True:
        choice = takeInput()
        if choice == 1:
            for action, state in resultA.path():
                if action is None:
                    print("Initial State")
                else:
                    print('Move: ', action)
                print(state)
        if choice == 2:
            for action, state in resultB.path():
                if action is None:
                    print("Initial State")
                else:
                    print('Move: ', action)
                print(state)
        if choice == 3:
            print(f"Using Greedy Search took {len(resultA.path())} moves and {elapsedA:4f} seconds to solve the puzzle")
            print(f"Using A* Search took {len(resultB.path())} moves and {elapsedB:4f} seconds to solve the puzzle\n\n")
        if choice == 4:
            sys.exit()

main()