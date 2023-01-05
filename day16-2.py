"""
--- Part Two ---
You're worried that even with an optimal approach, the pressure released won't be enough. What if you got one of the
elephants to help you?

It would take you 4 minutes to teach an elephant how to open the right valves in the right order, leaving you with only
26 minutes to actually execute your plan. Would having two of you working together be better, even if it means having
less time? (Assume that you teach the elephant before opening any valves yourself, giving you both the same full 26
minutes.)

In the example above, you could teach the elephant to help you as follows:

== Minute 1 ==
No valves are open.
You move to valve II.
The elephant moves to valve DD.

== Minute 2 ==
No valves are open.
You move to valve JJ.
The elephant opens valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You open valve JJ.
The elephant moves to valve EE.

== Minute 4 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve II.
The elephant moves to valve FF.

== Minute 5 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve AA.
The elephant moves to valve GG.

== Minute 6 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve BB.
The elephant moves to valve HH.

== Minute 7 ==
Valves DD and JJ are open, releasing 41 pressure.
You open valve BB.
The elephant opens valve HH.

== Minute 8 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve CC.
The elephant moves to valve GG.

== Minute 9 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve CC.
The elephant moves to valve FF.

== Minute 10 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant moves to valve EE.

== Minute 11 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant opens valve EE.

(At this point, all valves are open.)

== Minute 12 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 20 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
With the elephant helping, after 26 minutes, the best you could do would release a total of 1707 pressure.

With you and an elephant working together for 26 minutes, what is the most pressure you could release?
"""
from common import read_file
from collections import namedtuple
import re
from typing import List, Hashable, Optional, Tuple


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


PlayerFrame = namedtuple('PlayerFrame', ['start', 'timeleft'])


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

relief_valves = [i for i in sorted(Valve.valves.values(), key=lambda x: -x.flow_rate) if i.flow_rate > 0]
aa = Valve.valves['AA']


def path_cost(start: Valve, end: Valve):
    """Returns the cost of traveling from start to end and opening the valve at end."""
    global dist_root
    dist = dist_root[start]
    return 1 + dist[end]


def compute_pr(pf: PlayerFrame, end: Valve) -> Tuple[PlayerFrame, int]:
    # Travel to the node (dist[end]) and open the valve (+ 1)
    timeleft = pf.timeleft - path_cost(pf.start, end)
    if timeleft < 1:
        return pf, 0
    new_pf = PlayerFrame(end, timeleft)
    return new_pf, timeleft * end.flow_rate


def can_reach(pf_l, end):
    """True if any player can reach the goal in time, otherwise False."""
    for pf in pf_l:
        if path_cost(pf.start, end) < pf.timeleft:
            return True
    return False


def traverse_path(valve_l,
                  pf_t: Tuple[PlayerFrame, PlayerFrame] = (PlayerFrame(aa, 26), PlayerFrame(aa, 26)),
                  init_pr: int = 0, level: int = 0):
    """Recursively backtracks over the game tree."""
    #print(f'{level * " "}[{level}]traverse_node_path({valve_l}, {pf_t}, {level})')
    max_pr = init_pr
    best_nh_l = []
    if len(valve_l) == 1:
        valve = valve_l[0]
        for i in range(len(pf_t)):
            timeleft, pr = compute_pr(pf_t[i], valve)
            pr += init_pr
            if pr > max_pr:
                max_pr = pr
                best_nh_l = [valve]
        return best_nh_l, max_pr
    search_space = len(valve_l)
    for i in range(search_space):
        for j in range(i + 1, search_space):
            swaps = len(pf_t)
            if pf_t[0].start == pf_t[1].start:
                swaps = 1
            for k in range(swaps):
                if level < 2:
                    print(f'{level * "  "}[{level}] i = {i}/{search_space}, j = {j}/{search_space}, k = {k}/{swaps}')
                # Check player 1 vs player 2
                l = (k + 1) % len(pf_t)
                valve_0 = valve_l[i]
                pf_0, pr_0 = compute_pr(pf_t[k], valve_0)
                success_0 = pr_0 > 0
                valve_1 = valve_l[j]
                pf_1, pr_1 = compute_pr(pf_t[l], valve_1)
                success_1 = pr_1 > 0
                pr = init_pr + pr_0 + pr_1
                sub_nh_l = []
                if len(valve_l) > 2 and (success_0 or success_1) and (pf_0.timeleft > 1 or pf_1.timeleft > 1):
                    valve_sub_l = valve_l.copy()
                    if success_1:
                        del valve_sub_l[j]
                    if success_0:
                        del valve_sub_l[i]
                    sub_pf_t = (pf_0, pf_1)
                    valve_sub_l = [i for i in valve_sub_l if can_reach(sub_pf_t, i)]
                    if len(valve_sub_l) > 0:
                        sub_nh_l, pr = traverse_path(valve_sub_l, sub_pf_t, pr, level + 1)
                if pr > max_pr:
                    max_pr = pr
                    best_nh_l = [([valve_0], [valve_1])] + sub_nh_l
    return best_nh_l, max_pr


nh_l, max_pr = traverse_path(relief_valves)

print(f'Best relief: {max_pr}, path: {nh_l}')
