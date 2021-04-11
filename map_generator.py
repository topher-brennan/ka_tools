from random import random
from math import atan, degrees, e, log, pi, sqrt, tan
from numpy import cross

# Starting with a system for generating the Southlands

MAP_SIZE = 2**8 + 1
TAN_10_DEG = tan(pi / 18)
TAN_30_DEG = tan(pi / 6)
TAN_MINUS_12_DEG = tan(-1 * pi / 15)
ROUGHNESS = 1
BASE_HEIGHT = e ** (1/3)
DIRECTIONS = [
    [-1, -1],
    [-1, 0],
    [-1, 1],
    [0, -1],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1],
]
DIAGONALS = [
    [-1, -1],
    [-1, 1],
    [1, -1],
    [1, 1],
]

def bishop_step(map, y, x, step):
    map[y][x] = (map[y-step][x-step] + map[y+step][x-step] + map[y-step][x+step] + map[y+step][x+step]) / 4 + ROUGHNESS * TAN_10_DEG * BASE_HEIGHT ** log(step) * (random() * 2 - 1)

def rook_step(map, y, x, step):
    if map[y][x] is None:
        map[y][x] = average_adjacent(map, y, x, step) + ROUGHNESS * TAN_10_DEG * BASE_HEIGHT ** log(step) * (random() * 2 - 1)

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
    # total_slope = sqrt(y_incline(map, y, x)**2 + x_incline(map, y, x)**2)
    # if total_slope < TAN_10_DEG:
    #     return 1
    # elif total_slope < TAN_30_DEG:
    #     return 2
    # else:
    #     return 3
    nf = naismith_factor(map, y, x)
    if nf < 1.5:
        return 1
    elif nf < 3.5:
        return 2
    else:
        return 3

def naismith_factor(map, y, x):
    factors = []
    for dir in DIRECTIONS:
        if y + dir[0] > 0 and y + dir[0] < MAP_SIZE and x + dir[1] > 0 and x + dir[1] < MAP_SIZE:
            rise = map[y][x] - map[y+dir[0]][x+dir[1]]
            run = sqrt(dir[0]**2 + dir[1]**2)
            rise_over_run = rise / run
            if rise_over_run >= 0:
                factors.append(1 + rise_over_run * 5280 / 2000 * 3)
            elif rise_over_run >= TAN_MINUS_12_DEG:
                factors.append(1 - rise_over_run * 5280 / 2000)
            else:
                factors.append(1 + rise_over_run * 5280 / 2000)
    return max(factors)

def code_map(map):
    # arable_map = [[(2 if map[y][x] <= 0 else (1 if arable(map, y, x) else 0)) for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
    arable_map = [[slope_code(map, y, x) for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
    for y in range(MAP_SIZE):
        inland_distance = 0
        for x in reversed(range(MAP_SIZE)):
           if arable_map[y][x] == 0 and inland_distance > 0:
               inland_distance -= 1
           else:
                inland_distance += 1
           if inland_distance <= (100 + y / 4) and arable_map[y][x] == 1:
    	        arable_map[y][x] = '='
    return arable_map

def code_map2(map):
    arable_map = [[slope_code(map, y, x) for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
    for y in range(MAP_SIZE):
        inland_distance = 0
        for x in reversed(range(MAP_SIZE)):
           if arable_map[y][x] == 0:
               arable_map[y][x] = 'w'
               if inland_distance > 0:
                   inland_distance -= 1
           else:
                inland_distance += 1
                aq = arable_quadrants(map, y, x)
                if inland_distance <= (100 + y / 4) and aq > 0:
    	            arable_map[y][x] = aq
                elif arable_map[y][x] == 1:
                    arable_map[y][x] = 'P'
                elif arable_map[y][x] == 2:
                    arable_map[y][x] = 'H'
                else:
                    arable_map[y][x] = 'M'
    return arable_map

# Is there a better name for this?
def vector_slope(vector):
    horizontal = sqrt(vector[0]**2 + vector[1]**2)
    if horizontal == 0:
        return 90
    radians = atan(vector[2] / horizontal)
    return degrees(radians)

def quadrant_is_arable(map, y, x, dir):
    if y + dir[0] < 0 or y + dir[0] >= MAP_SIZE or x + dir[1] < 0 or x + dir[1] >= MAP_SIZE:
        return False
    leg1 = [dir[0], 0, map[y+dir[0]][x] - map[y][x]]
    leg2 = [0, dir[1], map[y][x+dir[1]] - map[y][x]]
    return vector_slope(cross(leg1, leg2)) > 80

def arable_quadrants(map, y, x):
    return len([dir for dir in DIAGONALS if quadrant_is_arable(map, y, x, dir)])

def print_arable_map(map, arable_map, total_arable, total_land):
    for row in arable_map:
        print(''.join([str(el) for el in row]))
    high_point = max([max([el for el in row]) for row in map])
    print(f'Northwest elevation: {map[0][0]}')
    print(f'High point: {high_point}')
    print(f'Total arable: {total_arable}')
    print(f'Pop: {total_arable*50}')
    print(f'% arable: {total_arable / total_land / 4}')

def open_csv(filename):
    return [[float(point) for point in row.split(',')] for row in open(filename).read().split('\n')]

if __name__ == "__main__":
    done = False
    while not done:
        map = [[None for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        step = int((MAP_SIZE - 1)/2)
    
        map[0][0] = 0.01 + 0.01 * random()
        map[0][-1] = 0
        map[-1][0] = ROUGHNESS * TAN_10_DEG * BASE_HEIGHT ** log(step) * random() * 2
        # map[-1][-1] = ROUGHNESS * TAN_10_DEG * step * random() * -2
        map[-1][-1] = 0
        
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
        if left_min > 0:
            left_min = 0
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                map[y][x] -= right_max * x / MAP_SIZE
                map[y][x] -= left_min * y * (MAP_SIZE - x) / MAP_SIZE ** 2
        	
        arable_map = code_map2(map)
        
        total_arable = 0
        total_land = 0
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                if arable_map[y][x] != 'w':
                    total_land += 1
                    if type(arable_map[y][x]) == int:
                        total_arable += arable_map[y][x]
        
        # if all([el != 'w' for el in arable_map[0][0:100]]):
        if True:
            done = True

    # f = open('southlands.csv', 'w')
    # f.write('\n'.join([','.join([str(point) for point in row]) for row in map])) 
    
    print_arable_map(map, arable_map, total_arable, total_land)
