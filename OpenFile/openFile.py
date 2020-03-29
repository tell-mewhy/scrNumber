#! /usr/bin/python3

import csv
# import logging

class file:

    def createFile(name):

        f = csv.writer(open(str(name)+'.csv', 'a')) # w

        return f
