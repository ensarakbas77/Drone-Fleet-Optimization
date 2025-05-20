import math
import heapq

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def heuristic(node, goal):
    return euclidean_distance(node, goal)

def a_star(start, goal, delivery_weight, priority, nofly_zones=None):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    step_count = 0
    max_steps = 5000  # A* algoritması en fazla 5000 adım çalışsın

    while open_set:
        step_count += 1
        if step_count > max_steps:
            print("❌ A* maksimum adım sayısına ulaştı, yol bulunamadı.")
            return None, float('inf')

        _, current = heapq.heappop(open_set)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, g_score[goal]

        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:  # 4 yönlü komşular
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor[0] < 0 or neighbor[1] < 0:
                continue

            tentative_g_score = g_score[current] + euclidean_distance(current, neighbor)

            penalty = 0
            if nofly_zones:
                for zone in nofly_zones:
                    if is_in_nofly_zone(neighbor, zone['coordinates']):
                        penalty += 100

            cost = tentative_g_score + delivery_weight * 0.1 + priority * 5 + penalty

            if neighbor not in g_score or cost < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = cost
                f_score[neighbor] = cost + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, float('inf')

def is_in_nofly_zone(point, polygon):
    if not polygon or len(polygon) < 3:
        return False  # En az 3 nokta olmalı

    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y + 1e-9) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside
