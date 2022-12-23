"""
--- Part Two ---
Now, you just need to put all of the packets in the right order. Disregard the blank lines in your list of received
packets.

The distress signal protocol also requires that you include two additional divider packets:

[[2]]
[[6]]
Using the same rules as before, organize all packets - the ones in your list of received packets as well as the two
divider packets - into the correct order.

For the example above, the result of putting the packets in the correct order is:

[]
[[]]
[[[]]]
[1,1,3,1,1]
[1,1,5,1,1]
[[1],[2,3,4]]
[1,[2,[3,[4,[5,6,0]]]],8,9]
[1,[2,[3,[4,[5,6,7]]]],8,9]
[[1],4]
[[2]]
[3]
[[4,4],4,4]
[[4,4],4,4,4]
[[6]]
[7,7,7]
[7,7,7,7]
[[8,7,6]]
[9]
Afterward, locate the divider packets. To find the decoder key for this distress signal, you need to determine the
indices of the two divider packets and multiply them together. (The first packet is at index 1, the second packet is at
index 2, and so on.) In this example, the divider packets are 10th and 14th, and so the decoder key is 140.

Organize all of the packets into the correct order. What is the decoder key for the distress signal?
"""
from common import read_file
from functools import cmp_to_key
from itertools import count
from typing import List, Optional


def compare_lists(left: List[int], right: List[int]) -> Optional[bool]:
    for i in range(0, max(len(left), len(right))):
        try:
            left_item = left[i]
        except IndexError:
            return True
        try:
            right_item = right[i]
        except IndexError:
            return False
        if type(left_item) is int and type(right_item) is int:
            if left_item > right_item:
                return False
            if left_item < right_item:
                return True
        if type(left_item) is list and type(right_item) is int:
            right_item = [right_item]
        if type(left_item) is int and type(right_item) is list:
            left_item = [left_item]
        if type(left_item) is list and type(right_item) is list:
            result = compare_lists(left_item, right_item)
            if result is not None:
                return result
    return None


def sort_by_compare(left, right):
    result = compare_lists(left, right)
    if result is None:
        return 0
    if result:
        return -1
    else:
        return 1


pkts = [
    [[2]],
    [[6]],
]
for line in read_file('input/13.txt'):
    if line != '':
        eval(f'pkts.append({line})')

cmp = cmp_to_key(sort_by_compare)
pkts.sort(key=cmp)
decoder_key = 1
for i in range(0, len(pkts)):
    if pkts[i] == [[2]] or pkts[i] == [[6]]:
        decoder_key *= i + 1

print(f'Decoder key: {decoder_key}')
