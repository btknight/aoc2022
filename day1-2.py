"""
--- Part Two ---
By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the most
Calories of food might eventually run out of snacks.

To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top three
Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks, they still have two backups.

In the example above, the top three Elves are the fourth Elf (with 24000 Calories), then the third Elf (with 11000
Calories), then the fifth Elf (with 10000 Calories). The sum of the Calories carried by these three elves is 45000.

Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
"""
from functools import reduce
from itertools import count
from collections import namedtuple


Elf = namedtuple('Elf', ['num', 'cal'])
ctr = count(1)

elf_l = []

def reset():
    return next(ctr), 0

with open('input/1.txt') as fh:
    highest = None
    cur, accum = reset()
    for line in fh.readlines():
        line = line.strip()
        if line == '':
            elf_l.append(Elf(cur, accum))
            cur, accum = reset()
        else:
            accum += int(line)

top3 = sorted(elf_l, key=lambda x: -x.cal)[:3]
top_cal = [i.cal for i in top3]
total_cal = reduce(lambda x, y: x + y, top_cal)
print(f'Total calorie count: {total_cal}')
