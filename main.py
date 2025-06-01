import matplotlib.pyplot as plt
from tools.html_map_generator import plot_folium_map
from utils.folium_visualizer import plot_routes_with_folium
from utils.data_loader import load_json_lines
from project.graph_builder import build_graph
from project.genetic_algorithm import run_ga
from project.astar import astar
from tools.metrics import (
    measure_runtime,
    calculate_delivery_completion,
    estimate_energy,
)
from utils.visualizer import plot_delivery_routes


# 🔹 Yeni metrik: Toplam mesafe hesaplayıcı
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


def main():
    senaryo = "senaryo1" 

    print(f"\n🚀 Drone Teslimat Planlayıcı başlatıldı → {senaryo}")

    # 🔹 1. Verileri yükle
    drones = load_json_lines(f"data/drones_{senaryo}.txt")
    deliveries = load_json_lines(f"data/deliveries_{senaryo}.txt")
    noflyzones = load_json_lines(f"data/noflyzones_{senaryo}.txt")

    # 🔹 2. Pozisyonlar
    positions = {d["id"]: d["pos"] for d in deliveries}

    # 🔹 3. Başlangıç konumları
    for i, drone in enumerate(drones):
        drone["start_pos"] = deliveries[i % len(deliveries)]["pos"]

    # 🔹 4. Graf oluştur
    graph = build_graph(deliveries)

    # 🔹 5. Genetik algoritmayı çalıştır
    (best_solution, best_score, history), duration = measure_runtime(
        run_ga, drones, deliveries, graph, positions, noflyzones, gen=10, pop_size=8
    )

    # 🔹 6. Çıktıları yazdır
    print("\n🧬 En iyi plan:")
    for drone_id, delivery_ids in best_solution.items():
        print(f"  Drone {drone_id} → Teslimatlar: {delivery_ids}")

    print(f"\n📊 En iyi skor: {round(best_score, 2)}")
    print(f"⏱️ GA çalışma süresi: {duration:.2f} saniye")

    # 🔹 7. Performans metrikleri
    completion_rate = calculate_delivery_completion(best_solution, len(deliveries))
    avg_energy = estimate_energy(best_solution, drones, deliveries)

    print(f"Teslimat tamamlama oranı: %{completion_rate:.2f}")
    print(f"Ortalama enerji tüketimi: {round(avg_energy, 2)} birim")

    # 🔹 8. Drone bazlı özet
    print("\n📦 Drone Bazlı Rotalar ve Enerji Kullanımı:")
    for drone_id, delivery_ids in best_solution.items():
        drone = next(d for d in drones if d["id"] == drone_id)
        total_distance = calculate_total_distance(drone, delivery_ids, deliveries)
        print(f"  Drone {drone_id}:")
        print(f"    Teslimat Noktaları: {delivery_ids}")
        print(f"    Toplam Mesafe: {round(total_distance, 2)}")
        print(f"    Kullanılan Enerji: {round(total_distance, 2)}")  # Şu an ≈ mesafe

    # 🔹 9. Görselleştirme
    try:
        plot_delivery_routes(drones, deliveries, best_solution, noflyzones)
    except:
        print("Görselleştirme yapılamadı (visualizer eksik olabilir).")


if __name__ == "__main__":
    main()
