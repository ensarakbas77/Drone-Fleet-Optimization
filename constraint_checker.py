
def check_constraints(drone, delivery, path_cost):
    """
    Teslimatın yapılabilirliğini kontrol eder:
    - Drone kapasitesini aşıyor mu?
    - Batarya yeterli mi?
    """

    violations = []

    if delivery.weight > drone.max_weight:
        violations.append("Ağırlık sınırı aşıldı")

    if path_cost > drone.battery:
        violations.append("Yetersiz batarya")

    return len(violations) == 0, violations
