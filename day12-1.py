"""
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent
signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from
above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the
lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal
(E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move
exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the
destination square can be at most one higher than the elevation of your current square; that is, if your current
elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the
destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but
eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or
right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
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

dist, prev = spf(map, start, end)

print(f'Minimum path from {start} to {end}: {dist[end[1]][end[0]]}')
