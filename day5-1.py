"""
--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in
stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be
rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or
fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are
rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which
crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N
is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a
single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack
to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack
1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate
to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up
below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in
stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?
"""
from collections import deque, defaultdict
import re

count_overlaps = 0
num_stacks = 0
setup_section = True
crate_init_l = []


def init_stacks(num_stacks, crate_init_l):
    stacks = defaultdict(deque)
    for line in crate_init_l:
        crate_l = []
        while len(line) > 0:
            crate_l.append(line[1:2])
            line = line[4:]
        for i in range(0, len(crate_l)):
            if crate_l[i] != ' ':
                stacks[i+1].append(crate_l[i])
    return stacks


with open('input/5.txt') as fh:
    for line in fh.readlines():
        line = line.rstrip()
        if setup_section:
            if '[' in line:
                crate_init_l.append(line)
            else:
                # Get last number from the list of stacks
                num_stacks = int([i for i in line.split(' ') if i != ''][-1])
                stacks = init_stacks(num_stacks, reversed(crate_init_l))
                setup_section = False
        else:
            cmd = re.match(r'^move (\d+) from (\d+) to (\d+)', line)
            if cmd:
                qty, src, dst = [int(i) for i in cmd.groups()]
                for _ in range(0, qty):
                    stacks[dst].append(stacks[src].pop())

msg = ''
for i in sorted(stacks.keys()):
    msg += stacks[i][-1]

print(f'Crates on top: {msg}')
