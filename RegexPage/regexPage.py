#! /usr/bin/python3

import re
from GetWeb_Parser import getWeb_parser

class RegexPage():
    '''Place to configure regex.'''

    def regexPage():
        '''Number'''
        #res = re.compile(r'(\d\d\d\s\d\d\d\s\d\d\d)')
        # >732 084 017                <
        res = re.compile(r'>(\d\d\d\s\d\d\d\s\d\d\d\s+)<|(\d\d\d\d\d\d\d\d\d)')
        return res
    def regexNumber():
        '''
        ['579 022 686                ', 'aaa', '1']
        '''
        #res = re.compile(r'(\d\d\d\s\d\d\d\s\d\d\d)')
        # >732 084 017                <
        res = re.compile(r"(\d\d\d\s\d\d\d\s\d\d\d)")
        return res

    def regexComment():
        '''Comment'''
        res = re.compile(r'[^<td>]([a-zA-Z0-9_])[</td>]$')
        return res

# lyrics = '12 drummers drumming, 10 pipers piping, 9 lords of leaping'
# xmasRegex = re.compile(r'\d+\s\w+')
