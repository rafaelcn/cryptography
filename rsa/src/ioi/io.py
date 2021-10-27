"""
Contains IO functions to help on read and write of data
"""

import json


def write(filename, data):
    with open(filename, 'w') as f:
        f.write(data)


def write_cryptogram(filename, encrypted_data: tuple, mode='w'):
    with open(filename, mode) as f:
        f.write(f'{encrypted_data}')


def read_cryptogram(filename, mode='r'):
    data = ''

    with open(filename, mode) as f:
        data = f.read()

    data = data.replace('\'', "\"")
    cryptogram = json.loads(data)

    return cryptogram


def read(filename, mode='r'):
    with open(filename, mode) as f:
        return f.read()


def read_key(filename, mode='r'):
    data = ''

    with open(filename, mode) as f:
        data = f.read()

    data = data.replace('\'', "\"")
    key = json.loads(data)

    return key


def write_key(filename, key: dict, mode='w'):
    with open(filename, mode) as f:
        f.write(f'{key}')
