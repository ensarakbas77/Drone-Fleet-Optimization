import matplotlib.pyplot as plt
from tools.html_map_generator import plot_folium_map
from utils.folium_visualizer import plot_routes_with_folium
from utils.data_loader import load_json_lines
from project.graph_builder import build_graph
from project.genetic_algorithm import run_ga
from project.astar import astar
from random import randint
from tools.metrics import (
    measure_runtime,
    calculate_delivery_completion,
    estimate_energy,
)
from utils.visualizer import plot_delivery_routes
import heapq

def calculate_total_distance(drone, delivery_ids, deliveries):
    current_pos = drone["start_pos"]
    total_distance = 0
    for deliv_id in delivery_ids:
        delivery = next(d for d in deliveries if d["id"] == deliv_id)
        dx = current_pos[0] - delivery["pos"][0]
        dy = current_pos[1] - delivery["pos"][1]
        distance = (dx**2 + dy**2) ** 0.5
        total_distance += distance
        current_pos = delivery["pos"]
    return total_distance

def create_priority_heap(deliveries):
    heap = []
    for delivery in deliveries:
        heapq.heappush(heap, (-delivery["priority"], delivery["id"], delivery))
    return heap

def display_top_priority_deliveries(deliveries, drones=None, count=None):
    if count is None:
        count = len(drones) if drones else 5
    heap = create_priority_heap(deliveries)
    print("\nEn Acil Teslimatlar (Öncelik Değerine Göre):")
    for _ in range(min(count, len(heap))):
        _, _, delivery = heapq.heappop(heap)
        print(f"  Teslimat {delivery['id']} → Öncelik: {delivery['priority']}")

def main():
    senaryo = "veriseti" 
    print(f"\n🚀 Drone Teslimat Planlayıcı başlatıldı → {senaryo}")

    drones = load_json_lines(f"data/drones_{senaryo}.txt")
    deliveries = load_json_lines(f"data/deliveries_{senaryo}.txt")
    noflyzones = load_json_lines(f"data/noflyzones_{senaryo}.txt")

    positions = {d["id"]: d["pos"] for d in deliveries}

    for i, drone in enumerate(drones):
        drone["start_pos"] = deliveries[i % len(deliveries)]["pos"]

    graph = build_graph(deliveries)

    # Öncelikli teslimatların gösterimi
    display_top_priority_deliveries(deliveries, drones=drones)

    (best_solution, best_score, history), duration = measure_runtime(
        run_ga, drones, deliveries, graph, positions, noflyzones, gen=10, pop_size=8
    )

    print("\nEn iyi plan:")
    for drone_id, delivery_ids in best_solution.items():
        print(f"\nDrone {drone_id} → Teslimatlar: {delivery_ids}")
        drone = next(d for d in drones if d["id"] == drone_id)
        current_pos = drone["start_pos"]
        battery = drone["battery"]
        total_battery = drone["battery"]
        total_cost = 0

        for deliv_id in delivery_ids:
            delivery = next(d for d in deliveries if d["id"] == deliv_id)
            dx = delivery["pos"][0] - current_pos[0]
            dy = delivery["pos"][1] - current_pos[1]
            distance = (dx**2 + dy**2) ** 0.5
            cost = distance * (1 + delivery["weight"])
            total_cost += cost
            battery -= cost
            current_pos = delivery["pos"]

        print(f"   Batarya: {round(battery, 2)} / {total_battery}")
        print(f"   Toplam Maliyet: {round(total_cost, 2)}")

    print(f"\nEn iyi skor: {round(best_score, 2)}")
    print(f"GA çalışma süresi: {duration:.2f} saniye")

    completion_rate = calculate_delivery_completion(best_solution, len(deliveries))
    avg_energy = estimate_energy(best_solution, drones, deliveries)

    print(f"Teslimat tamamlama oranı: %{completion_rate:.2f}")
    print(f"Ortalama enerji tüketimi: {round(avg_energy, 2)} birim")

    try:
        plot_delivery_routes(drones, deliveries, best_solution, noflyzones)
    except:
        print("Görselleştirme yapılamadı (visualizer eksik olabilir).")

    start_id = deliveries[0]["id"]
    goal_id = deliveries[-1]["id"]
    current_time = f"{randint(9, 17)}:{randint(0, 59):02d}"

    path, cost = astar(
        graph=graph,
        start_id=start_id,
        goal_id=goal_id,
        node_positions=positions,
        drone=drones[0],
        no_fly_zones=noflyzones,
        current_time=current_time  
    )

    try:
        plot_routes_with_folium(drones, deliveries, best_solution, noflyzones)
    except Exception as e:
        print("Folium haritası oluşturulamadı:", e)

    print("\n=== A* (tekli teslimat) testi ===")
    if path:
        drone = drones[0]
        distance = cost / (1 + deliveries[-1]["weight"])
        speed = drone["speed"]
        eta_hour = int((distance / speed + 13.0) % 24)
        eta_min = int(((distance / speed) * 60) % 60)
        print(f"🚁 Drone 0 ► Teslimat {goal_id}")
        print(f"Yol       : D{start_id} → D{goal_id}")
        print(f"Mesafe    : {round(distance, 1)} m")
        print(f"Maliyet   : {round(cost, 1)}")
        print(f"ETA       : {eta_hour:02d}:{eta_min:02d}")
        print(f"Batarya   : {round(drone['battery'] - cost, 1)} / {drone['battery']} mAh")
    else:
        print("A* algoritması uygun rota bulamadı.")

if __name__ == "__main__":
    main()
