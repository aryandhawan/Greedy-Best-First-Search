class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

class PriorityFrontier:
    def __init__(self, heuristic_func):
        self.frontier = []
        self.heuristic_func = heuristic_func

    def add(self, node):
        self.frontier.append(node)
        self.sort_frontier()

    def remove(self):
        if self.is_empty():
            raise Exception("Frontier is empty!")
        return self.frontier.pop(0)

    def is_empty(self):
        return len(self.frontier) == 0

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def sort_frontier(self):
        self.frontier.sort(key=lambda x: self.heuristic_func(x.state))  # Sorting by heuristic value

class GBFSSolver:
    def __init__(self, start_state, goal_state, neighbors_func, heuristic_func):
        self.start_state = start_state
        self.goal_state = goal_state
        self.neighbors_func = neighbors_func
        self.heuristic_func = heuristic_func
        self.frontier = PriorityFrontier(self.heuristic_func)

    def greedy_best_first_search(self):
        start_node = Node(self.start_state)
        self.frontier.add(start_node)
        explored = set()

        while not self.frontier.is_empty():
            node = self.frontier.remove()

            if node.state == self.goal_state:
                return self.reconstruct_path(node)

            explored.add(node.state)

            for action, state in self.neighbors_func(node.state):
                if state not in explored and not self.frontier.contains_state(state):
                    child_node = Node(state, node, action)
                    self.frontier.add(child_node)

        return None  # No solution found

    def reconstruct_path(self, node):
        path = []
        while node.parent is not None:
            path.append((node.action, node.state))
            node = node.parent
        path.reverse()
        return path



def neighbors(state):
    x, y = state
    moves = {
        "UP": (x, y - 1),
        "DOWN": (x, y + 1),
        "LEFT": (x - 1, y),
        "RIGHT": (x + 1, y),
    }
    return list(moves.items())

def heuristic(state):
    goal = (3, 3)  # Example goal state
    x1, y1 = state
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)  # Manhattan Distance

# Define start and goal states
start = (0, 0)
goal = (3, 3)

# Run GBFS
solver = GBFSSolver(start, goal, neighbors, heuristic)
solution = solver.greedy_best_first_search()

# Print Solution Path
print("Solution Path:", solution)
