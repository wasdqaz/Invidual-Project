import heapq
import time
import sys
from collections import deque

class Graph:
    def __init__(self, num_nodes, start, goal, adjacency_matrix, heuristic_weights):
        self.num_nodes = num_nodes
        self.start = start
        self.goal = goal
        self.adjacency_matrix = adjacency_matrix
        self.heuristic_weights = heuristic_weights

    def bfs(self):
        visited = [False] * self.num_nodes
        queue = deque([(self.start, [self.start])])
        while queue:
            current, path = queue.popleft()
            if current == self.goal:
                return path
            for neighbor, weight in enumerate(self.adjacency_matrix[current]):
                if weight > 0 and not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, path + [neighbor]))
        return []

    def dfs(self):
        visited = [False] * self.num_nodes
        stack = [(self.start, [self.start])]
        while stack:
            current, path = stack.pop()
            if current == self.goal:
                return path
            for neighbor, weight in enumerate(self.adjacency_matrix[current]):
                if weight > 0 and not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append((neighbor, path + [neighbor]))
        return []

    def ucs(self):
        priority_queue = [(0, self.start, [self.start])]
        visited = [False] * self.num_nodes
        while priority_queue:
            current_cost, current_node, path = heapq.heappop(priority_queue)
            if current_node == self.goal:
                return path, current_cost
            if not visited[current_node]:
                visited[current_node] = True
                for neighbor, weight in enumerate(self.adjacency_matrix[current_node]):
                    if weight > 0:
                        heapq.heappush(priority_queue, (current_cost + weight, neighbor, path + [neighbor]))
        return [], float('inf')

    def ids(self, max_depth=50):
        def dfs_limited(node, path, depth):
            if depth == 0 and node == self.goal:
                return path
            if depth > 0:
                for neighbor, weight in enumerate(self.adjacency_matrix[node]):
                    if weight > 0 and neighbor not in path:
                        result = dfs_limited(neighbor, path + [neighbor], depth - 1)
                        if result:
                            return result
            return None

        for depth in range(max_depth):
            result = dfs_limited(self.start, [self.start], depth)
            if result:
                return result
        return []

    def gbfs(self):
        priority_queue = [(self.heuristic_weights[self.start], self.start, [self.start])]
        visited = [False] * self.num_nodes
        while priority_queue:
            _, current_node, path = heapq.heappop(priority_queue)
            if current_node == self.goal:
                return path
            if not visited[current_node]:
                visited[current_node] = True
                for neighbor, weight in enumerate(self.adjacency_matrix[current_node]):
                    if weight > 0:
                        heapq.heappush(priority_queue, (self.heuristic_weights[neighbor], neighbor, path + [neighbor]))
        return []
 
    def a_star(self):
        open_set = [(self.heuristic_weights[self.start], 0, self.start, [self.start])]
        heapq.heapify(open_set)
        g_score = [float('inf')] * self.num_nodes
        g_score[self.start] = 0
        
        while open_set:
            _, current_g, current_node, path = heapq.heappop(open_set)
            
            if current_node == self.goal:
                return path, g_score[self.goal]
            
            for neighbor, weight in enumerate(self.adjacency_matrix[current_node]):
                if weight > 0:
                    tentative_g_score = current_g + weight
                    if tentative_g_score < g_score[neighbor]:
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic_weights[neighbor]
                        heapq.heappush(open_set, (f_score, tentative_g_score, neighbor, path + [neighbor]))
        return [], float('inf')

    def hill_climbing(self):
        current = self.start
        path = [current]       
        while current != self.goal:
            # Get neighbors of the current node
            neighbors = [(neighbor, self.heuristic_weights[neighbor]) 
                         for neighbor, weight in enumerate(self.adjacency_matrix[current]) 
                         if weight > 0]
            if not neighbors:
                return [-1]           
            # Select the neighbor with the lowest heuristic value
            next_node = min(neighbors, key=lambda x: x[1])[0]
            
            if self.heuristic_weights[next_node] >= self.heuristic_weights[current]:
                break 
            path.append(next_node)
            current = next_node
        if current != self.goal:
            return [-1]
        return path

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        num_nodes = int(file.readline().strip())
        start, goal = map(int, file.readline().strip().split())
        adjacency_matrix = [list(map(int, file.readline().strip().split())) for _ in range(num_nodes)]
        heuristic_weights = list(map(int, file.readline().strip().split()))
    return num_nodes, start, goal, adjacency_matrix, heuristic_weights

def write_output_file(file_path, results, case_num):
    with open(file_path, 'a') as file:
        file.write(f'Case: {case_num}\n')
        for algorithm, (path, cost, runtime, memory) in results.items():
            file.write(f'{algorithm} Path: {path}, Cost: {cost}, Runtime: {runtime:.2f}s, Memory: {memory:.2f}KB\n')
        file.write('\n')

def measure_performance(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    runtime = end_time - start_time
    memory_usage = sys.getsizeof(result) / 1024  #KB
    return result, runtime, memory_usage

def func(input_file, case_num):
    output_file = 'Test_case/graph_output.txt'
    num_nodes, start, goal, adjacency_matrix, heuristic_weights = read_input_file(input_file)
    
    graph = Graph(num_nodes, start, goal, adjacency_matrix, heuristic_weights)
    
    results = {}

    algorithms = [
        ("BFS", graph.bfs),
        ("DFS", graph.dfs),
        ("UCS", graph.ucs),
        ("IDS", graph.ids),
        ("GBFS", graph.gbfs),
        ("A*", graph.a_star),
        ("Hill Climbing", graph.hill_climbing)
    ]
    
    for name, algorithm in algorithms:
        if name in ("UCS", "A*"):
            (path, cost), runtime, memory = measure_performance(algorithm)
        else:
            path, runtime, memory = measure_performance(algorithm)
            cost = sum(adjacency_matrix[path[i]][path[i+1]] for i in range(len(path) - 1)) if path else float('inf')
        results[name] = (path, cost, runtime, memory)
    write_output_file(output_file, results, case_num)
def main():
    input_file = ['Test_case/graph_input_1.txt', 
                  'Test_case/graph_input_2.txt', 
                  'Test_case/graph_input_3.txt', 
                  'Test_case/graph_input_4.txt', 
                  'Test_case/graph_input_5.txt']
    with open('Test_case/graph_output.txt', 'w'):
        pass
    case_num = 1
    for fileName in input_file:
        func(fileName, case_num)
        case_num += 1

if __name__ == "__main__":
    main()
