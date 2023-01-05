"""
--- Day 16: Proboscidea Volcanium ---
The sensors have led you to the origin of the distress signal: yet another handheld device, just like the one the Elves
gave you. However, you don't see any Elves around; instead, the device is surrounded by elephants! They must have
gotten lost in these tunnels, and one of the elephants apparently figured out how to turn on the distress signal.

The ground rumbles again, much stronger this time. What kind of cave is this, exactly? You scan the cave with your
handheld device; it reports mostly igneous rock, some ash, pockets of pressurized gas, magma... this isn't just a cave,
it's a volcano!

You need to get the elephants out of here, quickly. Your device estimates that you have 30 minutes before the volcano
erupts, so you don't have time to go back out the way you came in.

You scan the cave for other options and discover a network of pipes and pressure-release valves. You aren't sure how
such a system got into a volcano, but you don't have time to complain; your device produces a report (your puzzle
input) of each valve's flow rate if it were opened (in pressure per minute) and the tunnels you could use to move
between the valves.

There's even a valve in the room you and the elephants are currently standing in labeled AA. You estimate it will take
you one minute to open a single valve and one minute to follow any tunnel from one valve to another. What is the most
pressure you could release?

For example, suppose you had the following scan output:

Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
All of the valves begin closed. You start at valve AA, but it must be damaged or jammed or something: its flow rate is
0, so there's no point in opening it. However, you could spend one minute moving to valve BB and another minute opening
it; doing so would release pressure during the remaining 28 minutes at a flow rate of 13, a total eventual pressure
release of 28 * 13 = 364. Then, you could spend your third minute moving to valve CC and your fourth minute opening it,
providing an additional 26 minutes of eventual pressure release at a flow rate of 2, or 52 total pressure released by
valve CC.

Making your way through the tunnels like this, you could probably open many or all of the valves by the time 30 minutes
have elapsed. However, you need to release as much pressure as possible, so you'll need to be methodical. Instead,
consider this approach:

== Minute 1 ==
No valves are open.
You move to valve DD.

== Minute 2 ==
No valves are open.
You open valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You move to valve CC.

== Minute 4 ==
Valve DD is open, releasing 20 pressure.
You move to valve BB.

== Minute 5 ==
Valve DD is open, releasing 20 pressure.
You open valve BB.

== Minute 6 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve AA.

== Minute 7 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve II.

== Minute 8 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve JJ.

== Minute 9 ==
Valves BB and DD are open, releasing 33 pressure.
You open valve JJ.

== Minute 10 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve II.

== Minute 11 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve AA.

== Minute 12 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve DD.

== Minute 13 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve EE.

== Minute 14 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve FF.

== Minute 15 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve GG.

== Minute 16 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve HH.

== Minute 17 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You open valve HH.

== Minute 18 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve GG.

== Minute 19 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve FF.

== Minute 20 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve EE.

== Minute 21 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve EE.

== Minute 22 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve DD.

== Minute 23 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve CC.

== Minute 24 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You open valve CC.

== Minute 25 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 27 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 28 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 29 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 30 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
This approach lets you release the most pressure possible in 30 minutes with this valve layout, 1651.

Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?
"""
from common import read_file
import re
from typing import List, Hashable, Optional


class Valve(object):
    valves = {}

    def __init__(self, name, flow_rate, linked_to):
        self.name = name
        self.is_open = False
        self.flow_rate = int(flow_rate)
        self._linked_to = linked_to.split(', ')
        self.valves[self.name] = self

    @property
    def linked_to(self):
        return [self.valves[i] for i in self._linked_to]

    def __hash__(self):
        #return hash(self.name) ^ hash(self.flow_rate) ^ hash(','.join(self._linked_to))
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, type(self)) and \
            self.name == other.name and self.flow_rate == other.flow_rate and self.linked_to == other.linked_to

    def __repr__(self):
        return f'<Valve {self.name}({self.flow_rate})>'


def is_adjacent(u: Valve, v: Valve):
    if v in u.linked_to:
        return True
    return False


def spf(node_l: List[Hashable], start: Hashable, end: Optional[Hashable] = None):
    """Wikipedia implementation of SPF.
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
    """
    Q = {n for n in node_l}
    dist = {n: float('inf') for n in node_l}
    prev = {n: None for n in node_l}

    dist[start] = 0

    while len(Q) > 0:
        u = [node for node in sorted(Q, key=lambda n: dist[n])][0]
        if u == end:
            return dist, prev
        Q.remove(u)

        for v in [v for v in Q if is_adjacent(u, v)]:
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev


for line in read_file('input/16.txt'):
    line_m = re.match(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)$', line)
    if line_m:
        Valve(*line_m.groups())

print(Valve.valves)

dist_root = {}
for start in Valve.valves.values():
    dist, _ = spf(Valve.valves.values(), start)
    dist_root[start] = dist

relief_valves = [i for i in Valve.valves.values() if i.flow_rate > 0]


def traverse_path(valve_l, start: Valve = Valve.valves['AA'], init_timeleft: int = 30, init_pr: int = 0, level: int = 0):
    global dist_root
    #print(f'{level * " "}traverse_node_path({valve_l}, {start}, {init_timeleft}, {level})')
    max_pr = 0
    best_nh_l = []
    dist = dist_root[start]
    for i in range(len(valve_l)):
        pr = init_pr
        timeleft = init_timeleft
        valve = valve_l[i]
        # Travel to the node
        if timeleft < dist[valve]:
            continue
        timeleft -= dist[valve]
        # Open the valve
        if timeleft < 1:
            continue
        timeleft -= 1
        pr += timeleft * valve.flow_rate
        sub_nh_l = []
        if len(valve_l) > 1 and timeleft > 1:
            valve_sub_l = valve_l[:i] + valve_l[i + 1:]
            sub_nh_l, pr = traverse_path(valve_sub_l, valve, timeleft, pr, level + 1)
        if pr > max_pr:
            max_pr = pr
            best_nh_l = [valve] + sub_nh_l
    return best_nh_l, max_pr


nh_l, max_pr = traverse_path(relief_valves)

print(f'Best relief: {max_pr}, path: {nh_l}')
