"""
--- Part Two ---
Your handheld device indicates that the distress signal is coming from a beacon nearby. The distress beacon is not
detected by any sensor, but the distress beacon must have x and y coordinates each no lower than 0 and no larger than
4000000.

To isolate the distress beacon's signal, you need to determine its tuning frequency, which can be found by multiplying
its x coordinate by 4000000 and then adding its y coordinate.

In the example above, the search space is smaller: instead, the x and y coordinates can each be at most 20. With this
reduced search area, there is only a single position that could have a beacon: x=14, y=11. The tuning frequency for
this distress beacon is 56000011.

Find the only possible position for the distress beacon. What is its tuning frequency?
"""
from common import read_file
import re
from typing import Tuple, Optional, List


Y_LINE = 10


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


sensors_and_beacons = []
for line in read_file('input/15.txt'):
    data_m = re.match(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)', line)
    if data_m:
        s_x, s_y, b_x, b_y = [int(i) for i in data_m.groups()]
        sb = ((s_x, s_y), (b_x, b_y))
        sensors_and_beacons.append(sb)


def find_uncovered_point():
    global sensors_and_beacons
    for y in range(0, 4000001):
        if y % 100000 == 0:
            print(f'y = {y}')
        sensor_coverage = []
        for sb in sensors_and_beacons:
            s_x, s_y = sb[0]
            b_x, b_y = sb[1]
            y_cov = find_y_coverage((s_x, s_y), (b_x, b_y), y)
            if y_cov is not None:
                sensor_coverage.append(y_cov)
        sensor_coverage = coalesce_values(sensor_coverage)
        for coords in sensor_coverage:
            if 0 <= coords[1] <= 4000000:
                uncovered_point = coords[1] + 1, y
                print(f'Found uncovered point: {uncovered_point}')
                return ((coords[1] + 1) * 4000000) + y
    return None


print(f'Beacon freq: {find_uncovered_point()}')
