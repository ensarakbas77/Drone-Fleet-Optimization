import folium
from folium import plugins
import random

# Renk paleti
COLORS = ['blue', 'green', 'red', 'purple', 'orange', 'darkred', 'cadetblue']

def plot_folium_map(drones, deliveries, solution, noflyzones, filename="drone_routes.html"):
    # Başlangıç merkezi
    center = [sum(d["pos"][1] for d in deliveries)/len(deliveries),
              sum(d["pos"][0] for d in deliveries)/len(deliveries)]
    m = folium.Map(location=center, zoom_start=15)

    # No-fly zones çiz
    for zone in noflyzones:
        folium.Polygon(
            locations=[(lat, lon) for lon, lat in zone["coordinates"]],
            color='red',
            fill=True,
            fill_opacity=0.3
        ).add_to(m)

    # Teslimat noktaları
    for d in deliveries:
        folium.CircleMarker(
            location=(d["pos"][1], d["pos"][0]),
            radius=5,
            color='black',
            fill=True,
            fill_opacity=1,
            popup=f'Teslimat {d["id"]}'
        ).add_to(m)

    # Rotaları çiz
    for i, (drone_id, route) in enumerate(solution.items()):
        drone = next(d for d in drones if d["id"] == drone_id)
        color = COLORS[i % len(COLORS)]
        points = [drone["start_pos"]] + [next(d["pos"] for d in deliveries if d["id"] == rid) for rid in route]
        folium.Marker(
            location=(points[0][1], points[0][0]),
            icon=folium.Icon(color="gray", icon="paper-plane", prefix="fa"),
            popup=f"Drone {drone_id} Başlangıç"
        ).add_to(m)
        folium.PolyLine(
            locations=[(y, x) for x, y in points],
            color=color,
            weight=3,
            popup=f"Drone {drone_id} rotası"
        ).add_to(m)

    m.save(filename)
    print(f"✅ Harita oluşturuldu: {filename}")
