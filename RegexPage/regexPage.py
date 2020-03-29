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
        ['999 999 999                ', 'aaa', '1']
        '''
        #res = re.compile(r'(\d\d\d\s\d\d\d\s\d\d\d)')
        # >999 999 999                <
        res = re.compile(r"(\d\d\d\s\d\d\d\s\d\d\d)")
        return res

    def regexComment():
        '''Comment'''
        res = re.compile(r'[^<td>]([a-zA-Z0-9_])[</td>]$')
        return res
