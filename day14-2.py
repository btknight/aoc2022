"""
--- Part Two ---
You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're
standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to
two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan
contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like
this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->
To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0,
blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally
looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to
rest?
"""
from common import read_file
from typing import Tuple, List, Optional
from itertools import count

x_margin = 160

# Get list of points. Parse the coordinates into lists of tuples.
line_l = []
for line in read_file('input/14.txt'):
    line_l.append([eval(f'({i})') for i in line.split(' -> ')])

# Find the upper-left and lower-right corner of the coords.
print(line_l)
all_pts = [p for i in line_l for p in i]
smallest_x = [i[0] for i in sorted(all_pts, key=lambda i: i[0])][0] - x_margin
largest_x = [i[0] for i in sorted(all_pts, key=lambda i: -i[0])][0] + x_margin
largest_y = [i[1] for i in sorted(all_pts, key=lambda i: -i[1])][0] + 2
upper_left = (smallest_x, 0)
lower_right = (largest_x, largest_y)
print(f'upper left = {upper_left}')
print(f'lower right = {lower_right}')


def coord_transform(coord: Tuple[int, int]):
    """Transforms the coordinates where the upper_left is considered (0, 0)."""
    return (coord[0] - upper_left[0], coord[1] - upper_left[1])


def print_map():
    """Prints the map."""
    for line in map:
        print(''.join(line))


def draw_line(start, end):
    """Generates a list of points between start and end."""
    if start[0] == end[0] and start[1] < end[1]:
        for y in range(start[1], end[1] + 1):
            yield (start[0], y)
    elif start[0] == end[0] and start[1] > end[1]:
        for y in range(start[1], end[1] - 1, -1):
            yield (start[0], y)
    elif start[1] == end[1] and start[0] < end[0]:
        for x in range(start[0], end[0] + 1):
            yield (x, start[1])
    elif start[1] == end[1] and start[0] > end[0]:
        for x in range(start[0], end[0] - 1, -1):
            yield (x, start[1])


class OutOfBounds(BaseException):
    """Thrown when sand falls off the bottom of the map."""
    pass


# Initialize the map.
t_end = coord_transform(lower_right)
map = [['.' for x in range(t_end[0] + 1)] for y in range(t_end[1] + 1)]
map[-1] = ['#' for x in range(t_end[0] + 1)]
print_map()
print()


# Draw lines on the map
for line in line_l:
    line = line.copy()
    cursor = start = coord_transform(line.pop(0))
    while len(line) > 0:
        end = coord_transform(line.pop(0))
        for x, y in draw_line(start, end):
            map[y][x] = '#'
        start = end


# Start running sand into the map
sand_source = coord_transform((500, 0))


def pour_1_sand(map: List[List[str]], source: Tuple[int, int] = sand_source):
    """Pours 1 unit of sand into the top of the map."""
    def is_free(point):
        """Returns whether a candidate point is open for sand to fall in."""
        return map[point[1]][point[0]] == '.'
    def next_move(point) -> Optional[Tuple[int, int]]:
        """Determines next point for the sand to fall. Returns None if there is nowhere for the sand to go.
        If the sand falls below the bottom limit of the map, throws an OutOfBounds exception to signal that the
        sand is done falling."""
        c_x, c_y = point
        if c_y + 1 == len(map):
            # Sand fell off the map! We are done
            raise OutOfBounds()
        # Sand prefers to fall directly below first, below and to left second, and below and to right third.
        candidate_l = [(c_x, c_y + 1), (c_x - 1, c_y + 1), (c_x + 1, c_y + 1)]
        for candidate in candidate_l:
            if is_free(candidate):
                return candidate
        # If these 3 spots are not free, the sand comes to a rest.
        return None
    if not is_free(source):
        raise OutOfBounds
    cursor = source
    while next_move(cursor) is not None:
        cursor = next_move(cursor)
    map[cursor[1]][cursor[0]] = 'o'


# Initialize a counter for the number of sand blocks.
ctr = count(0)
while True:
    try:
        pour_1_sand(map)
        next(ctr)
    except OutOfBounds:
        break

num_sands = next(ctr)
print_map()
print(f'num_sands = {num_sands}')
