from tools.data_generator import generate_random_drones, generate_random_deliveries, generate_random_nofly_zones

"""
data_generator.py dosyası ile üretilen örnek drone, teslimat noktası ve uçuşa yasak bölgelerin özelliklerini (id, ...) listeler
"""
drones = generate_random_drones(10)
deliveries = generate_random_deliveries(50)
nofly_zones = generate_random_nofly_zones(5)

for drone in drones:
    print(vars(drone))

for delivery in deliveries:
    print(vars(delivery))

for zone in nofly_zones:
    print(vars(zone))
