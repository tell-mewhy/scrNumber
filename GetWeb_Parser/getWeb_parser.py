#! /usr/bin/python3

import requests, csv, sys, re, os
from bs4 import BeautifulSoup as bs
from datetime import datetime
from datetime import date
from time import sleep
from pprint import pprint
from OpenFile import openFile

from RegexPage import regexPage as rp

import logging

logging.basicConfig(filename='../scrNumber/Log/myProgramLog.txt',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)
# logging.disable(logging.CRITICAL)


class Getweb_parser:
    '''
    First: getPage
    Second: findData
    Third: writeData
    Fourth: checkFile

                    (.) (.)
           \,,/        &       \,,/
            \\       \___/     //

    '''

    def __init__(self,link,part=0,counter=1):
        '''start'''

        self.link = (link)
        self.find = '' #find # 'table opinion table-striped'
        self.findall = '' #findall # td
        self.date = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.type = 'Dangerous'
        self.fileName = 'DangerousNumbers'
        self.part = part
        self.counter = counter

        logging.warn(self.__dict__)

        Getweb_parser.findData(self)

    def getPage(self):

        try:
            if self.part == 0:
                page = requests.get(self.link)
                page.raise_for_status()
                soup = bs(page.text, 'html.parser')
            else:
                page = requests.get(self.link + '/' + str(self.part))
                page.raise_for_status()
                soup = bs(page.text, 'html.parser')
                print(page)
        except:
            if self.counter == 3 and self.part != 0:
                logging.warn('Cant open site: '+self.link+'/'+str(self.part))
                print("Can't open link: {0}".format(self.link+'/'+str(self.part)))
                exit()
            if self.counter == 3 and self.part == 0:
                logging.warn('Cant open site: '+self.link+'/'+str(self.part))
                print("Can't open link: {0}".format(self.link))
                exit()

            sleep(5)

            self.counter += 1
            return Getweb_parser(self.link,self.part,self.counter)

        return soup

    def findData(self):

        table_rows = Getweb_parser.getPage(self).find_all('tr')
        rov = []

        for tr in table_rows:
            td = tr.find_all('td')
            a = tr.find_all('a')
            for href in a:
                row = [i.text for i in td]
                num = rp.RegexPage.regexNumber().search(str(row))
                if num:
                    number = num.group().rstrip()
                    comm = row[1]
                    link = href.get('href')
                    if number in rov:
                        continue
                    rov.append([number,comm,link,self.date,self.type])

        if self.part == 0:
            print('\nSave {0} numbers to rov from site: {1}'.format(len(rov),self.link))
        if self.part != 0:
            print('\nSave {0} numbers to rov from site: {1}'.format(len(rov),self.link+'/'+ str(self.part)))

        # self.part is necessary to one page
        self.part += 100

        # Write rows
        Getweb_parser.writeData(self,rov)

        # Don't load more records if you don't need! Uncomment this!
        # if self.part == 100:
        #     print('END')
        #     return rov

        if len(rov) <= 6:
            return rov
        if len(rov) > 6:
            return Getweb_parser(self.link,self.part)

    def writeData(self,row):

        # Check if rows was earlier load
        data = CheckFile.check(row)
        if len(data) == 0:
            pass
        else:
            f = openFile.file.createFile(self.fileName)
            f.writerow(['Telefon','Komentarz','Link','Data pobrania',self.type])
            counter = 0
            for r in data:
                counter += 1
                f.writerow([r[0],r[1],r[2],r[3],r[4]])
            # f.writerow(['WCZYTANO {0} REKORDÓW ZE STRONY: {1}'.format(counter,self.link)])

class CheckFile:
    '''Must check old file if new data was imported earlier.'''

    def check(data):

        try:
            file = open('DangerousNumbers.csv', mode='r')
        except:
            return data

        temp = []
        for f in file:
            t = rp.RegexPage.regexNumber().search(str(f))
            if t:
                temp.append(t.group())

        toWrite = []
        for r in data:
            if temp:
                if r[0] in temp:
                    pass
                else:
                    toWrite.append([r[0],r[1],r[2],r[3],r[4]])
            else:
                toWrite.append([r[0],r[1],r[2],r[3],r[4]])

        file.close()

        print('To load: {0}'.format(str(len(toWrite))))

        return toWrite

# UWAGI OGÓLNE:
# improve the program, it will be more universal, to other sites
# set the program to run every e.g. 5 minutes
