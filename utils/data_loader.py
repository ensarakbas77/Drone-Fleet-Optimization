import json

# Senaryo .txt dosyalarını okur
def load_json_lines(file_path):
    with open(file_path, 'r') as f:
        return [json.loads(line) for line in f]


drones = load_json_lines("data/drones_senaryo1.txt")
no_fly_zone = load_json_lines("data/noflyzones_senaryo1.txt")
deliveries = load_json_lines("data/deliveries_senaryo1.txt")
print(drones)


