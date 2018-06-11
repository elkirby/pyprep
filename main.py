#!/usr/bin/env python

import string
from argparse import Action, ArgumentParser
from datetime import datetime as dt
from random import randint


def generate_values(size=100, max_val=100):
    return [randint(0, max_val) for i in range(size)]


def selection_sort(values, debug=False):
    time_start = dt.now()
    for i in range(len(values)):
        min_val_idx = i
        for j in range(i+1, len(values)):
            if values[j] < values[min_val_idx]:
                min_val_idx = j
        values.insert(i, values.pop(min_val_idx))
    if debug:
        print(values)
    time_end = dt.now()
    total = time_end - time_start
    print('selection sort: {}'.format(total))


def insertion_sort(values, debug=False):
    time_start = dt.now()
    for i in range(1, len(values)):
        j = i - 1
        while j >= 0 and values[j + 1] < values[j]:
            values[j], values[j + 1] = values[j + 1], values[j]
            j -= 1
    if debug:
        print(values)
    time_end = dt.now()
    total = time_end - time_start
    print('insertion sort: {}'.format(total))


# assumes base 10, positive integers
def radix_sort(values, debug=False):
    time_start = dt.now()

    def get_buckets(array, level):
        buckets = [[] for i in range(10)]
        for n in array:
            idx = (n // (10 ** level)) % 10
            buckets[idx].append(n)
        return buckets

    def get_list(buckets):
        numbers = []
        for b in buckets:
            for num in b:
                numbers.append(num)
        return numbers

    max_num = max(values)

    iteration = 0
    while 10 ** iteration <= max_num:
        values = get_list(get_buckets(values, iteration))
        iteration += 1
    if debug:
        print(values)
    time_end = dt.now()
    total = time_end - time_start
    print('radix sort: {}'.format(total))


class isUnique(Action):

    def __call__(self, parser, namespace, values, option_string=None):
        ascii_chars = string.printable
        for c in values:
            if c not in ascii_chars:
                print('Non-unique char found: {}'.format(c))
                exit(1)
            ascii_chars = ascii_chars.replace(c, '')
        print('{} has all unique characters. Congratulations.'.format(values))


class CReverse(Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if not values[len(values) - 1] == '\0':
            print('String is not a C string. Please input a valid C-string.')
            exit(1)
        print(values[len(values) - 2::-1] + '\0')


class RDupes(Action):

    def __call__(self, parser, namespace, values, option_string=None):
        no_dupes = ''
        for c in values:
            if c not in no_dupes:
                no_dupes += c
        print(no_dupes)


class Anagrams(Action):

    def __call__(self, parser, namespace, values, option_string=None):
        str1, str2 = values
        fail_str = 'it\'s no good bro'
        for c in str1:
            if str1.count(c) != str2.count(c):
                print(fail_str)
                exit(1)
            else:
                str1 = str1.replace(c, '')
                str2 = str2.replace(c, '')
        if str2:
            print(fail_str)
        else:
            print('congrats! you got yourself an anagram.')


fn_parser = ArgumentParser(description='simple python exercises for arrays and strings')
subparsers = fn_parser.add_subparsers(help='operations')

# Sorting
sorters = subparsers.add_parser('sort', help='Sorting operations')

sorters.add_argument('method',
                     help='Type of sorting algorithm to use',
                     choices=['selection', 'insertion', 'radix'])
sorters.add_argument('values',
                     help='Values to pass to sorting algorithm',
                     nargs='?',
                     default=generate_values())
sorters.add_argument('--autogenerate', '-a', 
                     help='Generate a list of test values for use as sorting input',
                     metavar=('SIZE', 'MAX_VALUE'),
                     nargs=2,
                     type=int)
sorters.add_argument('--debug', '-d',
                     help='Print final array for debug purposes',
                     type=bool,
                     default=False)

# Misc. String operations
string_ops = subparsers.add_parser('str', help='String processing and manipulation')

string_ops.add_argument('--unique', help='Determine if an ASCII string has all unique characters', action=isUnique)
string_ops.add_argument('--reverse', help='Reverse a C-Style string', action=CReverse)
string_ops.add_argument('--duplicates', help='Remove duplicate characters', action=RDupes)
string_ops.add_argument('--anagrams', help='Check if two strings are anagrams', nargs=2, action=Anagrams)


if __name__ == '__main__':
    args = fn_parser.parse_args()
    if args.method:
        if args.autogenerate:
            input = generate_values(args.autogenerate[0], args.autogenerate[1])
            args.values = input
        locals()[args.method + '_sort'](args.values, args.debug)
