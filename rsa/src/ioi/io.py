"""
Contains IO functions to help on read and write of data
"""


def write(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)


def read(filename, mode='rb'):
    with open(filename, mode) as f:
        return f.read()


def read_key(filename, mode='r'):
    data = ''

    with open(filename, mode) as f:
        data = f.read()

    # TODO: parse key and return a dict
    return data


def write_key(filename, key, mode='wb'):
    with open(filename, mode) as f:
        f.write('')
