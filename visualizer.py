
import matplotlib.pyplot as plt

def plot_route(drone, deliveries, route):
    fig, ax = plt.subplots()
    start = drone.start_pos
    ax.plot(start[0], start[1], 'go', label='Başlangıç (Drone)')

    x_vals = [start[0]]
    y_vals = [start[1]]

    for idx in route:
        d = deliveries[idx]
        x_vals.append(d.pos[0])
        y_vals.append(d.pos[1])
        ax.plot(d.pos[0], d.pos[1], 'bo')
        ax.text(d.pos[0] + 1, d.pos[1] + 1, f"#{idx}", fontsize=9)

    ax.plot(x_vals, y_vals, 'r--', label='Rota')
    ax.set_title("Teslimat Rotası (Genetik Algoritma)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.grid(True)
    plt.show()
