"""
--- Part Two ---
You're worried you might not ever get your items back. So worried, in fact, that your relief that a monkey's inspection
didn't damage an item no longer causes your worry level to be divided by three.

Unfortunately, that relief was all that was keeping your worry levels from reaching ridiculous levels. You'll need to
find another way to keep your worry levels manageable.

At this rate, you might be putting up with these monkeys for a very long time - possibly 10000 rounds!

With these new rules, you can still figure out the monkey business after 10000 rounds. Using the same example above:

== After round 1 ==
Monkey 0 inspected items 2 times.
Monkey 1 inspected items 4 times.
Monkey 2 inspected items 3 times.
Monkey 3 inspected items 6 times.

== After round 20 ==
Monkey 0 inspected items 99 times.
Monkey 1 inspected items 97 times.
Monkey 2 inspected items 8 times.
Monkey 3 inspected items 103 times.

== After round 1000 ==
Monkey 0 inspected items 5204 times.
Monkey 1 inspected items 4792 times.
Monkey 2 inspected items 199 times.
Monkey 3 inspected items 5192 times.

== After round 2000 ==
Monkey 0 inspected items 10419 times.
Monkey 1 inspected items 9577 times.
Monkey 2 inspected items 392 times.
Monkey 3 inspected items 10391 times.

== After round 3000 ==
Monkey 0 inspected items 15638 times.
Monkey 1 inspected items 14358 times.
Monkey 2 inspected items 587 times.
Monkey 3 inspected items 15593 times.

== After round 4000 ==
Monkey 0 inspected items 20858 times.
Monkey 1 inspected items 19138 times.
Monkey 2 inspected items 780 times.
Monkey 3 inspected items 20797 times.

== After round 5000 ==
Monkey 0 inspected items 26075 times.
Monkey 1 inspected items 23921 times.
Monkey 2 inspected items 974 times.
Monkey 3 inspected items 26000 times.

== After round 6000 ==
Monkey 0 inspected items 31294 times.
Monkey 1 inspected items 28702 times.
Monkey 2 inspected items 1165 times.
Monkey 3 inspected items 31204 times.

== After round 7000 ==
Monkey 0 inspected items 36508 times.
Monkey 1 inspected items 33488 times.
Monkey 2 inspected items 1360 times.
Monkey 3 inspected items 36400 times.

== After round 8000 ==
Monkey 0 inspected items 41728 times.
Monkey 1 inspected items 38268 times.
Monkey 2 inspected items 1553 times.
Monkey 3 inspected items 41606 times.

== After round 9000 ==
Monkey 0 inspected items 46945 times.
Monkey 1 inspected items 43051 times.
Monkey 2 inspected items 1746 times.
Monkey 3 inspected items 46807 times.

== After round 10000 ==
Monkey 0 inspected items 52166 times.
Monkey 1 inspected items 47830 times.
Monkey 2 inspected items 1938 times.
Monkey 3 inspected items 52013 times.
After 10000 rounds, the two most active monkeys inspected items 52166 and 52013 times. Multiplying these together, the
level of monkey business in this situation is now 2713310158.

Worry levels are no longer divided by three after each item is inspected; you'll need to find another way to keep your
worry levels manageable. Starting again from the initial state in your puzzle input, what is the level of monkey
business after 10000 rounds?
"""
from common import read_file
import logging
import re
from typing import Callable

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
)

TOTAL_ROUNDS = 10000
monkey_playpen = {}

scale_back = 1
def scale_back_number(num: int):
    global scale_back
    return num % scale_back


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
        self.worry_mgmt = scale_back_number
        self.test = gen_no_op()
        self.test_action = {
            True: gen_no_op(),
            False: gen_no_op(),
        }
        self.inspections = 0
        self.parse(config_l)
        monkey_playpen[self.id] = self

    def parse(self, config_l):
        global scale_back
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
                        return x % dividend == 0
                    return fn
                self.test = div_is_even(dividend)
                scale_back *= dividend
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
