import search

""" Missionaries and Cannibals problem"""

# Defining initial states
initial_state = (3, 3, 1) # (Missionaries on left, Cannibals on left, Boat position 1 for left or 0 for right)
goal_state = (0, 0, 0)

# Function to check if state is valid
def is_valid(state):
    miss, canni, boat = state
    if miss < 0 or canni < 0 or miss > 3 or canni > 3 or (canni > miss > 0) or (3 - canni > 3 - miss > 0):
        return False
    return True

# Define a function to generate next possible states
def generate_next_states(state):
    miss, canni, boat = state
    possible_states = []

    # Define the possible moves
    moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]

    for move in moves:
        if boat == 1:
            new_state = (miss - move[0], canni - move[1], 0)
        else:
            new_state = (miss + move[0], canni + move[1], 1)
        if is_valid(new_state):
            possible_states.append(new_state)
    return possible_states

# Define the Problem class
class MissionariesCannibalsProblem:
    def __init__(self, initial_state, goal_state):
        self.initial = initial_state
        self.goal = goal_state

    def actions(self, state):
        return generate_next_states(state)

    def result(self, state, action):
        return action

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return 1
#  Instantiate the problem
problem = MissionariesCannibalsProblem(initial_state, goal_state)

# Apply the problem in the breadth_first_tree
solution_node = search.breadth_first_tree_search(problem)

# Print the solution
if solution_node:
    solution_path = []
    while solution_node:
        solution_path.append(solution_node.state)
        solution_node = solution_node.parent
    solution_path.reverse()
    for step, state in enumerate(solution_path):
        print(f"Step {step + 1}: {state}")
else:
    print("No solution found.")

