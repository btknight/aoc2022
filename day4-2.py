"""
--- Part Two ---
It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number of
pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap, while the remaining four pairs (5-7,7-9,
2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:

5-7,7-9 overlaps in a single section, 7.
2-8,3-7 overlaps all of the sections 3 through 7.
6-6,4-6 overlaps in a single section, 6.
2-6,4-8 overlaps in sections 4, 5, and 6.
So, in this example, the number of overlapping assignment pairs is 4.

In how many assignment pairs do the ranges overlap?
"""
from typing import Set

def parse_list(s) -> Set[int]:
    s_0, s_f = s.split('-')
    return {i for i in range(int(s_0), int(s_f) + 1)}

count_overlaps = 0
with open('input/4.txt') as fh:
    for line in fh.readlines():
        p = line.strip().split(',')
        s1 = parse_list(p[0])
        s2 = parse_list(p[1])
        if len(s1 & s2) > 0:
            count_overlaps += 1

print(f'Overlaps: {count_overlaps}')
