"""
--- Day 15: Beacon Exclusion Zone ---
You feel the ground rumble again as the distress signal leads you to a large network of subterranean tunnels. You don't
have time to search them all, but you don't need to: your pack contains a set of deployable sensors that you imagine
were originally built to locate lost Elves.

The sensors aren't very powerful, but that's okay; your handheld device indicates that you're close enough to the
source of the distress signal to use them. You pull the emergency sensor system out of your pack, hit the big button on
top, and the sensors zoom off down the tunnels.

Once a sensor finds a spot it thinks will give it a good reading, it attaches itself to a hard surface and begins
monitoring for the nearest signal source beacon. Sensors and beacons always exist at integer coordinates. Each sensor
knows its own position and can determine the position of a beacon precisely; however, sensors can only lock on to the
one beacon closest to the sensor as measured by the Manhattan distance. (There is never a tie where two beacons are the
same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and closest beacons (your puzzle input). For
example:

Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For the sensor at 9,16, the closest beacon to it
is at 10,16.

Drawing sensors as S and beacons as B, the above arrangement of sensors and beacons looks like this:

               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
This isn't necessarily a comprehensive map of all beacons in the area, though. Because each sensor only identifies its
closest beacon, if a sensor detects a beacon, you know there are no other beacons that close or closer to that sensor.
There could still be beacons that just happen to not be the closest beacon to any sensor. Consider the sensor at 8,7:

               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########............
12 ......#########.............
13 .......#######..............
14 ........#####.S.......S.....
15 B........###................
16 ..........#SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
This sensor's closest beacon is at 2,10, and so you know there are no beacons that close or closer (in any positions
marked #).

None of the detected beacons seem to be producing the distress signal, so you'll need to work out where the distress
beacon is by working out where it isn't. For now, keep things simple by counting the positions where a beacon cannot
possibly be along just a single row.

So, suppose you have an arrangement of beacons and sensors like in the example above and, just in the row where y=10,
you'd like to count the number of positions a beacon cannot possibly exist. The coverage from all sensors near that row
looks like this:

                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.
In this example, in the row where y=10, there are 26 positions where a beacon cannot be present.

Consult the report from the sensors you just deployed. In the row where y=2000000, how many positions cannot contain a
beacon?
"""
from common import read_file
import re
from typing import Tuple, Optional, List


Y_LINE = 2000000


def taxicab_distance(sensor: Tuple[int, int], beacon: Tuple[int, int]):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def find_y_coverage(sensor: Tuple[int, int], beacon: Tuple[int, int], y: int) -> Optional[Tuple[int, int]]:
    s_x, s_y = sensor
    taxicab_dist = taxicab_distance(sensor, beacon)
    is_on_y = (s_y - taxicab_dist) <= y <= (s_y + taxicab_dist)
    if not is_on_y:
        return None
    taxicab_dist -= abs(y - s_y)
    return s_x - taxicab_dist, s_x + taxicab_dist


def find_max_x(sensor: Tuple[int, int], beacon: Tuple[int, int]) -> Tuple[int, int]:
    taxicab_dist = taxicab_distance(sensor, beacon)
    return s_x - taxicab_dist, s_x + taxicab_dist


def coalesce_values(coords):
    if len(coords) < 2:
        return coords
    # Sort the list
    coords = sorted(coords.copy())
    result = []
    # Start with first item in the list
    cursor = coords[0]
    # For each subsequent item,
    for i in range(1, len(coords)):
        # If the end of the cursor overlaps with the next element,
        if coords[i][0] <= cursor[1]:
            # Update the cursor to include that next element
            # Use the maximum of either the cursor or the next element's end point
            cursor = (cursor[0], max(coords[i][1], cursor[1]))
        else:
            # Otherwise, no more overlaps are expected. Store the cursor value,
            # then update the cursor to the new element
            result.append(cursor)
            cursor = coords[i]
    # When there are no more elements to consider, add the cursor to result
    result.append(cursor)
    return result


sensor_coverage = []
beacons_on_y_line = set()
for line in read_file('input/15.txt'):
    data_m = re.match(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)', line)
    if data_m:
        s_x, s_y, b_x, b_y = [int(i) for i in data_m.groups()]
        if b_y == Y_LINE:
            beacons_on_y_line.add(b_x)
        y_cov = find_y_coverage((s_x, s_y), (b_x, b_y), Y_LINE)
        if y_cov is not None:
            sensor_coverage.append(y_cov)


def no_beacon_area(coord):
    global beacons_on_y_line
    start = coord[0]
    end = coord[1] + 1
    return end - start - len({i for i in beacons_on_y_line if start <= i < end})


print(sorted(sensor_coverage))
print(sorted(beacons_on_y_line))
sensor_coverage = coalesce_values(sensor_coverage)
print(sorted(sensor_coverage))
pos_no_beacon = sum([no_beacon_area(i) for i in sensor_coverage])
print(f'No-beacon: {pos_no_beacon}')
