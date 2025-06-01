import folium

COLORS = ["blue", "green", "red", "purple", "orange", "darkred", "cadetblue"]

def plot_routes_with_folium(drones, deliveries, solution, noflyzones, save_path="drone_routes.html"):
    # Harita merkezini belirlemek için tüm koordinatların ortalamasını al
    all_coords = [d["pos"] for d in deliveries]
    center_lat = sum(p[1] for p in all_coords) / len(all_coords)
    center_lon = sum(p[0] for p in all_coords) / len(all_coords)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

    # No-Fly Zone bölgeleri (düzgün sıralı lat-lon olacak)
    for zone in noflyzones:
        zone_coords = [(coord[1], coord[0]) for coord in zone["coordinates"]]  # (y, x)
        folium.Polygon(
            locations=zone_coords,
            color='red',
            fill=True,
            fill_opacity=0.3,
            tooltip=f"No-Fly Zone {zone['id']}"
        ).add_to(m)

    # Teslimat noktaları
    for delivery in deliveries:
        lat, lon = delivery["pos"][1], delivery["pos"][0]
        folium.CircleMarker(
            location=(lat, lon),
            radius=4,
            color='black',
            fill=True,
            fill_opacity=1,
            popup=f"Teslimat {delivery['id']}"
        ).add_to(m)

    # Drone rotaları
    for idx, (drone_id, delivery_ids) in enumerate(solution.items()):
        drone = next(d for d in drones if d["id"] == drone_id)
        color = COLORS[idx % len(COLORS)]

        # Rota koordinatlarını al (başlangıç + teslimatlar)
        points = [drone["start_pos"]] + [next(d["pos"] for d in deliveries if d["id"] == did) for did in delivery_ids]
        path = [(p[1], p[0]) for p in points]  # (lat, lon)

        # Başlangıç işareti
        folium.Marker(
            location=path[0],
            icon=folium.Icon(color=color),
            popup=f"Drone {drone_id} Başlangıç"
        ).add_to(m)

        # Çizgi (rota)
        folium.PolyLine(
            locations=path,
            color=color,
            weight=3,
            opacity=0.8,
            popup=f"Drone {drone_id} rotası"
        ).add_to(m)

    # Haritayı kaydet
    m.save(save_path)
    print(f"📍 Harita oluşturuldu: {save_path}")
