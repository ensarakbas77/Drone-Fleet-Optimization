import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.cm as cm
import numpy as np

def plot_delivery_routes(drones, delivery_points, paths, noflyzones=None):
    plt.figure(figsize=(12, 10))
    ax = plt.gca()

    # 1. Tüm teslimat noktalarını çiz (mavi daire + ID)
    for dp in delivery_points:
        x, y = dp["pos"]
        plt.plot(x, y, 'o', color='deepskyblue', markersize=7, zorder=3)
        plt.text(x + 1.2, y + 1.2, str(dp["id"]), fontsize=9, color='black')

    # 2. No-Fly Zones (açık kırmızı şeffaf çokgen)
    if noflyzones:
        for zone in noflyzones:
            poly = Polygon(zone['coordinates'], closed=True, color='lightcoral', alpha=0.3, zorder=1)
            ax.add_patch(poly)

    # 3. Her drone için ayrı renk ve rota çizimi
    color_map = cm.get_cmap('tab10')
    for i, drone in enumerate(drones):
        drone_id = drone['id']
        start = drone['start_pos']
        assigned_ids = paths.get(drone_id, [])
        color = color_map(i % 10)

        # Başlangıç noktasını çiz (kare, kalın)
        plt.plot(start[0], start[1], marker='s', markersize=9, color=color, label=f"Drone {drone_id}", zorder=4)

        # Rota noktalarını sıraya diz: start + teslimatlar
        route = [start] + [dp["pos"] for dp in delivery_points if dp["id"] in assigned_ids]

        # Her iki nokta arası çizgi ve yön oku
        for j in range(len(route) - 1):
            x1, y1 = route[j]
            x2, y2 = route[j+1]

            # Rota çizgisi
            plt.plot([x1, x2], [y1, y2], color=color, linewidth=2, alpha=0.9, zorder=2)

            # Küçük yön oku (uçtan uca değil, ortadan)
            dx = x2 - x1
            dy = y2 - y1
            plt.arrow(x1 + dx/2, y1 + dy/2, dx * 0.01, dy * 0.01,
                      head_width=1.3, head_length=2.0, fc=color, ec=color, zorder=5)

    # 4. Grafik ayarları
    plt.title("Drone Teslimat Rotaları (Harita Benzeri Görselleştirme)", fontsize=14)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.show()
