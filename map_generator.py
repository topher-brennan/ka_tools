from random import random
from math import pi, sqrt, tan

# Starting with a system for generating the Southlands

MAP_SIZE = 257
TAN_10_DEG = tan(pi / 18)
ROUGHNESS = 1.5
RIGHT_CORNERS = 0.0

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
        return abs(map[y+1][x] - map[y-1][x]) / 2
        
def x_incline(map, y, x):
    if x == 0:
        return abs(map[y][x+1] - map[y][x])
    elif x == MAP_SIZE - 1:
        return abs(map[y][x] - map[y][x-1])
    else:
        return abs(map[y][x+1] - map[y][x-1]) / 2

map = [[None for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
for y in [0, -1]:
    map[y][-1] = RIGHT_CORNERS
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

left_max = max(row[0] for row in map)
if left_max < 0:
    left_max = 0
right_min = min(row[-1] for row in map)
if right_min > -0.02:
    right_min = -0.02
for y in range(MAP_SIZE):
    for x in range(MAP_SIZE):
        map[y][x] -= left_max * (MAP_SIZE - x) / MAP_SIZE
        map[y][x] -= right_min * x / MAP_SIZE
        
arable_map = [[(2 if map[y][x] <= 0 else (1 if arable(map, y, x) else 0)) for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
for row in arable_map:
    print(''.join([str(el) for el in row]))

total_arable = 0
total_land = 0
for y in range(MAP_SIZE):
    for x in range(MAP_SIZE):
        if arable_map[y][x] < 2:
            total_land += 1
            if arable_map[y][x] == 1:
                total_arable += 1

print(f'Total arable: {total_arable}')
print(f'Pop: {total_arable*275}')
print(f'% arable: {total_arable / total_land}')
