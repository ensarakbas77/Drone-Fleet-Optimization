import math

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

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
            distance = euclidean_distance(dp_from["pos"], dp_to["pos"])
            edge_info = {
                "distance": distance,
                "weight": dp_to["weight"],
                "priority": dp_to["priority"]
            }
            graph[from_id].append((to_id, edge_info))
    return graph