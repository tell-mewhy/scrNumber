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

        self.link = link
        # self.find = '' #find # 'table opinion table-striped'
        # self.findall = '' #findall # td
        self.date = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.type = 'test'
        self.fileName = 'PhoneNumbers'
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
        except:
            if self.counter == 3 and self.part != 0:
                logging.warn('Cant open site: '+self.link+'/'+str(self.part))
                print("Can't open link: {0}".format(self.link+'/'+str(self.part)))
                exit()
            if self.counter == 3 and self.part == 0:
                logging.warn('Cant open site: '+self.link+'/'+str(self.part))
                print("Can't open link: {0}".format(self.link))
                exit()

            # Wait 5 second and reload page
            sleep(5)

            self.counter += 1
            return Getweb_parser(self.link,self.part,self.counter)

        return soup

    def findData(self):

        # First checking page
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

        # When program don't found data on page then he check p tag and write to file
        if len(rov) == 0:
            rows = Getweb_parser.getPage(self).find_all('p')
            data = []
            for i in rows:
                number = rp.RegexPage.regexNumber().search(str(i.get_text()))
                if number and (number[0][0:4] != (' 000' or '000')):
                    data.append(number.group())

            # Open and write data to file
            if len(data) != 0:
                file = open('PhonesFromWeb.txt', 'a')
                file.write(self.link + '\n')
                for i in data:
                    file.write(i + '\n')
                file.close()
                print('The PhonesFromWeb.txt file is updated in the current program folder.\n')

            # While loop to check other sites if you need
            while True:
                check = input('\nDo you check other page? [write Y or N and press enter]\n')
                if isinstance(check, str) == True and check.lower() == 'y':
                    link = input('Paste link and press enter:\n')
                    if isinstance(link, str) == True:
                        return Getweb_parser(link,self.part)
                    else:
                        print('Wrong link!')
                if isinstance(check, str) == True and check.lower() == 'n':
                    print('Thx, bye :)')
                    exit()
                else:
                    print('Wrong data!')

        if self.part == 0:
            print('\nLoad {0} numbers to rov from site: {1}\n'.format(len(rov),self.link))
        if self.part != 0:
            print('\nLoad {0} numbers to rov from site: {1}\n'.format(len(rov),self.link+'/'+ str(self.part)))

        # Write rows
        Getweb_parser.writeData(self,rov)

        # self.part is necessary to one page
        self.part += 100

        # Don't load more records if you don't need! Uncomment this!
        if self.part == 100:
            print('END')
            return rov

        # if len(rov) <= 6:
        #     return rov
        if len(rov) > 6:
            return Getweb_parser(self.link,self.part)

    def writeData(self,row):

        # Check if rows was earlier load
        data = CheckFile.check(row)
        if len(data) == 0:
            pass
        else:
            f = openFile.file.createFile(self.fileName)
            f.writerow(['Phone','Comment','Link','Date',self.type])
            counter = 0
            for r in data:
                counter += 1
                f.writerow([r[0],r[1],r[2],r[3],r[4]])

class CheckFile:
    '''Must check old file if new data was imported earlier.'''

    def check(data):

        try:
            file = open('PhoneNumbers.csv', mode='r')
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

        if len(toWrite) == 0:
            print('You already have all the numbers from this page.')
        elif len(data) != len(toWrite):
            print('{0} records are already in the file'.format(str(int(len(data) - len(toWrite)))))
        if toWrite:
            print('To saving {0} record(s) to file'.format(str(len(toWrite))))

        return toWrite

# UWAGI OGÓLNE:
# set the program to run every e.g. 5 minutes
