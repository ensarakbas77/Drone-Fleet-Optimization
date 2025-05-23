import random
import math
from project.csp import check_battery, check_weight, check_nofly_zones, check_time_window
from project.astar import astar

# 1️⃣ Rastgele başlangıç popülasyonu üretir
def initialize_population(drones, deliveries, pop_size):
    population = []
    for _ in range(pop_size):
        individual = {}  # her birey: drone_id → teslimat ID listesi
        for drone in drones:
            assigned = random.sample(deliveries, k=random.randint(1, 3))  # rastgele 1-3 teslimat
            individual[drone['id']] = [d['id'] for d in assigned]
        population.append(individual)
    return population

# 2️⃣ Fitness fonksiyonu: bireyin başarımını puanla
def evaluate(individual, drones, deliveries, graph, positions, noflyzones):
    total_score = 0
    visited_deliveries = set()

    for drone_id, delivery_ids in individual.items():
        drone = next(d for d in drones if d['id'] == drone_id)
        current_pos = drone['start_pos']
        battery = drone['battery']

        for deliv_id in delivery_ids:
            if deliv_id in visited_deliveries:
                total_score -= 100  # aynı teslimat 2 drone tarafından alınmış → ceza
                continue

            delivery = next(d for d in deliveries if d['id'] == deliv_id)
            visited_deliveries.add(deliv_id)

            # Bu teslimat için geçici bir grafik oluşturuluyor
            temp_graph = {
                0: [(1, {
                    "distance": euclidean(current_pos, delivery['pos']),
                    "weight": delivery['weight'],
                    "priority": delivery['priority']
                })],
                1: []
            }
            temp_positions = {
                0: current_pos,
                1: delivery['pos']
            }

            # A* ile yol bulunur
            path, cost = astar(temp_graph, 0, 1, temp_positions, drone, noflyzones)

            if not path:
                total_score -= 50  # yol bulunamadıysa ceza ver
                continue

            # CSP kısıtları kontrol edilir
            valid_battery = check_battery(drone, path, temp_graph)
            valid_weight = check_weight(drone, delivery)
            valid_time = check_time_window(delivery, "13:00")  # sabit saat ile kontrol
            valid_flight = check_nofly_zones(
                [temp_positions[n] for n in path], noflyzones, "13:00"
            )

            if all([valid_battery, valid_weight, valid_time, valid_flight]):
                total_score += 100 - cost  # geçerliyse puan ver, maliyeti çıkar
                current_pos = delivery['pos']  # drone'un yeni pozisyonu
                battery -= cost  # batarya düşürülür
            else:
                total_score -= 50  # herhangi bir CSP ihlali varsa ceza ver

    return total_score

# Öklidyen mesafe hesaplar
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# 3️⃣ En iyi bireyleri seç
def selection(population, scores, num_parents):
    paired = list(zip(scores, population))
    paired.sort(reverse=True, key=lambda x: x[0])
    return [p[1] for p in paired[:num_parents]]

# 4️⃣ Çaprazlama: 2 ebeveynden çocuk üret
def crossover(p1, p2):
    child = {}
    for drone_id in p1:
        child[drone_id] = random.choice([p1[drone_id], p2[drone_id]])
    return child

# 5️⃣ Mutasyon: rastgele bir drone'un görevini değiştir
def mutate(individual, deliveries):
    drone_id = random.choice(list(individual.keys()))
    if individual[drone_id]:
        new_deliv = random.choice(deliveries)['id']
        individual[drone_id] = [new_deliv]
    return individual

# 🔁 GA ana döngüsü
def run_ga(drones, deliveries, graph, positions, noflyzones, gen=10, pop_size=10):
    population = initialize_population(drones, deliveries, pop_size)

    for i in range(gen):
        scores = [evaluate(ind, drones, deliveries, graph, positions, noflyzones) for ind in population]
        parents = selection(population, scores, num_parents=2)
        new_population = parents.copy()

        while len(new_population) < pop_size:
            child = crossover(random.choice(parents), random.choice(parents))
            if random.random() < 0.3:  # %30 ihtimalle mutasyon yapılır
                child = mutate(child, deliveries)
            new_population.append(child)

        population = new_population
        print(f"🧬 Gen {i+1} | En iyi skor: {max(scores)}")

    best_score = max(scores)
    best_index = scores.index(best_score)
    return population[best_index], best_score
