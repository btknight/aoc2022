"""
--- Day 11: Monkey in the Middle ---
As you finally start making your way upriver, you realize your pack is much lighter than you remember. Just then, one of
the items from your pack goes flying overhead. Monkeys are playing Keep Away with your missing things!

To get your stuff back, you need to be able to predict where the monkeys will throw your items. After some careful
observation, you realize the monkeys operate based on how worried you are about each item.

You take some notes (your puzzle input) on the items each monkey currently has, how worried you are about those items,
and how the monkey makes decisions based on your worry level. For example:

Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
Each monkey has several attributes:

Starting items lists your worry level for each item the monkey is currently holding in the order they will be inspected.
Operation shows how your worry level changes as that monkey inspects an item. (An operation like new = old * 5 means
that your worry level after the monkey inspected the item is five times whatever your worry level was before
inspection.)
Test shows how the monkey uses your worry level to decide where to throw an item next.
If true shows what happens with an item if the Test was true.
If false shows what happens with an item if the Test was false.
After each monkey inspects an item but before it tests your worry level, your relief that the monkey's inspection didn't
damage the item causes your worry level to be divided by three and rounded down to the nearest integer.

The monkeys take turns inspecting and throwing items. On a single monkey's turn, it inspects and throws all of the items
it is holding one at a time and in the order listed. Monkey 0 goes first, then monkey 1, and so on until each monkey has
had one turn. The process of each monkey taking a single turn is called a round.

When a monkey throws an item to another monkey, the item goes on the end of the recipient monkey's list. A monkey that
starts a round with no items could end up inspecting and throwing many items by the time its turn comes around. If a
monkey is holding no items at the start of its turn, its turn ends.

In the above example, the first round proceeds as follows:

Monkey 0:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by 19 to 1501.
    Monkey gets bored with item. Worry level is divided by 3 to 500.
    Current worry level is not divisible by 23.
    Item with worry level 500 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 98.
    Worry level is multiplied by 19 to 1862.
    Monkey gets bored with item. Worry level is divided by 3 to 620.
    Current worry level is not divisible by 23.
    Item with worry level 620 is thrown to monkey 3.
Monkey 1:
  Monkey inspects an item with a worry level of 54.
    Worry level increases by 6 to 60.
    Monkey gets bored with item. Worry level is divided by 3 to 20.
    Current worry level is not divisible by 19.
    Item with worry level 20 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 65.
    Worry level increases by 6 to 71.
    Monkey gets bored with item. Worry level is divided by 3 to 23.
    Current worry level is not divisible by 19.
    Item with worry level 23 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 75.
    Worry level increases by 6 to 81.
    Monkey gets bored with item. Worry level is divided by 3 to 27.
    Current worry level is not divisible by 19.
    Item with worry level 27 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 6 to 80.
    Monkey gets bored with item. Worry level is divided by 3 to 26.
    Current worry level is not divisible by 19.
    Item with worry level 26 is thrown to monkey 0.
Monkey 2:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by itself to 6241.
    Monkey gets bored with item. Worry level is divided by 3 to 2080.
    Current worry level is divisible by 13.
    Item with worry level 2080 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 60.
    Worry level is multiplied by itself to 3600.
    Monkey gets bored with item. Worry level is divided by 3 to 1200.
    Current worry level is not divisible by 13.
    Item with worry level 1200 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 97.
    Worry level is multiplied by itself to 9409.
    Monkey gets bored with item. Worry level is divided by 3 to 3136.
    Current worry level is not divisible by 13.
    Item with worry level 3136 is thrown to monkey 3.
Monkey 3:
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 3 to 77.
    Monkey gets bored with item. Worry level is divided by 3 to 25.
    Current worry level is not divisible by 17.
    Item with worry level 25 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 500.
    Worry level increases by 3 to 503.
    Monkey gets bored with item. Worry level is divided by 3 to 167.
    Current worry level is not divisible by 17.
    Item with worry level 167 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 620.
    Worry level increases by 3 to 623.
    Monkey gets bored with item. Worry level is divided by 3 to 207.
    Current worry level is not divisible by 17.
    Item with worry level 207 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 1200.
    Worry level increases by 3 to 1203.
    Monkey gets bored with item. Worry level is divided by 3 to 401.
    Current worry level is not divisible by 17.
    Item with worry level 401 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 3136.
    Worry level increases by 3 to 3139.
    Monkey gets bored with item. Worry level is divided by 3 to 1046.
    Current worry level is not divisible by 17.
    Item with worry level 1046 is thrown to monkey 1.
After round 1, the monkeys are holding items with these worry levels:

Monkey 0: 20, 23, 27, 26
Monkey 1: 2080, 25, 167, 207, 401, 1046
Monkey 2:
Monkey 3:
Monkeys 2 and 3 aren't holding any items at the end of the round; they both inspected items during the round and threw
them all before the round ended.

This process continues for a few more rounds:

After round 2, the monkeys are holding items with these worry levels:
Monkey 0: 695, 10, 71, 135, 350
Monkey 1: 43, 49, 58, 55, 362
Monkey 2:
Monkey 3:

After round 3, the monkeys are holding items with these worry levels:
Monkey 0: 16, 18, 21, 20, 122
Monkey 1: 1468, 22, 150, 286, 739
Monkey 2:
Monkey 3:

After round 4, the monkeys are holding items with these worry levels:
Monkey 0: 491, 9, 52, 97, 248, 34
Monkey 1: 39, 45, 43, 258
Monkey 2:
Monkey 3:

After round 5, the monkeys are holding items with these worry levels:
Monkey 0: 15, 17, 16, 88, 1037
Monkey 1: 20, 110, 205, 524, 72
Monkey 2:
Monkey 3:

After round 6, the monkeys are holding items with these worry levels:
Monkey 0: 8, 70, 176, 26, 34
Monkey 1: 481, 32, 36, 186, 2190
Monkey 2:
Monkey 3:

After round 7, the monkeys are holding items with these worry levels:
Monkey 0: 162, 12, 14, 64, 732, 17
Monkey 1: 148, 372, 55, 72
Monkey 2:
Monkey 3:

After round 8, the monkeys are holding items with these worry levels:
Monkey 0: 51, 126, 20, 26, 136
Monkey 1: 343, 26, 30, 1546, 36
Monkey 2:
Monkey 3:

After round 9, the monkeys are holding items with these worry levels:
Monkey 0: 116, 10, 12, 517, 14
Monkey 1: 108, 267, 43, 55, 288
Monkey 2:
Monkey 3:

After round 10, the monkeys are holding items with these worry levels:
Monkey 0: 91, 16, 20, 98
Monkey 1: 481, 245, 22, 26, 1092, 30
Monkey 2:
Monkey 3:

...

After round 15, the monkeys are holding items with these worry levels:
Monkey 0: 83, 44, 8, 184, 9, 20, 26, 102
Monkey 1: 110, 36
Monkey 2:
Monkey 3:

...

After round 20, the monkeys are holding items with these worry levels:
Monkey 0: 10, 12, 14, 26, 34
Monkey 1: 245, 93, 53, 199, 115
Monkey 2:
Monkey 3:
Chasing all of the monkeys at once is impossible; you're going to have to focus on the two most active monkeys if you
want any hope of getting your stuff back. Count the total number of times each monkey inspects items over 20 rounds:

Monkey 0 inspected items 101 times.
Monkey 1 inspected items 95 times.
Monkey 2 inspected items 7 times.
Monkey 3 inspected items 105 times.
In this example, the two most active monkeys inspected items 101 and 105 times. The level of monkey business in this
situation can be found by multiplying these together: 10605.

Figure out which monkeys to chase by counting how many items they inspect over 20 rounds. What is the level of monkey
business after 20 rounds of stuff-slinging simian shenanigans?
"""
from common import read_file
import logging
import re
from typing import Callable

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
)

