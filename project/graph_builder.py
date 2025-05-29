import math

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def calculate_cost(dp_from, dp_to):
    # cost = distance * weight + (priority * 100)
    distance = euclidean_distance(dp_from["pos"], dp_to["pos"])
    weight = dp_to["weight"]
    priority = dp_to["priority"]
    return distance * weight + (priority * 100)

# Kenar bilgisini detaylı döndürür
def build_graph(delivery_points):
    graph = {}
    for dp_from in delivery_points:
        from_id = dp_from["id"]
        graph[from_id] = []
        for dp_to in delivery_points:
            to_id = dp_to["id"]
            if from_id == to_id:
                continue
            cost = calculate_cost(dp_from, dp_to)
            graph[from_id].append((to_id, cost))
    return graph

# Test için
if __name__ == "__main__":
    deliveries = [
        {"id": 0, "pos": (10, 20), "weight": 2.0, "priority": 3},
        {"id": 1, "pos": (15, 25), "weight": 1.5, "priority": 5},
        {"id": 2, "pos": (20, 30), "weight": 3.0, "priority": 1},
    ]
    graph = build_graph(deliveries)
    for k, v in graph.items():
        print(f"{k}: {v}")
