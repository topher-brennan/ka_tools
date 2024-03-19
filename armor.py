from math import floor

#   'Material':                (DR,Cost, Weight)
BY_MATERIAL = {
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

ALL_MATERIALS = list(BY_MATERIAL.keys())

FLEXIBLE_MATERIALS = [
    'NO',
    'CLOTH_PADDED',
    'LAYERED_CLOTH_LIGHT',
    'LAYERED_LEATHER_LIGHT',
    'LAYERED_LEATHER_LIGHT_F'
]

# Location: (Cost multiplier, Hit probability)
BY_LOCATION = {
    'HEAD':       (0.23, 10.0 / 216),
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

LOCATIONS = list(BY_LOCATION.keys())

CACHE = {}

# `exclude` means exclude all locations whose index is < `exclude`
def for_cost_and_weight(cost, weight, exclude=0):
    if exclude >= len(LOCATIONS):
        return (0, [])

    cost = floor(cost)
    weight = floor(weight * 10) / 10.0

    if not cost in CACHE:
        CACHE[cost] = {}
    if not weight in CACHE[cost]:
        CACHE[cost][weight] = {}
    if exclude in CACHE[cost][weight]:
        return CACHE[cost][weight][exclude]

    location = LOCATIONS[exclude]

    if location in ['HANDS', 'THIGHS', 'FEET']:
        material_options = FLEXIBLE_MATERIALS
    else:
        material_options = ALL_MATERIALS

    best = None

    for material in material_options:
        this_value = item_value(material, location)
        this_cost = item_cost(material, location)
        this_weight = item_weight(material, location)

        if this_cost <= cost and this_weight <= weight:
            recursive = for_cost_and_weight(
                    cost - this_cost,
                    weight - this_weight,
                    exclude + 1,
            )

            new_value = this_value + recursive[0]
            new_items = [material] + recursive[1]

            if best is None or new_value > best[0]:
                best = (new_value, new_items)

    CACHE[cost][weight][exclude] = best

    return best

def item_value(material, location):
    result = BY_MATERIAL[material][0] * BY_LOCATION[location][1]
    if location == 'HEAD':
        result *= 1.4
    elif location in ['CHEST', 'ABDOMEN']:
        result *= 6.5 / 6
    return round(result * 10) / 10.0

def item_cost(material, location):
    result = BY_MATERIAL[material][1] * BY_LOCATION[location][0]
    if location == 'HEAD':
        result += 10 * 1.15
    return round(result)

def item_weight(material, location):
    result = BY_MATERIAL[material][2] * BY_LOCATION[location][0]
    if location == 'HEAD':
        result += 1.2 * 1.15
    return round(result)

print(LOCATIONS)
print(for_cost_and_weight(837, 68.8))
print(for_cost_and_weight(640, 72.8))
print(for_cost_and_weight(680, 88.8))
print(for_cost_and_weight(417, 68.8))
for i in range(21):
    print(for_cost_and_weight(1000 + 500 * i, 83.8))
