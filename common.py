def read_file(file_name: str):
    with open(file_name) as fh:
        for line in fh.readlines():
            yield line.rstrip()
    return
