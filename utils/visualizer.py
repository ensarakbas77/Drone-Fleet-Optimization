import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.cm as cm
import math

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def plot_delivery_routes(drones, deliveries, paths, noflyzones=None):
    plt.figure(figsize=(14, 12))
    ax = plt.gca()

    all_assigned_ids = set()
    for dlist in paths.values():
        all_assigned_ids.update(dlist)

    # Teslimat noktaları
    for dp in deliveries:
        x, y = dp["pos"]
        if dp["id"] in all_assigned_ids:
            plt.plot(x, y, 'o', color='deepskyblue', markersize=7, zorder=3)
        else:
            plt.plot(x, y, 'x', color='gray', markersize=8, zorder=3)
            plt.text(x + 1.5, y + 1.5, f"{dp['id']} (atanmadı)", fontsize=7, color='gray')
            continue
        plt.text(x + 1.0, y + 1.0, f"{dp['id']}", fontsize=8, color='black')

    # No-fly zones
    if noflyzones:
        for zone in noflyzones:
            poly = Polygon(zone['coordinates'], closed=True, color='salmon', alpha=0.25, zorder=1)
            ax.add_patch(poly)

    # Drone rotalari ve toplam mesafe etiketi
    color_map = cm.get_cmap('tab10')
    for i, drone in enumerate(drones):
        drone_id = drone['id']
        color = color_map(i % 10)
        assigned_ids = paths.get(drone_id, [])
        start = drone['start_pos']

        # Baslangic karesi
        plt.plot(start[0], start[1], marker='s', markersize=10, color=color, label=f"Drone {drone_id}", zorder=4)

        # Rota olustur
        route = [start]
        for deliv_id in assigned_ids:
            delivery = next(d for d in deliveries if d["id"] == deliv_id)
            route.append(delivery["pos"])

        # Rota cizimi + toplam mesafe hesaplama
        total_distance = 0
        for j in range(len(route) - 1):
            x1, y1 = route[j]
            x2, y2 = route[j+1]
            seg_distance = euclidean((x1, y1), (x2, y2))
            total_distance += seg_distance
            plt.plot([x1, x2], [y1, y2], color=color, linewidth=2.5, alpha=0.85, zorder=2)

        # Toplam mesafe etiketi
        if len(route) > 1:
            x_end, y_end = route[-1]
            plt.text(x_end + 2, y_end + 2,
                     f"Toplam: {round(total_distance, 1)}", fontsize=9, fontweight='bold', color=color)

    # Grafik ayarlari
    plt.title("Drone Teslimat Rotalari", fontsize=14)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend(loc="upper left")
    plt.tight_layout(pad=2.0)
    plt.show()