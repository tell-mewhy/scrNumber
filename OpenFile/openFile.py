#! /usr/bin/python3

import csv
# from GetWeb_Parser import getWeb_parser
# import logging

class file:

    def createFile(name):
        
        f = csv.writer(open(str(name)+'.csv', 'a')) # w

        return f
