import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.cm as cm
import numpy as np
import os
import math

def euclidean(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def plot_delivery_routes(drones, delivery_points, paths, noflyzones=None, save_as_image=True):
    plt.figure(figsize=(14, 12))  # daha geniş çizim alanı
    ax = plt.gca()

    # 1. Tüm teslimat noktalarını çiz (mavi daire + ID)
    for dp in delivery_points:
        x, y = dp["pos"]
        plt.plot(x, y, 'o', color='deepskyblue', markersize=7, zorder=3)
        plt.text(x + 1.2, y + 1.2, str(dp["id"]), fontsize=8, color='black')

    # 2. No-Fly Zones (şeffaf salmon renkli çokgen)
    if noflyzones:
        for zone in noflyzones:
            poly = Polygon(zone['coordinates'], closed=True, color='salmon', alpha=0.2, zorder=1)
            ax.add_patch(poly)

    # 3. Her drone için rota çizimi
    color_map = cm.get_cmap('tab10')
    for i, drone in enumerate(drones):
        drone_id = drone['id']
        start = drone['start_pos']
        assigned_ids = paths.get(drone_id, [])
        color = color_map(i % 10)

        # Başlangıç noktası
        plt.plot(start[0], start[1], marker='s', markersize=9, color=color, label=f"Drone {drone_id}", zorder=4)

        # Teslimat noktaları
        route = [start] + [dp["pos"] for dp in delivery_points if dp["id"] in assigned_ids]
        id_route = [None] + [dp["id"] for dp in delivery_points if dp["id"] in assigned_ids]

        total_distance = 0

        for j in range(len(route) - 1):
            x1, y1 = route[j]
            x2, y2 = route[j+1]
            seg_distance = euclidean((x1, y1), (x2, y2))
            total_distance += seg_distance

            plt.plot([x1, x2], [y1, y2], color=color, linewidth=2, alpha=0.9, zorder=2)

            dx = x2 - x1
            dy = y2 - y1
            plt.arrow(x1 + dx/2, y1 + dy/2, dx * 0.01, dy * 0.01,
                      head_width=1.3, head_length=2.0, fc=color, ec=color, zorder=5)

            if j + 1 < len(id_route) and id_route[j+1] is not None:
                plt.text(x2 + 1.5, y2 + 1.5, f"{id_route[j+1]} ({j})", fontsize=7, color=color)

        if len(route) > 1:
            plt.text(route[-1][0] + 2, route[-1][1] + 2,
                     f"Toplam: {round(total_distance, 1)}", color=color, fontsize=8)

    # 4. Ayarlar
    plt.title("Drone Teslimat Rotaları", fontsize=14)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend(loc="upper left")
    plt.tight_layout(pad=2.0)
    plt.show()
