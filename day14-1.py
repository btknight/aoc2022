"""
--- Day 14: Regolith Reservoir ---
The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the
waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the
signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the
cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-
dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures
made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path,
where x represents distance to the right and y represents distance down. Each path appears as a single line of text in
your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to
be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path
consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and
another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to
rest. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the
unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of
sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do
so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked,
the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless
void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........
Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the
abyss below?
"""
from common import read_file
from typing import Tuple, List, Optional
from itertools import count


# Get list of points. Parse the coordinates into lists of tuples.
line_l = []
for line in read_file('input/14.txt'):
    line_l.append([eval(f'({i})') for i in line.split(' -> ')])

# Find the upper-left and lower-right corner of the coords.
print(line_l)
all_pts = [p for i in line_l for p in i]
smallest_x = [i[0] for i in sorted(all_pts, key=lambda i: i[0])][0] - 1
largest_x = [i[0] for i in sorted(all_pts, key=lambda i: -i[0])][0] + 1
largest_y = [i[1] for i in sorted(all_pts, key=lambda i: -i[1])][0] + 1
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
    def next_move(point) -> Optional[Tuple[int, int]]:
        """Determines next point for the sand to fall. Returns None if there is nowhere for the sand to go.
        If the sand falls below the bottom limit of the map, throws an OutOfBounds exception to signal that the
        sand is done falling."""
        def is_free(point):
            """Returns whether a candidate point is open for sand to fall in."""
            return map[point[1]][point[0]] == '.'
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
