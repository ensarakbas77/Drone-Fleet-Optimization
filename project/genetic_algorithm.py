import random
from project.csp import check_battery, check_weight, check_nofly_zones, check_time_window
from project.astar import astar

# 1️⃣ Popülasyon oluştur
def initialize_population(drones, deliveries, pop_size):
    population = []
    for _ in range(pop_size):
        individual = {}
        for drone in drones:
            assigned = random.sample(deliveries, k=random.randint(1, 3))
            individual[drone['id']] = [d['id'] for d in assigned]
        population.append(individual)
    return population

# 2️⃣ Fitness hesapla
def evaluate(individual, drones, deliveries, graph, positions, noflyzones):
    total_score = 0
    visited_deliveries = set()

    for drone_id, delivery_ids in individual.items():
        drone = next(d for d in drones if d['id'] == drone_id)

        for deliv_id in delivery_ids:
            if deliv_id in visited_deliveries:
                total_score -= 100  # ceza: aynı teslimat tekrarlandı
                continue

            visited_deliveries.add(deliv_id)
            delivery = next(d for d in deliveries if d['id'] == deliv_id)

            path, cost = astar(graph, drone['start_node'], deliv_id, positions)
            if path is None:
                continue

            valid_battery = check_battery(drone, path, graph)
            valid_weight = check_weight(drone, delivery)
            valid_time = check_time_window(delivery, "13:00")
            valid_flight = check_nofly_zones([positions[n] for n in path], noflyzones, "13:00")

            if all([valid_battery, valid_weight, valid_time, valid_flight]):
                total_score += 100
                total_score -= cost
            else:
                total_score -= 50
    return total_score


# 3️⃣ Seçim
def selection(population, scores, num_parents):
    paired = list(zip(scores, population))
    paired.sort(reverse=True, key=lambda x: x[0])
    return [p[1] for p in paired[:num_parents]]

# 4️⃣ Çaprazlama
def crossover(p1, p2):
    child = {}
    for drone_id in p1:
        if random.random() < 0.5:
            child[drone_id] = p1[drone_id]
        else:
            child[drone_id] = p2[drone_id]
    return child

# 5️⃣ Mutasyon
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
            if random.random() < 0.3:
                child = mutate(child, deliveries)
            new_population.append(child)

        population = new_population
        print(f"Gen {i+1} En iyi skor: {max(scores)}")

    # En iyi birey:
    best_score = max(scores)
    best_index = scores.index(best_score)
    return population[best_index], best_score
