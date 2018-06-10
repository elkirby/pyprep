#!/usr/bin/env python

import string
from argparse import ArgumentParser, Action
from datetime import datetime as dt


class InsertSort(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        time_start = dt.now()
        for i in range(1, len(values)):
            j = i - 1
            while j >= 0 and values[j + 1] < values[j]:
                values[j], values[j + 1] = values[j + 1], values[j]
                j -= 1
        print(values)
        time_end = dt.now()
        total = time_end - time_start
        print('time taken: {}'.format(total))


class RadixSort(Action):
    # assumes base 10, positive integers
    def __call__(self, parser, namespace, values, option_string=None):
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
        array = values
        while 10 ** iteration <= max_num:
            array = get_list(get_buckets(array, iteration))
            iteration += 1
        print(array)
        time_end = dt.now()
        total = time_end - time_start
        print('time taken: {}'.format(total))


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

# Sorting
fn_parser.add_argument('--insert-sort', help='Perform an insert sort on an array', nargs='*', type=int,
                       action=InsertSort)
fn_parser.add_argument('--radix-sort', help='Perform a radix sort on an array', nargs='*', type=int, action=RadixSort)

# Misc. String operations
fn_parser.add_argument('--unique', help='Determine if an ASCII string has all unique characters', action=isUnique)
fn_parser.add_argument('--reverse', help='Reverse a C-Style string', action=CReverse)
fn_parser.add_argument('--duplicates', help='Remove duplicate characters', action=RDupes)
fn_parser.add_argument('--anagrams', help='Check if two strings are anagrams', nargs=2, action=Anagrams)

if __name__ == '__main__':
    fn_parser.parse_args()
