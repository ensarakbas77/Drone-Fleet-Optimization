import json

def load_drones(file_path):
    with open(file_path, 'r') as f:
        return [json.loads(line) for line in f]


drones = load_drones("data/drones_senaryo2.txt")
no_fly_zone = load_drones("data/noflyzones_senaryo1.txt")
deliveries = load_drones("data/deliveries_senaryo1.txt")
print(drones)


