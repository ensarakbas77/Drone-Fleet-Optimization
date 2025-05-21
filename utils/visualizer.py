import matplotlib.pyplot as plt

def plot_delivery_routes(drones, delivery_points, paths):
    plt.figure(figsize=(10, 8))

    # Tüm teslimat noktalarını çiz
    for dp in delivery_points:
        x, y = dp["pos"]
        plt.plot(x, y, 'bo')  # mavi daire
        plt.text(x + 0.5, y + 0.5, f"{dp['id']}", fontsize=8)

    # Drone rotalarını çiz
    colors = ['r', 'g', 'm', 'c', 'y', 'k']
    for i, drone in enumerate(drones):
        start = drone['start_pos']
        drone_id = drone['id']
        path = paths.get(drone_id, [])

        # Nokta dizisine çevrilsin
        route = [start] + [dp["pos"] for dp in delivery_points if dp["id"] in path]

        if len(route) > 1:
            xs = [p[0] for p in route]
            ys = [p[1] for p in route]
            plt.plot(xs, ys, color=colors[i % len(colors)], linewidth=2, label=f"Drone {drone_id}")
            plt.scatter(*start, color=colors[i % len(colors)], marker='s')  # drone start konumu

    plt.title("Drone Teslimat Rotaları")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
