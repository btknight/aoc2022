"""
--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least
30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165;
this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the
update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can
run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.
Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are
both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is
the total size of that directory?
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


unused_space = 70000000 - root.size
all_sizes_l = root.get_all_dir_sizes()
size_l = sorted([(d, s) for d, s in all_sizes_l if s >= 30000000 - unused_space], key=lambda x: x[1])
candidate = size_l[0]
print(f'Candidate dir: {candidate}')
