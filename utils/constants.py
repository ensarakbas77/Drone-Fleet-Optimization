# utils/constants.py

# 🔧 Genetik Algoritma Ayarları
MAX_DELIVERIES_PER_DRONE = 3
MUTATION_RATE = 0.3
GENERATION_COUNT = 10
POPULATION_SIZE = 8

# ⚠ Ceza Katsayıları
PENALTY_NO_ROUTE = -50
PENALTY_NOFLY_ZONE = 9999

# ⚡ Enerji & Şarj
CHARGE_TIME_HOURS = 1.0

# 📦 Teslimat Öncelik Ceza Katsayısı
PRIORITY_PENALTY_MULTIPLIER = 100
MAX_PRIORITY_VALUE = 5  # (6 - priority) yapısında bu değer 5 olmalı

# Fitness hesaplama katsayıları
FITNESS_DELIVERY_REWARD = 50
FITNESS_ENERGY_PENALTY = 0.1
FITNESS_VIOLATION_PENALTY = 1000
