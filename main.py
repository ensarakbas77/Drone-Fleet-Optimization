from utils.data_loader import load_json_lines
from project.graph_builder import build_graph
from project.genetic_algorithm import run_ga
from utils.visualizer import plot_delivery_routes

def main():
    # 🔧 Buradan senaryoyu sabit olarak ayarlayabilirsin
    senaryo = "senaryo1"  # "senaryo2" ile değiştirilebilir

    print(f"\n🚀 Drone Teslimat Planlayıcı başlatıldı → {senaryo}")

    # 1. Verileri yükle
    drones = load_json_lines(f"data/drones_{senaryo}.txt")
    deliveries = load_json_lines(f"data/deliveries_{senaryo}.txt")
    noflyzones = load_json_lines(f"data/noflyzones_{senaryo}.txt")

    # 2. Teslimat noktalarının pozisyonlarını çıkar
    positions = {d['id']: d['pos'] for d in deliveries}

    # 3. Her drone’a geçici start_node ata (basitçe ilk teslimatlar)
    for i, drone in enumerate(drones):
        drone['start_node'] = deliveries[i % len(deliveries)]['id']

    # 4. Grafı oluştur
    graph = build_graph(deliveries)

    # 5. Genetik algoritmayı çalıştır
    best_solution, best_score = run_ga(
        drones, deliveries, graph, positions, noflyzones,
        gen=10, pop_size=8
    )

    # 6. Sonuçları yazdır
    print("\n🧬 En iyi plan:")
    for drone_id, delivery_ids in best_solution.items():
        print(f"  Drone {drone_id} → Teslimatlar: {delivery_ids}")
    print(f"📊 En iyi skor: {round(best_score, 2)}")

    # 7. Görselleştirme
    plot_delivery_routes(drones, deliveries, best_solution, noflyzones)

if __name__ == "__main__":
    main()
