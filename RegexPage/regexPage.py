#! /usr/bin/python3

import re
from GetWeb_Parser import getWeb_parser

class RegexPage():
    '''Place to configure regex.'''

    def regexNumber():
        '''Number'''
        res = re.compile(r'(\d\d\d(\s|-)\d\d\d(\s|-)\d\d\d)')

        # res2 = re.compile(r'(((\+\d\d\s)|(.{0}))(\d\d(\s|-)\d\d\d(\s|-)\d\d(\s|-)\d\d)|(\(\d\d\d\)(\s|-|.)\d\d(\s|-|.)\d\d(\s|-|.)\d\d\d)|(\(\d\d\)(\s|-|.)\d\d(\s|-|.)\d\d\d(\s|-|.)\d\d)|((\s|'')\d{9}(\s|''))|(\d\d\d(\s|-|.)\d\d\d(\s|-|.)\d\d\d)|((\(|'')(\+|'')((00\d\d)|(\d\d)|(''))(\)|'')(\s|-|'')\d\d\d(\s|-|'')\d\d\d(\s|-|'')\d\d\d$))')

        return res

    def regexComment():
        '''Comment'''
        res = re.compile(r'[^<td>]([a-zA-Z0-9_])[</td>]$')
        return res
