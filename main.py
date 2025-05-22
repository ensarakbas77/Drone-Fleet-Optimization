from utils.data_loader import load_json_lines
from project.graph_builder import build_graph
from project.genetic_algorithm import run_ga
from utils.visualizer import plot_delivery_routes

 # 1. Verileri yükle
drones = load_json_lines("data/drones_senaryo1.txt")
deliveries = load_json_lines("data/deliveries_senaryo1.txt")
noflyzones = load_json_lines("data/noflyzones_senaryo1.txt")
# 2. Her teslimat noktasının konumlarını al
positions = {d['id']: d['pos'] for d in deliveries}
# Geçici çözüm: drone'lara bir başlangıç noktası (teslimatlardan biri) ekle
for i, drone in enumerate(drones):
    drone['start_node'] = deliveries[i % len(deliveries)]['id']
# 3. Grafı oluştur
graph = build_graph(deliveries)
# 4. Genetik algoritmayı çalıştır
best_solution, best_score = run_ga(
    drones, deliveries, graph, positions, noflyzones,
    gen=10, pop_size=8
)
print("\n🧬 En iyi plan:")
for drone_id, delivery_ids in best_solution.items():
    print(f"Drone {drone_id} → Teslimatlar: {delivery_ids}")
print(f"📊 En iyi skor: {best_score}")

# GA sonrası:
plot_delivery_routes(drones, deliveries, best_solution, noflyzones)
