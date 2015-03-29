from __future__ import print_function

import struct
import ctypes

from itertools import izip_longest

__author__ = 'anton-goy'


def varbyte_compress(numbers):
    return ''.join([varbyte_compress_number(n) for n in numbers])


def varbyte_compress_number(number):
    if number < 128:
        return chr(number ^ 128)

    decomposition = []

    while number >= 128:
        number, remainder = divmod(number, 128)
        decomposition.append(remainder)

    decomposition.append(number)
    encode_string = b''

    for i, n in enumerate(reversed(decomposition)):
        if i != len(decomposition) - 1:
            encode_string += chr(n)
        else:
            encode_string += chr(n ^ 128)

    return encode_string


def varbyte_uncompress(byte_string):
    decode_numbers = []

    current_number = []
    for byte in byte_string:
        byte_number = ord(byte)

        if byte_number >= 128:
            byte_number -= 128
            current_number.append(byte_number)

            new_decode_number = sum([n * (128 ** i) for i, n in enumerate(reversed(current_number))])
            decode_numbers.append(new_decode_number)
            current_number = []
        else:
            current_number.append(byte_number)

    return decode_numbers


def to_gaps(numbers):
    return [n - numbers[i - 1] if i != 0 else n for i, n in enumerate(numbers)]


def from_gaps(gaps):
    n = len(gaps)
    for i, gap in enumerate(gaps, 1):
        if i != n:
            gaps[i] += gap

    return gaps


def simple9_compress(numbers):
    selectors = [(0, 28, 1, 2 ** 1),
                 (1, 14, 2, 2 ** 2),
                 (2, 9, 3, 2 ** 3),
                 (3, 7, 4, 2 ** 4),
                 (4, 5, 5, 2 ** 5),
                 (5, 4, 7, 2 ** 7),
                 (6, 3, 9, 2 ** 9),
                 (7, 2, 14, 2 ** 14),
                 (8, 1, 28, 2 ** 28)]

    encode_numbers = []
    current_number = 0

    n_numbers = len(numbers)
    i = 0
    rest = n_numbers - i

    while i < n_numbers:
        for code, amount, length, limit in selectors:
            if amount > rest:
                continue

            numbers_slice = numbers[i:i + amount]

            for n in numbers_slice:
                if n >= limit:
                    break
            else:
                current_number |= code << 28
                shift = 28 - length
                for x in numbers_slice:
                    current_number |= x << shift
                    shift -= length
                encode_numbers.append(ctypes.c_uint32(current_number))

                current_number = 0
                i += amount
                rest = n_numbers - i

                break

    return ''.join([struct.pack('I', n.value) for n in encode_numbers])


def simple9_uncompress(encode_string):
    selectors = {0: (28, 1),
                 1: (14, 2),
                 2: (9, 3),
                 3: (7, 4),
                 4: (5, 5),
                 5: (4, 7),
                 6: (3, 9),
                 7: (2, 14),
                 8: (1, 28)}

    decode_numbers = []

    def grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)

    for num in grouper(encode_string, 4):
        num = struct.unpack('I', ''.join(num))[0]
        code = num >> 28
        amount, length = selectors[code]
        mask = (2 ** length - 1) << (28 - length)

        if 28 % length == 0:
            stop = -length
        else:
            stop = 0

        for i in range(28 - length, stop, -length):
            decode_numbers.append((num & mask) >> i)
            mask >>= length

    return decode_numbers