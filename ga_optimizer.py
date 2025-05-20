
import random
import copy

def calculate_fitness(route, drone, deliveries):
    total_distance = 0
    total_weight = 0

    current_pos = drone.start_pos
    for delivery_id in route:
        delivery = deliveries[delivery_id]
        dist = ((current_pos[0] - delivery.pos[0])**2 + (current_pos[1] - delivery.pos[1])**2)**0.5
        total_distance += dist
        total_weight += delivery.weight
        current_pos = delivery.pos

    if total_weight > drone.max_weight:
        return 0  # kapasiteyi aşarsa geçersiz
    if total_distance > drone.battery:
        return 0  # batarya yetmiyorsa geçersiz

    return 1 / total_distance  # mesafe azsa fitness yüksek

def crossover(parent1, parent2):
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child = [None]*size
    child[a:b] = parent1[a:b]

    fill = [item for item in parent2 if item not in child]
    ptr = 0
    for i in range(size):
        if child[i] is None:
            child[i] = fill[ptr]
            ptr += 1
    return child

def mutate(route, mutation_rate=0.1):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route)-1)
            route[i], route[j] = route[j], route[i]
    return route

def genetic_algorithm(drone, deliveries, population_size=20, generations=100):
    delivery_ids = list(range(len(deliveries)))
    population = [random.sample(delivery_ids, len(delivery_ids)) for _ in range(population_size)]

    for _ in range(generations):
        population.sort(key=lambda x: calculate_fitness(x, drone, deliveries), reverse=True)
        next_gen = population[:2]  # elit bireyler

        while len(next_gen) < population_size:
            parents = random.sample(population[:10], 2)
            child = crossover(parents[0], parents[1])
            child = mutate(child)
            next_gen.append(child)

        population = next_gen

    best_route = population[0]
    best_fitness = calculate_fitness(best_route, drone, deliveries)
    return best_route, best_fitness
