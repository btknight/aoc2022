"""
--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear
much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input).
For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files).
The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and
listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

cd means change directory. This changes which directory is the current directory, but the specific result depends on the
argument:
cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the
current directory.
cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all of the files and directories immediately contained by the current directory:
123 abc means that the current directory contains a file named abc with size 123.
dir xyz means that the current directory contains a directory named xyz.
Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These
directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion.
To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the
sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic
size.)

The total sizes of the directories above can be found as follows:

The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596),
plus file i indirectly (a contains e which contains i).
Directory d has total size 24933642.
As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes.
In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this
example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those
directories?
"""
from functools import reduce
import re

class Dir(object):
    def __init__(self, name):
        self.name = name
        self.filesizes_l = []
        self.subdir_d = {}
        self.parent = None

    @property
    def path(self):
        parent_path = self.parent.path if self.parent is not None else ''
        has_trailing_slash = parent_path != '' and parent_path[-1] != '/'
        is_root = self.name == '/'
        self_name = f'/{self.name}' if has_trailing_slash and not is_root else self.name
        return parent_path + self_name

    @property
    def root(self):
        obj = self
        while obj.parent is not None:
            obj = obj.parent
        return obj

    def mkdir(self, name):
        if name not in self.subdir_d:
            new_dir = Dir(name)
            self.subdir_d[name] = new_dir
            new_dir.parent = self
        return self.subdir_d[name]

    @property
    def size(self):
        size = 0
        if len(self.filesizes_l) > 0:
            size = reduce(lambda x, y: x + y, self.filesizes_l)
        for subdir in self.subdir_d.values():
            size += subdir.size
        return size

    def get_all_dir_sizes(self):
        dir_size_l = [(str(self), self.size)]
        for subdir in self.subdir_d.values():
            dir_size_l.extend(subdir.get_all_dir_sizes())
        return dir_size_l

    def __repr__(self):
        return self.path

in_ls = False
root = Dir('/')
current_dir = root

with open('input/7.txt') as fh:
    for line in fh.readlines():
        cmd_m = re.match(r'^\$\s+(\S+)\s*(\S*)', line)
        if cmd_m:
            in_ls = False
            cmd, arg = cmd_m.groups()
            if cmd == 'cd':
                if arg == '/':
                    current_dir = root
                elif arg == '..':
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.subdir_d[arg]
            if cmd == 'ls':
                in_ls = True
        if in_ls:
            dir_m = re.match(r'dir (\S+)', line)
            if dir_m:
                current_dir.mkdir(dir_m.group(1))
            file_m = re.match(r'(\d+) (\S+)', line)
            if file_m:
                current_dir.filesizes_l.append(int(file_m.group(1)))


all_sizes_l = root.get_all_dir_sizes()
size_l = [(d, s) for d, s in all_sizes_l if s <= 100000]
size = reduce(lambda x, y: x + y, [s for d, s in size_l])
print(f'Size of all dirs of at most 100000: {size}')
