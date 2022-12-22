"""
--- Part Two ---
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house:
they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an
edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on
the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large
eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390
Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks
its view).
A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this
tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390
Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?
"""
from functools import reduce
from typing import List

matrix_by_row = []
with open('input/8.txt') as fh:
    for line in fh.readlines():
        matrix_by_row.append([int(i) for i in line.rstrip()])

# https://stackoverflow.com/questions/6473679/transpose-list-of-lists
matrix_by_col = list(map(list, zip(*matrix_by_row)))

r_edge = len(matrix_by_row[0]) - 1
b_edge = len(matrix_by_row) - 1


def scenic_score(x: int, y: int) -> int:
    # If tree is on the edge, it is visible
    if x == 0 or x == r_edge or y == 0 or y == b_edge:
        return 0
    #
    h = matrix_by_row[y][x]
    def scenic_score_row(side: List[int], h: int):
        score = 0
        for i in range(0, len(side)):
            if side[i] >= h:
                return score + 1
            score += 1
        return score

    sc_left = scenic_score_row(matrix_by_row[y][x-1::-1], h)
    sc_right = scenic_score_row(matrix_by_row[y][x + 1:], h)
    sc_top = scenic_score_row(matrix_by_col[x][y - 1::-1], h)
    sc_bot = scenic_score_row(matrix_by_col[x][y + 1:], h)
    return sc_left * sc_right * sc_top * sc_bot


highest = 0
for y in range(0, len(matrix_by_row)):
    for x in range(0, len(matrix_by_row[0])):
        sc = scenic_score(x, y)
        if sc > highest:
            highest = sc

print(f'Best spot score: {highest}')
