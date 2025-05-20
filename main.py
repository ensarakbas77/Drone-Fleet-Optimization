from data_generator import generate_random_drones, generate_random_deliveries
from constraint_checker import check_constraints
from ga_optimizer import genetic_algorithm
from visualizer import plot_route

print("Genetik algoritma başlatıldı.")

# Rastgele 1 drone ve 5 teslimat üret
drones = generate_random_drones(1)
deliveries = generate_random_deliveries(5)
nofly_zones = generate_random_nofly_zones(1)


drone = drones[0]

# Genetik algoritmayı çalıştır
best_route, best_fitness = genetic_algorithm(drone, deliveries)

# En iyi rotayı ve detaylarını yazdır
print("En iyi rota (teslimat ID sırası):", best_route)
print("Fitness değeri:", best_fitness)

# Rota detaylarını yazdır
total_distance = 0
current_pos = drone.start_pos
total_weight = 0

for idx in best_route:
    delivery = deliveries[idx]
    print(f"- Teslimat {idx}: hedef={delivery.pos}, ağırlık={delivery.weight}")
    dist = ((current_pos[0] - delivery.pos[0])**2 + (current_pos[1] - delivery.pos[1])**2)**0.5
    total_distance += dist
    total_weight += delivery.weight
    current_pos = delivery.pos

print("Toplam mesafe:", total_distance)
print("Toplam ağırlık:", total_weight)
print("Drone kapasitesi:", drone.max_weight)
print("Drone bataryası:", drone.battery)

# Uygunluk kontrolü
if total_distance > drone.battery:
    print("❌ Batarya yetersiz!")
elif total_weight > drone.max_weight:
    print("❌ Taşıma kapasitesi yetersiz!")
else:
    print("✅ Rota uygundur.")

# Rota görselleştirme
plot_route(drone, deliveries, best_route)
