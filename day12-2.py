"""
--- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very
scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square
marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find
the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at
elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the
best signal?
"""
from common import read_file
from itertools import count

map = []
start = (0, 0)
end = (0, 0)
ctr = count(0)
for line in read_file('input/12.txt'):
    row = next(ctr)
    row_char = [i for i in line]
    for col in range(0, len(row_char)):
        if row_char[col] == 'S':
            start = (col, row)
            row_char[col] = 'a'
        if row_char[col] == 'E':
            end = (col, row)
            row_char[col] = 'z'
    map.append([ord(i) - ord('a') for i in row_char])


def is_adjacent(u, v):
    """Returns True if a node u in the map is adjacent to node v."""
    x_u, y_u = u
    x_v, y_v = v
    def is_nei(dir_u, dir_v):
        return dir_u + 1 == dir_v or dir_u - 1 == dir_v
    # CSPF
    if map[y_v][x_v] - map[y_u][x_u] > 1:
        return False
    # Can go left or right
    if is_nei(x_u, x_v) and y_u == y_v:
        return True
    # Or up and down
    if is_nei(y_u, y_v) and x_u == x_v:
        return True
    return False


def spf(map, start, end):
    """Wikipedia implementation of SPF.
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
    """
    dist = []
    prev = []
    Q = set()

    for y in range(0, len(map)):
        row = map[y]
        dist.append([float('inf') for i in row])
        prev.append([None for i in row])
        for x in range(0, len(row)):
            Q.add((x, y))
    dist[start[1]][start[0]] = 0

    while len(Q) > 0:
        u = [node for node in sorted(Q, key=lambda n: dist[n[1]][n[0]])][0]
        if u == end:
            return dist, prev
        Q.remove(u)

        for v in [v for v in Q if is_adjacent(u, v)]:
            alt = dist[u[1]][u[0]] + 1
            if alt < dist[v[1]][v[0]]:
                dist[v[1]][v[0]] = alt
                prev[v[1]][v[0]] = u

    return dist, prev


starts = set()
for y in range(0, len(map)):
    for x in range(0, len(map[y])):
        if map[y][x] == 0:
            starts.add((x, y))

min_start = None
min_dist = float('inf')
ctr = count(1)
for start in starts:
    print(f'{next(ctr)} / {len(starts)} Starting spf from {start}')
    dist, prev = spf(map, start, end)
    dist_to_end = dist[end[1]][end[0]]
    if dist_to_end < min_dist:
        print(f'  New shortest dist: {start} -> {dist_to_end}')
        min_dist = dist_to_end
        min_start = start

print(start, end)
print(map)
print(dist)
print(prev)
print(f'Minimum path from {min_start} to {end}: {min_dist}')
