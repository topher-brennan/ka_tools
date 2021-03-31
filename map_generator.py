from random import random
from math import pi, sqrt, tan

# Starting with a system for generating the Southlands

MAP_SIZE = 257
TAN_10_DEG = tan(pi / 18)
TAN_30_DEG = tan(pi / 6)
ROUGHNESS = 1

def bishop_step(map, y, x, step):
    map[y][x] = (map[y-step][x-step] + map[y+step][x-step] + map[y-step][x+step] + map[y+step][x+step]) / 4 + ROUGHNESS * TAN_10_DEG * step * (random() * 2 - 1)

def rook_step(map, y, x, step):
    if map[y][x] is None:
        map[y][x] = average_adjacent(map, y, x, step) + ROUGHNESS * TAN_10_DEG * step * (random() * 2 - 1)

def average_adjacent(map, y, x, step):
    adjacent_heights = []
    if y - step >= 0:
        adjacent_heights.append(map[y-step][x])
    if y + step < MAP_SIZE:
        adjacent_heights.append(map[y+step][x])
    if x - step >= 0:
        adjacent_heights.append(map[y][x-step])
    if x + step < MAP_SIZE:
        adjacent_heights.append(map[y][x+step])
    return sum(adjacent_heights) / len(adjacent_heights)

def arable(map, y, x):
    return map[y][x] > 0 and sqrt(y_incline(map, y, x)**2 + x_incline(map, y, x)**2) < TAN_10_DEG

def y_incline(map, y, x):
    if y == 0:
        return abs(map[y+1][x] - map[y][x])
    elif y == MAP_SIZE - 1:
        return abs(map[y][x] - map[y-1][x])
    else:
        return (abs(map[y+1][x] - map[y][x]) + abs(map[y][x] - map[y-1][x])) / 2
        
def x_incline(map, y, x):
    if x == 0:
        return abs(map[y][x+1] - map[y][x])
    elif x == MAP_SIZE - 1:
        return abs(map[y][x] - map[y][x-1])
    else:
        return (abs(map[y][x+1] - map[y][x]) + abs(map[y][x] - map[y][x-1])) / 2

def slope_code(map, y, x):
    if map[y][x] <=0:
        return 0
    total_slope = sqrt(y_incline(map, y, x)**2 + x_incline(map, y, x)**2)
    if total_slope < TAN_10_DEG:
        return 1
    elif total_slope < TAN_30_DEG:
        return 2
    else:
        return 3

done = False
while not done:
    map = [[None for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    for y in [0, -1]:
        map[y][-1] = 0
        map[y][0] = 0
    step = int((MAP_SIZE - 1)/2)
    
    while step > 0:
        for y in range(step, MAP_SIZE, step * 2):
            for x in range(step, MAP_SIZE, step * 2):
    	        bishop_step(map, y, x, step)
        
        for y in range(0, MAP_SIZE, step):
            for x in range(0, MAP_SIZE, step):
                rook_step(map, y, x, step)
    
        step = int(step/2)
    
    right_max = max(row[-1] for row in map)
    if right_max < 0:
        right_max = 0
    left_min = min(row[0] for row in map)
    if left_min > -0.02:
        left_min = -0.02
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            map[y][x] -= right_max * x / MAP_SIZE
            map[y][x] -= left_min * (MAP_SIZE - x) / MAP_SIZE
    	
    # arable_map = [[(2 if map[y][x] <= 0 else (1 if arable(map, y, x) else 0)) for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
    arable_map = [[slope_code(map, y, x) for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
    for y in range(MAP_SIZE):
        inland_distance = 0
        for x in reversed(range(MAP_SIZE)):
           if arable_map[y][x] == 0 and inland_distance > 0:
               inland_distance -= 1
           else:
                inland_distance += 1
           if inland_distance <= (100 + (MAP_SIZE - 100) / MAP_SIZE * y) and arable_map[y][x] == 1:
    	        arable_map[y][x] = '='

    for row in arable_map:
        print(''.join([str(el) for el in row]))
    
    total_arable = 0
    total_land = 0
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            if arable_map[y][x] != 0:
                total_land += 1
                if arable_map[y][x] == 1:
                    total_arable += 1
    
    if all([el != 0 for el in map[0][:100]]):
        done = True

print(f'Total arable: {total_arable}')
print(f'Pop: {total_arable*275}')
print(f'% arable: {total_arable / total_land}')
