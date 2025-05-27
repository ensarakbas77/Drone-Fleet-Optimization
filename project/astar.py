import heapq
import math
from shapely.geometry import LineString, Polygon  # 🔹 Eklendi

# Öklidyen mesafe
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Maliyet fonksiyonu: mesafe, ağırlık ve teslimat önceliği
def calculate_cost(distance, weight, priority):
    base_cost = distance * (1 + weight)
    priority_penalty = (6 - priority) * 100  # öncelik 5 → az ceza
    return base_cost + priority_penalty

# 🔍 Gelişmiş no-fly zone kontrolü (shapely ile çizgi-çokgen kesişimi)
def intersects_no_fly_zone(start, end, zones):
    path_line = LineString([start, end])
    for zone in zones:
        polygon = Polygon(zone['coordinates'])
        if path_line.intersects(polygon):
            return True
    return False

# A* algoritması
def astar(graph, start_id, goal_id, node_positions, drone, no_fly_zones=[]):
    max_weight = drone["max_weight"]
    battery = drone["battery"]
    start_pos = node_positions[start_id]

    open_set = []
    heapq.heappush(open_set, (0, start_id, battery))

    came_from = {}
    g_score = {node: float("inf") for node in graph}
    g_score[start_id] = 0

    f_score = {node: float("inf") for node in graph}
    f_score[start_id] = euclidean(node_positions[start_id], node_positions[goal_id])

    while open_set:
        _, current, remaining_battery = heapq.heappop(open_set)

        if current == goal_id:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_id)
            path.reverse()
            return path, g_score[goal_id]

        for neighbor, info in graph[current]:
            distance = info["distance"]
            weight = info["weight"]
            priority = info["priority"]

            if weight > max_weight:
                continue

            cost = calculate_cost(distance, weight, priority)

            # Gelişmiş no-fly zone kontrolü
            if intersects_no_fly_zone(node_positions[current], node_positions[neighbor], no_fly_zones):
                cost += 9999

            if cost > remaining_battery:
                continue

            tentative_g = g_score[current] + cost

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                heuristic = euclidean(node_positions[neighbor], node_positions[goal_id])

                if intersects_no_fly_zone(node_positions[neighbor], node_positions[goal_id], no_fly_zones):
                    heuristic += 9999

                f_score[neighbor] = tentative_g + heuristic
                heapq.heappush(open_set, (f_score[neighbor], neighbor, remaining_battery - cost))

    return None, float("inf")
