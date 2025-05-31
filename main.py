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


def main():
    senaryo = "veriseti"  # "senaryo2" ile değiştirilebilir
    print(f"\nDrone Teslimat Planlayıcı başlatıldı → {senaryo}")

    # 1. Verileri yükle
    drones = load_json_lines(f"data/drones_{senaryo}.txt")
    deliveries = load_json_lines(f"data/deliveries_{senaryo}.txt")
    noflyzones = load_json_lines(f"data/noflyzones_{senaryo}.txt")

    # 2. Pozisyonlar
    positions = {d["id"]: d["pos"] for d in deliveries}

    # 3. Başlangıç konumları ayarlanıyor
    for i, drone in enumerate(drones):
        drone["start_pos"] = deliveries[i % len(deliveries)]["pos"]

    # 4. Graf yapısı
    graph = build_graph(deliveries)

    # 5. Genetik algoritmayı çalıştır ve süresini ölç
    (best_solution, best_score, history), duration = measure_runtime(
        run_ga, drones, deliveries, graph, positions, noflyzones, gen=10, pop_size=8
    )

    # 6. Sonuçları yazdır
    print("\nEn iyi plan:")
    for drone_id, delivery_ids in best_solution.items():
        print(f"  Drone {drone_id} → Teslimatlar: {delivery_ids}")
    print(f"\nEn iyi skor: {round(best_score, 2)}")
    print(f"GA çalışma süresi: {duration:.2f} saniye")

    # 7. Performans metrikleri
    completion_rate = calculate_delivery_completion(best_solution, len(deliveries))
    avg_energy = estimate_energy(best_solution, drones, deliveries)

    print(f"Teslimat tamamlama oranı: %{completion_rate:.2f}")
    print(f"Ortalama enerji tüketimi: {round(avg_energy, 2)} birim")

    # 9. Görselleştirme
    try:
        plot_delivery_routes(drones, deliveries, best_solution, noflyzones)
    except:
        print("Görselleştirme yapılamadı (visualizer eksik olabilir).")



if __name__ == "__main__":
    main()
