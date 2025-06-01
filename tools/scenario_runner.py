from tools.data_generator import generate_random_drones, generate_random_deliveries, generate_random_nofly_zones
from project.astar import astar
import math

def build_graph(deliveries):
    graph = {}
    for i, src in enumerate(deliveries):
        graph[i] = []
        for j, dst in enumerate(deliveries):
            if i != j:
                distance = math.sqrt((src.pos[0] - dst.pos[0])**2 + (src.pos[1] - dst.pos[1])**2)
                info = {
                    "distance": distance,
                    "weight": dst.weight,
                    "priority": dst.priority
                }
                graph[i].append((j, info))
    return graph

def delivery_positions(deliveries):
    return {i: delivery.pos for i, delivery in enumerate(deliveries)}

def nofly_dict_list(zones):
    return [vars(z) for z in zones]

def run_scenario():
    drones = generate_random_drones(3)
    deliveries = generate_random_deliveries(5)
    nofly_zones = generate_random_nofly_zones(2)

    graph = build_graph(deliveries)
    positions = delivery_positions(deliveries)

    current_time = "10:00"  # 🕒 Simülasyon zamanı burada tanımlanır

    for i, drone in enumerate(drones):
        print(f"\n🚁 Drone #{i+1}")
        path, cost = astar(
            graph=graph,
            start_id=0,
            goal_id=len(deliveries)-1,
            node_positions=positions,
            drone=vars(drone),
            no_fly_zones=nofly_dict_list(nofly_zones),
            current_time=current_time  # 🆕 parametre burada geçildi
        )

        if path:
            print(f"📦 Rota: {path}")
            print(f"🔋 Toplam Maliyet: {round(cost, 2)}")
        else:
            print("❌ Uygun rota bulunamadı.")


if __name__ == "__main__":
    run_scenario()