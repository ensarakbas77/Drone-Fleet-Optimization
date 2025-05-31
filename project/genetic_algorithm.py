import random
import math
from project.csp import check_battery, check_weight, check_nofly_zones, check_time_window
from project.astar import astar
from utils.constants import (
    MAX_DELIVERIES_PER_DRONE,
    PENALTY_NO_ROUTE,
    MUTATION_RATE,
    CHARGE_TIME_HOURS,
    FITNESS_DELIVERY_REWARD,
    FITNESS_ENERGY_PENALTY,
    FITNESS_VIOLATION_PENALTY,
)

# 🚀 Öklidyen mesafe
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# 1️⃣ Popülasyonu başlat
def initialize_population(drones, deliveries, pop_size):
    population = []
    for _ in range(pop_size):
        available_deliveries = deliveries.copy()
        random.shuffle(available_deliveries)

        individual = {drone['id']: [] for drone in drones}

        for delivery in available_deliveries:
            assigned = False
            drone_ids = [d['id'] for d in drones]
            random.shuffle(drone_ids)

            for drone_id in drone_ids:
                if len(individual[drone_id]) < MAX_DELIVERIES_PER_DRONE:
                    individual[drone_id].append(delivery['id'])
                    assigned = True
                    break
            if not assigned:
                continue

        population.append(individual)
    return population

# 2️⃣ Fitness hesaplama
def evaluate(individual, drones, deliveries, graph, positions, noflyzones):
    total_score = 0
    visited_deliveries = set()
    energy_cost = 0
    penalty_count = 0
    valid_count = 0

    for drone_id, delivery_ids in individual.items():
        drone = next(d for d in drones if d['id'] == drone_id)
        current_pos = drone['start_pos']
        battery = drone['battery']
        speed = drone['speed']
        current_time = 13.00

        delivery_ids = sorted(
            delivery_ids,
            key=lambda d_id: next(d['priority'] for d in deliveries if d['id'] == d_id),
            reverse=True
        )

        #Teslimat yalnızca bir kez bir drone tarafından alınır.
        for deliv_id in delivery_ids:
            if deliv_id in visited_deliveries:
                continue
            visited_deliveries.add(deliv_id)

            delivery = next(d for d in deliveries if d['id'] == deliv_id)

            temp_graph = {
                0: [(1, {
                    "distance": euclidean(current_pos, delivery['pos']),
                    "weight": delivery['weight'],
                    "priority": delivery['priority']
                })],
                1: []
            }
            temp_positions = {0: current_pos, 1: delivery['pos']}

            path, cost = astar(temp_graph, 0, 1, temp_positions, drone, noflyzones)

            if not path:
                total_score -= PENALTY_NO_ROUTE
                penalty_count += 1
                continue

            if battery < cost:
                current_time += CHARGE_TIME_HOURS
                battery = drone['battery']

            arrival_time = current_time + (cost / speed)
            total_minutes = int(arrival_time * 60)
            hours = (total_minutes // 60) % 24
            minutes = total_minutes % 60
            arrival_str = f"{hours:02d}:{minutes:02d}"

            valid_battery = check_battery(drone, path, temp_graph)
            valid_weight = check_weight(drone, delivery)
            valid_time = check_time_window(delivery, arrival_str)
            valid_flight = check_nofly_zones(
                [temp_positions[n] for n in path], noflyzones, arrival_str
            )

            if all([valid_battery, valid_weight, valid_time, valid_flight]):
                valid_count += 1
                energy_cost += cost
                current_pos = delivery['pos']
                battery -= cost
                current_time = arrival_time
            else:
                total_score -= PENALTY_NO_ROUTE
                penalty_count += 1

    fitness = (valid_count * FITNESS_DELIVERY_REWARD) \
        - (energy_cost * FITNESS_ENERGY_PENALTY) \
        - (penalty_count * FITNESS_VIOLATION_PENALTY)

    return fitness

# 3️⃣ Seçim
def selection(population, scores, num_parents):
    paired = list(zip(scores, population))
    paired.sort(reverse=True, key=lambda x: x[0])
    return [p[1] for p in paired[:num_parents]]

# 4️⃣ Çaprazlama
def crossover(p1, p2):
    child = {}
    all_assigned = set()
    for drone_id in p1:
        choices = [lst for lst in [p1[drone_id], p2[drone_id]] if lst]
        selected = random.choice(choices) if choices else []
        filtered = [d for d in selected if d not in all_assigned]
        child[drone_id] = filtered[:MAX_DELIVERIES_PER_DRONE]
        all_assigned.update(filtered)
    return child

# 5️⃣ Mutasyon
def mutate(individual, deliveries):
    new_individual = {k: v.copy() for k, v in individual.items()}
    all_deliv_ids = set(d['id'] for d in deliveries)
    used_ids = set(did for lst in new_individual.values() for did in lst)
    remaining = list(all_deliv_ids - used_ids)

    if not remaining:
        return new_individual

    drone_id = random.choice(list(new_individual.keys()))
    new_id = random.choice(remaining)
    if len(new_individual[drone_id]) < MAX_DELIVERIES_PER_DRONE:
        new_individual[drone_id].append(new_id)
    else:
        replace_idx = random.randint(0, MAX_DELIVERIES_PER_DRONE - 1)
        new_individual[drone_id][replace_idx] = new_id
    return new_individual

# 🔁 GA döngüsü
def run_ga(drones, deliveries, graph, positions, noflyzones, gen=10, pop_size=10):
    population = initialize_population(drones, deliveries, pop_size)
    history = []

    for i in range(gen):
        scores = [evaluate(ind, drones, deliveries, graph, positions, noflyzones) for ind in population]
        parents = selection(population, scores, num_parents=2)
        new_population = parents.copy()

        while len(new_population) < pop_size:
            child = crossover(random.choice(parents), random.choice(parents))
            if random.random() < MUTATION_RATE:
                child = mutate(child, deliveries)
            new_population.append(child)

        population = new_population
        best = max(scores)
        avg = sum(scores) / len(scores)
        history.append(best)
        print(f"Gen {i+1} | En iyi: {best} | Ortalama: {avg:.2f}")

    best_score = max(scores)
    best_index = scores.index(best_score)
    return population[best_index], best_score, history
