from data_generator import generate_random_drones, generate_random_deliveries, generate_random_nofly_zones


drones = generate_random_drones(1)
deliveries = generate_random_deliveries(1)
nofly_zones = generate_random_nofly_zones(1)

for drone in drones:
    print(vars(drone))

for delivery in deliveries:
    print(vars(delivery))

for zone in nofly_zones:
    print(vars(zone))
