"""
--- Part Two ---
Your device's communication system is correctly detecting packets, but still isn't working. It looks like it also needs
to look for messages.

A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters rather
than 4.

Here are the first positions of start-of-message markers for all of the above examples:

mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
How many characters need to be processed before the first start-of-message marker is detected?
"""

accum = 0
with open('input/6.txt') as fh:
    for line in fh.readlines():
        ctr = 14
        while len(line) > 0:
            s = set(line[:14])
            if not len(s) == 14:
                line = line[1:]
                ctr += 1
            else:
                print(f'SOP found: {ctr}')
                exit()

