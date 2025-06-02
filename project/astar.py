import heapq
import math
from shapely.geometry import LineString, Polygon
from datetime import datetime
from utils.constants import (
    PENALTY_NOFLY_ZONE,
    PRIORITY_PENALTY_MULTIPLIER,
    MAX_PRIORITY_VALUE
)

# Öklidyen mesafe
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Maliyet fonksiyonu: mesafe, ağırlık ve teslimat önceliği
def calculate_cost(distance, weight, priority):
    base_cost = distance * (1 + weight)
    priority_penalty = (MAX_PRIORITY_VALUE + 1 - priority) * PRIORITY_PENALTY_MULTIPLIER
    return base_cost + priority_penalty

# Zaman verisini dakikaya çevir 
def parse_time_value(val):
    if isinstance(val, int):
        return val
    elif isinstance(val, float):
        return int(val * 60)  
    elif isinstance(val, str):
        t = datetime.strptime(val, "%H:%M").time()
        return t.hour * 60 + t.minute
    else:
        raise ValueError("Geçersiz zaman formatı")


# Evrensel zaman kontrolü entegre edilmiş no-fly zone kontrolü
def intersects_no_fly_zone(start, end, zones, current_time=None):
    path_line = LineString([start, end])

    if current_time is not None:
        current_min = parse_time_value(current_time)
    else:
        current_min = None

    for zone in zones:
        if "active_time" in zone and current_min is not None:
            start_val, end_val = zone["active_time"]
            start_min = parse_time_value(start_val)
            end_min = parse_time_value(end_val)
            if not (start_min <= current_min <= end_min):
                continue

        polygon = Polygon(zone['coordinates'])
        if path_line.intersects(polygon):
            return True

    return False

# A* algoritması
def astar(graph, start_id, goal_id, node_positions, drone, no_fly_zones=[], current_time="10:00"):
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

            if intersects_no_fly_zone(node_positions[current], node_positions[neighbor], no_fly_zones, current_time):
                cost += PENALTY_NOFLY_ZONE

            if cost > remaining_battery:
                continue

            tentative_g = g_score[current] + cost

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                heuristic = euclidean(node_positions[neighbor], node_positions[goal_id])

                if intersects_no_fly_zone(node_positions[neighbor], node_positions[goal_id], no_fly_zones, current_time):
                    heuristic += PENALTY_NOFLY_ZONE

                f_score[neighbor] = tentative_g + heuristic
                heapq.heappush(open_set, (f_score[neighbor], neighbor, remaining_battery - cost))

    return None, float("inf")