"""
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a
previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location
for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the
number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For
example:

30373
25512
65332
33549
35390
Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees
in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to
block the view. In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height
5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0
between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most
height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this
arrangement.

Consider your map; how many trees are visible from outside the grid?
"""
from typing import List

matrix_by_row = []
with open('input/8.txt') as fh:
    for line in fh.readlines():
        matrix_by_row.append([int(i) for i in line.rstrip()])

# https://stackoverflow.com/questions/6473679/transpose-list-of-lists
matrix_by_col = list(map(list, zip(*matrix_by_row)))

r_edge = len(matrix_by_row[0]) - 1
b_edge = len(matrix_by_row) - 1


def is_visible(x: int, y: int) -> bool:
    # If tree is on the edge, it is visible
    if x == 0 or x == r_edge or y == 0 or y == b_edge:
        return True
    #
    h = matrix_by_row[y][x]
    def are_trees_higher(side: List[int], h: int):
        return len([i for i in side if i >= h]) > 0

    blk_left = are_trees_higher(matrix_by_row[y][:x], h)
    blk_right = are_trees_higher(matrix_by_row[y][x + 1:], h)
    blk_top = are_trees_higher(matrix_by_col[x][:y], h)
    blk_bot = are_trees_higher(matrix_by_col[x][y + 1:], h)
    if blk_left and blk_right and blk_top and blk_bot:
        return False
    return True


accum = 0
for x in range(0, len(matrix_by_row[0])):
    for y in range(0, len(matrix_by_row)):
        if is_visible(x, y):
            accum += 1

print(f'Trees visible: {accum}')
