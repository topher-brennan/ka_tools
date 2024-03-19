#   'Material':                (DR,Cost, Weight)
MATERIALS = {
    'NO':                       (0, 0,    0),
    'CANE':                     (1, 35,   12),
    'CLOTH_PADDED':             (1, 50,   6),
    'STRAW':                    (2, 50,   20),
    'LAYERED_LEATHER_LIGHT':    (2, 120,  15),
    'LAYERED_CLOTH_LIGHT':      (2, 150,  12),
    'WOOD':                     (3, 100,  30),
    'LAYERED_LEATHER_MEDIUM':   (3, 220,  26),
    'HORN':                     (3, 250,  25),
    'LAYERED_CLOTH_MEDIUM':     (3, 350,  20),
    'LAYERED_LEATHER_LIGHT_F':  (3, 600,  15),
    'PLATE_LIGHT':              (3, 4000, 8),
    'LAYERED_LEATHER_HEAVY':    (4, 525,  35),
    'LAYERED_CLOTH_HEAVY':      (4, 600,  28),
    'LAYERED_LEATHER_MEDIUM_F': (4, 1100, 26),
    'SEGMENTED_PLATE_MEDIUM':   (4, 3600, 24),
    'PLATE_LIGHT_P':            (4, 6000, 12),
    'LAYERED_LEATHER_HEAVY_F':  (5, 2625, 35),
    'SEGMENTED_PLATE_HEAVY':    (5, 4800, 32),
    'PLATE_LIGHT_PP':           (5, 8000, 16)
} 

FLEXIBLE_MATERIALS = [
    'NO',
    'CLOTH_PADDED',
    'LAYERED_CLOTH_LIGHT',
    'LAYERED_LEATHER_LIGHT',
    'LAYERED_LEATHER_LIGHT_F'
]

# Location: (Cost multiplier, Hit probability)
LOCATIONS = {
    'HEAD':       (0.20, 4.0 / 216),
    'NOSE':       (0.01, 6.0 / 216 / 6),
    'CHEEKS':     (0.02, 6.0 / 216 / 3),
    # 'NECK':     (0.05, 4.0 / 216),
    'CHEST':      (0.75, 52.0 / 216),
    'ABDOMEN':    (0.25, 27.0 / 216),
    'SHOULDERS':  (0.10, 46.0 / 216 / 6),
    'UPPER_ARMS': (0.10, 46.0 / 216 / 6),
    'ELBOWS':     (0.05, 46.0 / 216 / 6),
    'FOREARMS':   (0.25, 46.0 / 216 / 2),
    # 'ELBOWS_FOREARMS': (0.30, 46.0 / 216 * 2 / 3),
    'HANDS':      (0.10, 10.0 / 216),
    'THIGHS':     (0.45, 61.0 / 216 / 3),
    'KNEES':      (0.05, 61.0 / 216 / 6),
    'SHINS':      (0.50, 61.0 / 216 / 2),
    # 'KNEES_SHINS': (0.55, 61.0 * 2 / 3),
    'FEET':       (0.10, 6.0 / 216),
}

options = []

for dr in BY_DR.keys():
    for location in BY_LOCATION.keys():
        options.append((dr, location))

def efficiency(option):
    by_location = BY_LOCATION[option[1]]
    return BY_DR[option[0]] * by_location[0] / by_location[1]

sorted_options = sorted(options, key=efficiency)

def for_cost(max_cost):
    total_cost = 0
    result = {}

    for option in sorted_options:
        option_cost = BY_DR[option[0]] * BY_LOCATION[option[1]][0]
        if total_cost + option_cost <= max_cost:
            total_cost += option_cost
            result[option[1]] = option[0]

    for key, val in result.items():
        print(f'{key}: {val}')

    print(f'TOTAL COST: ${total_cost}')
    print('')

for_cost(200)
for_cost(300)
for_cost(400)
for_cost(500)
for_cost(600)
for_cost(700)
for_cost(800)
for_cost(900)
for_cost(1000)
