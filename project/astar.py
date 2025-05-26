import heapq
import math

# İki nokta arası düz mesafe (öklidyen)
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Mesafe, ağırlık ve önceliğe göre maliyet hesaplar
def calculate_cost(distance, weight, priority):
    base_cost = distance * (1 + weight)
    priority_penalty = (6 - priority) * 100  # 5 öncelik = düşük ceza
    return base_cost + priority_penalty

# Başlangıç-bitiş arasındaki geçiş no-fly zone içinden geçiyor mu?
def intersects_no_fly_zone(start, end, zones):
    for zone in zones:
        for corner in zone['coordinates']:
            if min(start[0], end[0]) <= corner[0] <= max(start[0], end[0]) and \
               min(start[1], end[1]) <= corner[1] <= max(start[1], end[1]):
                return True
    return False

# Proje isterlerine uygun geliştirilmiş A* algoritması
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
            # Yol oluşturuluyor
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

            # Ağırlık kontrolü (drone kapasitesini aşarsa geçme)
            if weight > max_weight:
                continue

            cost = calculate_cost(distance, weight, priority)

            # No-fly zone kontrolü
            if intersects_no_fly_zone(node_positions[current], node_positions[neighbor], no_fly_zones):
                cost += 9999  # ağır ceza

            # Batarya yetmiyorsa geçme
            if cost > remaining_battery:
                continue

            tentative_g = g_score[current] + cost

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                heuristic = euclidean(node_positions[neighbor], node_positions[goal_id])
                f_score[neighbor] = tentative_g + heuristic
                heapq.heappush(open_set, (f_score[neighbor], neighbor, remaining_battery - cost))

    return None, float("inf")  # geçerli yol yoksa


# Test için örnek kod
if __name__ == "__main__":
    # Örnek graf (kenar: mesafe, ağırlık, öncelik)
    graph = {
        0: [(1, {"distance": 5, "weight": 2.0, "priority": 4}),
            (2, {"distance": 10, "weight": 3.5, "priority": 2})],
        1: [(2, {"distance": 3, "weight": 1.0, "priority": 5}),
            (3, {"distance": 8, "weight": 2.5, "priority": 3})],
        2: [(3, {"distance": 1, "weight": 1.2, "priority": 5})],
        3: []
    }

    # Düğüm konumları
    positions = {
        0: (0, 0),
        1: (1, 1),
        2: (2, 2),
        3: (3, 3)
    }

    # No-fly zone örneği
    no_fly_zones = [
        {"id": 1, "coordinates": [(2, 2), (2.5, 2.5)]}
    ]

    # Drone özellikleri
    drone = {
        "id": 1,
        "start_pos": (0, 0),
        "max_weight": 5.0,
        "battery": 1000
    }

    path, cost = astar(graph, 0, 3, positions, drone, no_fly_zones)
    print("🚁 En iyi rota:", path)
    print("🔋 Toplam maliyet:", round(cost, 2))
