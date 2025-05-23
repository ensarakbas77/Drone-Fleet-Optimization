import sys
from utils.data_loader import load_json_lines
from project.graph_builder import build_graph
from project.genetic_algorithm import run_ga
from utils.visualizer import plot_delivery_routes

def main():
    # Komut satırından senaryo adı alınır (senaryo1 / senaryo2)
    senaryo = sys.argv[1] if len(sys.argv) > 1 else "senaryo1"

    print(f"🚀 Drone Teslimat Planlayıcı çalışıyor → {senaryo}")

    # 1. Verileri yükle
    drones = load_json_lines(f"data/drones_{senaryo}.txt")
    deliveries = load_json_lines(f"data/deliveries_{senaryo}.txt")
    noflyzones = load_json_lines(f"data/noflyzones_{senaryo}.txt")

    # 2. Konumlar
    positions = {d['id']: d['pos'] for d in deliveries}

    # 3. Graf oluştur
    graph = build_graph(deliveries)

    # 4. Genetik algoritma
    best_solution, best_score = run_ga(
        drones, deliveries, graph, positions, noflyzones,
        gen=10, pop_size=8
    )

    # 5. Sonuçlar
    print("\n🧬 En iyi plan:")
    for drone_id, delivery_ids in best_solution.items():
        print(f"  Drone {drone_id} → Teslimatlar: {delivery_ids}")
    print(f"📊 En iyi skor: {round(best_score, 2)}")

    # 6. Görselleştirme
    plot_delivery_routes(drones, deliveries, best_solution, noflyzones)

if __name__ == "__main__":
    main()
