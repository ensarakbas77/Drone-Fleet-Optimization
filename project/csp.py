import math
from datetime import datetime
from datetime import datetime, timedelta

# Yardımcı: Euclidean mesafe
def euclidean(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# 1. Batarya kontrolü: drone bataryası bu rotayı uçmaya yeter mi?
def check_battery(drone, path, graph):
    total_cost = 0
    for i in range(len(path) - 1):
        from_id = path[i]
        to_id = path[i+1]
        neighbors = dict(graph[from_id])
        if to_id not in neighbors:
            return False  
        edge = neighbors[to_id]
        total_cost += edge['distance'] * (1 + edge['weight'])  
    return total_cost <= drone['battery']

#  2. Ağırlık kontrolü: drone paketi taşıyabilir mi?
def check_weight(drone, delivery):
    return delivery['weight'] <= drone['max_weight']

# 3. Zaman aralığı kontrolü: teslimat istenen saat aralığında mı?
def check_time_window(delivery, arrival_time_str):
    fmt = "%H:%M"
    arrival = datetime.strptime(arrival_time_str, fmt)

    start_raw, end_raw = delivery['time_window']

    # Eğer zamanlar string ise doğrudan parse et
    if isinstance(start_raw, str) and isinstance(end_raw, str):
        start = datetime.strptime(start_raw, fmt)
        end = datetime.strptime(end_raw, fmt)
    elif isinstance(start_raw, int) and isinstance(end_raw, int):
        start = datetime.combine(arrival.date(), datetime.min.time()) + timedelta(minutes=start_raw)
        end = datetime.combine(arrival.date(), datetime.min.time()) + timedelta(minutes=end_raw)
    else:
        raise ValueError("time_window formatı geçersiz")

    return start <= arrival <= end


# 4. No-Fly Zone kontrolü: rota aktif bir yasak alandan geçiyor mu?
def check_nofly_zones(path_coords, noflyzones, arrival_time_str):
    fmt = "%H:%M"
    arrival = datetime.strptime(arrival_time_str, fmt)

    for zone in noflyzones:
        z_start_raw, z_end_raw = zone['active_time']

        # Eğer zamanlar string ise doğrudan parse et
        if isinstance(z_start_raw, str) and isinstance(z_end_raw, str):
            z_start = datetime.strptime(z_start_raw, fmt)
            z_end = datetime.strptime(z_end_raw, fmt)

        elif isinstance(z_start_raw, int) and isinstance(z_end_raw, int):
            z_start = datetime.combine(arrival.date(), datetime.min.time()) + timedelta(minutes=z_start_raw)
            z_end = datetime.combine(arrival.date(), datetime.min.time()) + timedelta(minutes=z_end_raw)
        else:
            raise ValueError("active_time formatı geçersiz")

        if z_start <= arrival <= z_end:
            if intersects_zone(path_coords, zone['coordinates']):
                return False  # yasak bölgeye giriyor
    return True

# Basit poligon içi kontrol fonksiyonu (yaklaşık)
def intersects_zone(path_coords, polygon_coords):
    for point in path_coords:
        if point_inside_polygon(point, polygon_coords):
            return True
    return False

# Nokta poligon içinde mi? (Ray casting algoritması)
def point_inside_polygon(point, polygon):
    x, y = point
    inside = False
    n = len(polygon)
    px1, py1 = polygon[0]
    for i in range(1, n + 1):
        px2, py2 = polygon[i % n]
        if y > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y - py1) * (px2 - px1) / (py2 - py1 + 1e-10) + px1
                        if px1 == px2 or x <= xinters:
                            inside = not inside
        px1, py1 = px2, py2
    return inside


# if __name__ == "__main__":

    # drone = {'id': 0, 'max_weight': 5.0, 'battery': 300}
    # delivery = {'id': 1, 'pos': (10, 20), 'weight': 3.0, 'priority': 2, 'time_window': ['12:00', '14:00']}
    # graph = {
    # 0: {
    #     1: {'distance': 150, 'weight': 0.2}
    # },
    # }
 
    # path = [0, 1]
    # noflyzones = [
    # {
    #     'id': 0,
    #     'coordinates': [(50, 50), (60, 50), (60, 60), (50, 60)],
    #     'active_time': ['12:00', '14:00']
    # }
    # ]
    # path_coords = [(0, 0), (10, 20)]
    # arrival_time = "13:00"


    # Rota koordinatları
    # path_coords = [ (0, 0), (10, 20) ]  

    # valid_battery = check_battery(drone, path, graph)
    # valid_weight = check_weight(drone, delivery)
    # valid_time = check_time_window(delivery, arrival_time)
    # valid_flight = check_nofly_zones(path_coords, noflyzones, arrival_time)

    # if valid_battery and valid_weight and valid_time and valid_flight:
    #     print("✅ Rota geçerli.")
    # else:
    #     print("❌ Rota reddedildi.")
    #     if not valid_battery:
    #         print("❌ Batarya yetersiz.")
    #     if not valid_weight:
    #         print("❌ Taşınan yük drone kapasitesini aşıyor.")
    #     if not valid_time:
    #         print("❌ Teslimat zaman aralığı dışında.")
    #     if not valid_flight:
    #         print("❌ Rota no-fly zone içinden geçiyor.")
