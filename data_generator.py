import random
from typing import List, Tuple
from datetime import datetime, timedelta

class Drone:
    def __init__(self, id: int, max_weight: float, battery: int, speed: float, start_pos: Tuple[float, float]):
        self.id = id
        self.max_weight = max_weight
        self.battery = battery
        self.speed = speed
        self.start_pos = start_pos

class DeliveryPoint:
    def __init__(self, id: int, pos: Tuple[float, float], weight: float, priority: int, time_window: Tuple[str, str]):
        self.id = id
        self.pos = pos
        self.weight = weight
        self.priority = priority
        self.time_window = time_window

class NoFlyZone:
    def __init__(self, id: int, coordinates: List[Tuple[float, float]], active_time: Tuple[str, str]):
        self.id = id
        self.coordinates = coordinates
        self.active_time = active_time


def generate_random_drones(n: int) -> List[Drone]:
    drones = []
    for i in range(n):
        drone = Drone(
            id=i,
            max_weight=round(random.uniform(2.0, 10.0), 2),
            battery=random.randint(3000, 10000),
            speed=round(random.uniform(5.0, 20.0), 2),
            start_pos=(random.uniform(0, 100), random.uniform(0, 100))
        )
        drones.append(drone)
    return drones

def generate_random_deliveries(n: int) -> List[DeliveryPoint]:
    deliveries = []
    for i in range(n):
        start_hour = random.randint(9, 16)
        end_hour = start_hour + random.randint(1, 2)
        delivery = DeliveryPoint(
            id=i,
            pos=(random.uniform(0, 100), random.uniform(0, 100)),
            weight=round(random.uniform(0.5, 5.0), 2),
            priority=random.randint(1, 5),
            time_window=(f"{start_hour:02d}:00", f"{end_hour:02d}:00")
        )
        deliveries.append(delivery)
    return deliveries

def generate_random_nofly_zones(n: int) -> List[NoFlyZone]:
    zones = []
    for i in range(n):
        coordinates = [(random.uniform(20, 80), random.uniform(20, 80)) for _ in range(4)]  # 4 köşeli alan
        start_hour = random.randint(9, 16)
        end_hour = start_hour + random.randint(1, 2)
        zone = NoFlyZone(
            id=i,
            coordinates=coordinates,
            active_time=(f"{start_hour:02d}:00", f"{end_hour:02d}:00")
        )
        zones.append(zone)
    return zones