TOTAL_ROUNDS = 20
monkey_playpen = {}


def gen_no_op() -> Callable[[int], None]:
    def do_nothing(item: int) -> None:
        return None
    return do_nothing


class Monkey(object):
    def __init__(self, config_l):
        global monkey_playpen
        self.id = None
        self.item_l = []
        self.op = gen_no_op()
        self.worry_mgmt = lambda x: x // 3
        self.test = gen_no_op()
        self.test_action = {
            True: gen_no_op(),
            False: gen_no_op(),
        }
        self.inspections = 0
        self.parse(config_l)
        monkey_playpen[self.id] = self

    def parse(self, config_l):
        for line in config_l:
            id_m = re.match(r'Monkey (\d+):', line)
            if id_m:
                self.id = int(id_m.group(1))
            item_m = re.match(r'\s+Starting items: (.*)', line)
            if item_m:
                self.item_l = [int(i) for i in item_m.group(1).split(', ')]
            op_m = re.match(r'\s+Operation: new = (.+)', line)
            if op_m:
                def op_eval(op):
                    def do_op(old: int):
                        return eval(op)
                    return do_op
                self.op = op_eval(op_m.group(1))
            test_m = re.match(r'\s*Test: divisible by (\d+)', line)
            if test_m:
                dividend = int(test_m.group(1))
                def div_is_even(dividend):
                    def fn(x):
                        return x / dividend == float(x // dividend)
                    return fn
                self.test = div_is_even(dividend)
            test_true_m = re.match(r'\s*If true: throw to monkey (\d+)', line)
            if test_true_m:
                self.test_action[True] = self.toss_cb(int(test_true_m.group(1)))
            test_false_m = re.match(r'\s*If false: throw to monkey (\d+)', line)
            if test_false_m:
                self.test_action[False] = self.toss_cb(int(test_false_m.group(1)))

    def toss_cb(self, target):
        def toss(item: int) -> None:
            global monkey_playpen
            logging.debug(f'  Tossing item {item} to Monkey {target}.')
            monkey_playpen[target].catch(item)
        return toss

    def catch(self, item):
        logging.debug(f'  Monkey {self.id} caught {item}.')
        self.item_l.append(item)

    def run(self):
        logging.debug(f'Monkey {self.id}:')
        while len(self.item_l) > 0:
            item = self.item_l.pop(0)
            logging.debug(f' Monkey inspects an item with a worry level of {item}.')
            worry_level = self.op(item)
            logging.debug(f'  Worry level goes to {worry_level}.')
            worry_level = self.worry_mgmt(worry_level)
            logging.debug(f'  Monkey gets bored with item. Worry level is scaled back to {worry_level}.')
            result = self.test(worry_level)
            logging.debug(f'  Current worry level did {" not" if not result else ""} pass the test.')
            self.test_action[result](worry_level)
            self.inspections += 1

    def __str__(self):
        return f'Monkey {self.id} :: insp: {self.inspections}; items: ' + ', '.join([str(i) for i in self.item_l])

    def __repr__(self):
        return f'<Monkey({self.id}, {self.item_l}, {self.op}, {self.test}, {self.test_action})>'

buffer_l = []
for line in read_file('input/11.txt'):
    if line == '':
        Monkey(buffer_l)
        buffer_l = []
    else:
        buffer_l.append(line)
#
if len(buffer_l) > 0:
    Monkey(buffer_l)

for round in range(1, TOTAL_ROUNDS + 1):
    print(f'!! Round {round} !!')
    for k, m in sorted(monkey_playpen.items(), key=lambda x: x[0]):
        m.run()
    for k, m in sorted(monkey_playpen.items(), key=lambda x: x[0]):
        print(str(m))

two_most_active = [m.inspections for m in sorted(monkey_playpen.values(), key=lambda x: -x.inspections)]
monkey_business = two_most_active[0] * two_most_active[1]
print(f'Monkey business: {monkey_business}')
