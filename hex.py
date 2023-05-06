from math import ceil, floor, sqrt
from sys import stdout
import argparse

AVERAGE_HEX_WIDTH = sqrt(3)/2
DEFAULT_WINDOW_WIDTH = 80
DEFAULT_WINDOW_HEIGHT = 24

def distance(x, y):
  y_adjust = (0.5 if x % 2 == 1 else 0)
  return ceil(sqrt((y + y_adjust)**2 + (x * AVERAGE_HEX_WIDTH)**2))

parser = argparse.ArgumentParser()
parser.add_argument('--width', type=int, default=DEFAULT_WINDOW_WIDTH)
parser.add_argument('--height', type=int, default=DEFAULT_WINDOW_HEIGHT)
args = parser.parse_args()

for i in range(args.height):
    for j in range(args.width):
        magic_number = j 
        if i % 2 == 1:
            magic_number += 2 
        magic_number %= 5

        if magic_number == 0:
            stdout.write('/')
        elif magic_number == 1:
            x = floor(j / 2.5)
            y = i // 2
            if y <= x/2:
                stdout.write(str(x - distance(x, y)).rjust(2))
            else:
                stdout.write('  ')
        elif magic_number == 2:
            stdout.write('\\')
        elif magic_number > 2:
            stdout.write('_') 
    stdout.write('\n')

