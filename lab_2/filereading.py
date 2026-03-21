def read_file(path: str) -> str:
    with open(path, 'r+') as file:
        return file.readline()


def read_vector(line: str) -> list[bool]:
    result = []
    for symb in line:
        if symb == '0':
            result += [False]
        elif symb == '1':
            result += [True]
        else:
            raise ValueError('Uncorrect file format!')
    return result


def read_sequence(path: str) -> list[int]:
    return read_vector(read_file(path))
