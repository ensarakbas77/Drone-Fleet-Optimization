import heapq
import math

def euclidean(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def astar(graph, start_id, goal_id, node_positions):
    open_set = []
    heapq.heappush(open_set, (0, start_id)) 

    came_from = {}
    g_score = {node: float("inf") for node in graph}
    g_score[start_id] = 0

    f_score = {node: float("inf") for node in graph}
    f_score[start_id] = euclidean(node_positions[start_id], node_positions[goal_id])

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal_id:
            
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_id)
            path.reverse()
            return path, g_score[goal_id]

        for neighbor, cost in graph[current]:
            tentative_g = g_score[current] + cost
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + euclidean(
                    node_positions[neighbor], node_positions[goal_id])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, float("inf")  

if __name__ == "__main__":
    graph = {
        0: [(1, 5), (2, 10)],
        1: [(2, 3), (3, 8)],
        2: [(3, 1)],
        3: []
    }
    positions = {
        0: (0, 0),
        1: (1, 1),
        2: (2, 2),
        3: (3, 3)
    }
    path, cost = astar(graph, 0, 3, positions)
    print("En iyi rota:", path)
    print("Toplam maliyet:", cost)

