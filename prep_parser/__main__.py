#!/usr/bin/env python

import string
import sys
from argparse import Action, ArgumentParser
from datetime import datetime as dt
from random import randint, randrange

# Utilities
def generate_values(size=100, max_val=100):
    return [randint(0, max_val) for i in range(size)]


# Sort
def selection_sort(values):
    time_start = dt.now()
    for i in range(len(values)):
        min_val_idx = i
        for j in range(i+1, len(values)):
            if values[j] < values[min_val_idx]:
                min_val_idx = j
        values.insert(i, values.pop(min_val_idx))
    
    print(values)
    time_end = dt.now()
    total = time_end - time_start
    print('selection sort: {}'.format(total))


def insertion_sort(values):
    time_start = dt.now()
    for i in range(1, len(values)):
        j = i - 1
        while j >= 0 and values[j + 1] < values[j]:
            values[j], values[j + 1] = values[j + 1], values[j]
            j -= 1
    
    print(values)
    time_end = dt.now()
    total = time_end - time_start
    print('insertion sort: {}'.format(total))


def counting_sort(values):
    time_start = dt.now()
    max_value = max(values)

    num_counts = [0] * (max_value + 1)

    for item in values:
        num_counts[item] += 1

    array_idx = 0
    for item, count in enumerate(num_counts):

        for _ in range(count):
            values[array_idx] = item
            array_idx += 1

    print(values)
    total = dt.now() - time_start
    print('counting sort: {}'.format(total))


def radix_sort(values):
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

    max_num = max(values) if values else -1

    iteration = 0
    while 10 ** iteration <= max_num:
        values = get_list(get_buckets(values, iteration))
        iteration += 1
    
    print(values)
    time_end = dt.now()
    total = time_end - time_start
    print('radix sort: {}'.format(total))
    return values


# String Methods
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


# Array manipulations
def product_of_idx(values):
    # greedy algorithm approach, O(n)
    time_start = dt.now()
    product_array = [None] * len(values)
    total_so_far = 1

    # product of all values before i
    for i in range(len(values)):
        product_array[i] = total_so_far
        total_so_far *= values[i]
    
    # now product of all values after i
    # start at end and go back
    total_so_far = 1
    for i in range(len(values) - 1, -1, -1):
        product_array[i] *= total_so_far
        total_so_far *= values[i]
    
    print(product_array)
    time_end = dt.now()
    print('time taken: {}'.format(time_end - time_start))


def highest_product_of_3(values):
    # greedy algorithm approach, O(n) time, O(1) space
    time_start = dt.now()
    # start with first 3
    if len(values) < 3:
        print('Need at least 3 values!')
        exit(1)
    highest = max(values[0], values[1])
    lowest = min(values[0], values[1])
    highest_product_of_2 = values[0] * values[1]
    lowest_product_of_2 = values[0] * values[1]
    highest_product_of_3 = values[0] * values[1] * values[2]

    for i in range(2, len(values)):
        current = values[i]
        # new highest product of 3?
        highest_product_of_3 = max(highest_product_of_3,
                                   current * highest_product_of_2,
                                   current * lowest_product_of_2)
        
        # new highest product of 2?
        highest_product_of_2 = max(highest_product_of_2,
                                   current * highest,
                                   current * lowest)

        # new lowest product of 2?
        lowest_product_of_2 = min(lowest_product_of_2,
                                  current * highest,
                                  current * lowest)

        # new highest or lowest?
        highest = max(highest, current)
        lowest = min(lowest, current)

    print(highest_product_of_3)
    time_end = dt.now()
    print('time taken: {}'.format(time_end - time_start))


