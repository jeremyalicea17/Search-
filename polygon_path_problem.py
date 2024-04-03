import math
from search import Problem, astar_search  


class PolygonPathProblem(Problem):
    def __init__(self, initial, goal, polygons, step_size=1):
        super().__init__(initial, goal)
        self.polygons = polygons
        self.step_size = step_size

    def actions(self, state):
        neighbors = self.get_neighbors(state)
        valid_actions = [neighbor for neighbor in neighbors if self.can_reach_directly(state, neighbor)]
        if self.can_reach_directly(state, self.goal):
            valid_actions.append(self.goal)
        return valid_actions

    def get_neighbors(self, state):
        step = self.step_size
        x, y = state
        # Generate neighboring nodes in a grid pattern
        return [(x+dx, y+dy) for dx in [-step, 0, step] for dy in [-step, 0, step] if not (dx == 0 and dy == 0)]

    def can_reach_directly(self, state, vertex):
        if state == vertex:
            return False
        for polygon in self.polygons:
            for i in range(len(polygon)):
                edge_start, edge_end = polygon[i], polygon[(i + 1) % len(polygon)]
                if self.do_lines_intersect(state, vertex, edge_start, edge_end):
                    return False
        return True

    @staticmethod
    def do_lines_intersect(line1_start, line1_end, line2_start, line2_end):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        A, B = line1_start, line1_end
        C, D = line2_start, line2_end

        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


    def result(self, state, action):
        return action
 


    def h(self, node):
        return math.sqrt((node.state[0] - self.goal[0])**2 + (node.state[1] - self.goal[1])**2)


# Test cases
def test_cases():
    polygons = {
        "simple": [],
        "single_obstacle": [[[2, 2], [2, 3], [3, 3], [3, 2]]],
        "multiple_obstacles": [[[1, 2], [1, 3], [2, 3], [2, 2]], 
                               [[3, 1], [3, 2], [4, 2], [4, 1]]],
        "narrow_path": [[[1, 1], [1, 3], [2, 3], [2, 1]],
                        [[3, 1], [3, 3], [4, 3], [4, 1]]],
        "dead_end": [[[1, 1], [1, 2], [2, 2], [2, 1]], 
                     [[1, 3], [1, 4], [3, 4], [3, 3]]],
        "distant_goal": []
        } 

    start_goal_pairs = {
        "simple": ((0, 0), (5, 5)),
        "single_obstacle": ((0, 0), (4, 4)),
        "multiple_obstacles": ((0, 0), (5, 5)),
        "narrow_path": ((0, 0), (5, 5)),
        "dead_end": ((0, 0), (4, 0)),
        "distant_goal": ((0, 0), (10, 10))
    }

    problems = {name: PolygonPathProblem(start, goal, polygons[name])
                for name, (start, goal) in start_goal_pairs.items()}

    for name, problem in problems.items():
        solution = astar_search(problem, h = problem.h)
        print(f"Test Case '{name}': Path - {solution.solution() if solution else 'No path found'}, "
              f"Path Cost - {solution.path_cost if solution else 'N/A'}")


if __name__ == "__main__":
    test_cases()