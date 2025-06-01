import time

def measure_runtime(func, *args, **kwargs):
    """Verilen fonksiyonu çalıştırır ve çalışma süresini ölçer."""
    start_time = time.time()
    result = func(*args, **kwargs)
    duration = time.time() - start_time
    return result, duration

def calculate_delivery_completion(best_solution, total_deliveries):
    """Tamamlanan teslimatların yüzdesini hesaplar."""
    all_assigned = set()
    for deliveries in best_solution.values():
        all_assigned.update(deliveries)
    return (len(all_assigned) / total_deliveries) * 100

def estimate_energy(best_solution, drones, deliveries):
    """Tahmini toplam enerji tüketimini döner."""
    delivery_lookup = {d['id']: d['pos'] for d in deliveries}
    total_energy = 0
    for drone in drones:
        drone_id = drone['id']
        start = drone['start_pos']
        assigned = best_solution.get(drone_id, [])
        pos = start
        for deliv_id in assigned:
            next_pos = delivery_lookup[deliv_id]
            dist = euclidean(pos, next_pos)
            energy = dist * (1 + 1.0)  # basit model: ağırlık = 1.0
            total_energy += energy
            pos = next_pos
    avg_energy = total_energy / len(drones) if drones else 0
    return avg_energy

def euclidean(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5