def is_single_riffle(cards):
    """
    Single Riffle
    Originally, all cards are in order, i.e. 1, 2, 3 .. 52
    Split in half, half1 is 1 .. 26, half2 is 27 .. 52
    If it is a single riffle, while cards, check for perfect ascending order
    of each side
    """
    time_start = dt.now()
    if len(cards) != 52:
        print('Improper deck length. A full deck is 52 cards.')
        exit(1)
    current = 0
    is_riffle = True
    deck = [r for r in range(1, 53)]
    half1 = deck[:len(deck)//2]
    half2 = deck[len(deck)//2:]
    half1_idx = 0
    half2_idx = 0
 
    for card in cards:
        
        if half1_idx < 26 and card == half1[half1_idx]:
            half1_idx += 1

        elif half2_idx < 26 and card == half2[half2_idx]:
            half2_idx += 1

        else:
            is_riffle = False
            break

    print('Is single riffle: %s' % is_riffle)
    time_end = dt.now()
    print('time taken: {}'.format(time_end - time_start))


def shuffle(values):
    # Fisher-Yates / Knuth Shuffle
    time_start = dt.now()

    if len(values) > 1:
        for i in range(len(values)):
            random_index = randrange(i, len(values))
            if random_index != i:
                values[i], values[random_index] = \
                        values[random_index], values[i]

    print(values)
    time_end = dt.now()
    print('time taken: {}'.format(time_end - time_start))


def binary_search(values):
    time_start = dt.now()
    idx_of = -1
    search = None
    if len(values) > 1:
        search = values[-1]
        values = values[:-1]
        values = radix_sort(values)

        floor = -1
        ceiling = len(values)
        while floor + 1 < ceiling:
            size = (ceiling - floor) // 2
            guess = floor + size
            if values[guess] == search:
                idx_of = guess
            elif values[guess] < search:
                floor = guess
            else:
                ceiling = guess
            if idx_of != -1:
                break

    print('Search value: %s' % search)
    print('Index: %s' % idx_of)
    time_end = dt.now()
    print('time taken: {}'.format(time_end - time_start))


def rotation_point(values):
    time_start = dt.now()
    """
    Assume sorted. Somewhere in list, list[i] < list[i-1]
    Account for rotation point being the first element.
    Brute-force approach can be done in O(N)
    By modifying binary search, can be done in O(lg(N))
    """
    rotation_point = 0
    if len(values) > 1:
        first_word = values[0]
        floor = 0
        ceiling = len(values) - 1
        while floor < ceiling - 1:
            guess = floor + ((ceiling - floor) // 2)

            # Check if floor is first word or whether it's higher than it
            if values[guess] >= first_word:
                floor = guess
            else:
                ceiling = guess
        
        rotation_point = ceiling
    print('Rotation point: %s' % rotation_point)
    total = dt.now() - time_start
    print('Time taken: {}'.format(total))


# Parser
fn_parser = ArgumentParser(description='simple python exercises for arrays and strings')
subparsers = fn_parser.add_subparsers(help='operations')

## sorters
sorters = subparsers.add_parser('sort', help='Sorting operations')
sorters.add_argument('method',
                     help='Type of sorting algorithm to use',
                     choices=['selection', 'insertion', 'radix', 'counting'])
sorters.add_argument('values',
                     help='Values to pass to sorting algorithm',
                     nargs='*',
                     type=int,
                     default=[])
sorters.add_argument('--autogenerate', '-a',
                     help='Generate a list of test values for use as sorting input',
                     metavar=('SIZE', 'MAX_VALUE'),
                     nargs=2,
                     type=int)

## string operations
string_ops = subparsers.add_parser('str', help='String processing and manipulation')

string_ops.add_argument('--unique', help='Determine if an ASCII string has all unique characters', action=isUnique)
string_ops.add_argument('--reverse', help='Reverse a C-Style string', action=CReverse)
string_ops.add_argument('--duplicates', help='Remove duplicate characters', action=RDupes)
string_ops.add_argument('--anagrams', help='Check if two strings are anagrams', nargs=2, action=Anagrams)

## array functions
array_ops = subparsers.add_parser('arrays', help='Misc. array processing and manipulation')
array_parsers = array_ops.add_subparsers(help='Array operations separated by allowed input.')
int_arrays = array_parsers.add_parser('int', help='integer specific array operations')
int_arrays.add_argument('problem',
                     help='Which problem to test',
                     choices=['product_of_idx', 'highest_product_of_3',
                              'is_single_riffle', 'binary_search'])
int_arrays.add_argument('values',
                     help='Values to pass to problem',
                     nargs='*',
                     type=int,
                     default=[])
str_arrays = array_parsers.add_parser('str', help='string array operations')
str_arrays.add_argument('problem',
                     help='Which problem to test',
                     choices=['shuffle', 'rotation_point'])
str_arrays.add_argument('values',
                     help='Values to pass to problem',
                     nargs='*',
                     type=str,
                     default=[])
array_ops.add_argument('--autogenerate', '-a',
                     help='Generate a list of test values for use as input',
                     metavar=('SIZE', 'MAX_VALUE'),
                     nargs=2,
                     type=int)


def main():
    if len(sys.argv) == 1:
        fn_parser.print_help()
        exit(1)
    args = fn_parser.parse_args()
    if getattr(args, 'method', None):
        if args.autogenerate:
            input = generate_values(args.autogenerate[0], args.autogenerate[1])
            args.values = input
        globals()[args.method + '_sort'](args.values)
    elif getattr(args, 'problem', None):
        if args.autogenerate:
            input = generate_values(args.autogenerate[0], args.autogenerate[1])
            args.values = input
        globals()[args.problem](args.values)

if __name__ == '__main__':
    main()
