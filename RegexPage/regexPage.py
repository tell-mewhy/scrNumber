#! /usr/bin/python3

import re
from GetWeb_Parser import getWeb_parser

class RegexPage():
    '''Place to configure regex.'''

    def regexNumber():
        '''Number'''
        #res = re.compile(r'(\d\d\d\s\d\d\d\s\d\d\d)')
        # >999 999 999                <
        res = re.compile(r'(\d\d\d(\s|-)\d\d\d(\s|-)\d\d\d)')
        return res

    def regexComment():
        '''Comment'''
        res = re.compile(r'[^<td>]([a-zA-Z0-9_])[</td>]$')
        return res
