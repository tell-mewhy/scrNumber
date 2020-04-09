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

    def __init__(self, link, sign=0, part=0, counter=1):
        '''start'''

        self.link = link
        self.sign = sign
        self.date = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.counter = counter

        # My security sign to check specyfic page
        if sign == 1:
            self.type = 'test'
            self.fileName = 'PhoneNumbers'
            self.part = part

        logging.warn(self.__dict__)

        Getweb_parser.findData(self)

    def getPage(self):

        if self.sign == 1:
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
                return Getweb_parser(self.link,self.sign,self.part,self.counter)
        else:
            try:
                page = requests.get(self.link)
                page.raise_for_status()
                soup = bs(page.text, 'html.parser')
            except:
                # check the page three times
                if self.counter == 3:
                    logging.warn('Cant open site: ' + self.link)
                    print("Can't open link: {0}".format(self.link))
                    exit()

                sleep(5)
                self.counter += 1
                return Getweb_parser(self.link,self.sign,0,self.counter)

        self.counter = 0

        return soup

    def findData(self):

        table_rows = Getweb_parser.getPage(self)

        rov = []
        # Checking my specyfic page
        if self.sign == 1:
            specificPage = table_rows.find_all('tr')

            for tr in specificPage:
                td = tr.find_all('td')
                a = tr.find_all('a')
                for href in a:
                    row = [i.text for i in td]
                    num = rp.RegexPage.regexNumber().search(str(row))
                    if num:
                        number = num.group().rstrip()   # take number
                        comm = row[1]                   # take comment
                        link = href.get('href')         # take link
                        rov.append([number,comm,link,self.date,self.type])

            if self.part == 0:
                print('\nLoad {0} numbers to rov from site: {1}\n'.format(len(rov),self.link))
            if self.part != 0:
                print('\nLoad {0} numbers to rov from site: {1}\n'.format(len(rov),self.link+'/'+ str(self.part)))

            # Write rows if exists
            if rov:
                Getweb_parser.writeData(self,rov)

            # self.part is necessary to one page
            self.part += 100

            # Don't load more records if you don't need! Uncomment this!
            if self.part == 100:
                print('END')
                return rov

            # if len(rov) <= 6:
            #     return rov
            if len(rov) > 5:
                return Getweb_parser(self.link,self.part)

        # When program don't found data on page then he check p tag and write to file
        if len(rov) == 0:
            rows = table_rows.find_all('p')
            data = []
            for i in rows:
                number = rp.RegexPage.regexNumber().search(str(i.get_text()))
                if number and (number[0][0:4] != (' 000' or '000')):
                    data.append(number.group())

            # Open and write data to file
            if len(data) != 0:

                # file = open('PhonesFromWeb.txt', 'a')
                # file2 = open('PhonesFromWeb.txt','r')
                # listQ = [x[0:len(x)-1] for x in list(file2)]

                with open("PhonesFromWeb.txt", "r") as f:
                    lines = f.readlines()
                with open("PhonesFromWeb.txt", "a") as f:
                    f.write(self.link + '\n')
                    for i in data:
                        if i in [x.strip() for x in lines]:
                            print('{0} is already in the list'.format(i))
                        else:
                            f.write(i + '\n')

                # file.write(self.link + '\n')
                # for i in data:
                #     if self.link in listQ:
                #         print('----')
                #         print(self.link)
                #         print('----')
                #     if i in listQ:
                #         print('{0} is already in the list'.format(i))
                #         pass
                #     else:
                #         file.write(i + '\n')
                # file.close()
                # file2.close()

                # file.write(self.link + '\n')
                # for i in data:
                #     file.write(i + '\n')
                # file.close()
                print('The PhonesFromWeb.txt file is updated in the current program folder.\n')

            # While loop to check other sites if you need
            while True:
                check = input('\nDo you check other page? [write Y or N and press enter]\n')
                if isinstance(check, str) == True and check.lower() == 'y':
                    link = input('Paste link and press enter:\n')
                    if isinstance(link, str) == True:
                        return Getweb_parser(link)
                    else:
                        print('Wrong link!')
                if isinstance(check, str) == True and check.lower() == 'n':
                    print('Thx, bye :)')
                    exit()
                else:
                    print('Wrong data!')

    def writeData(self,row):

        # Check if rows was earlier load
        data = CheckFile.check(row)
        if len(data) == 0:
            pass
        else:
            f = openFile.file.createFile(self.fileName)
            f.writerow(['Phone','Comment','Link','Date',self.type])
            for r in data:
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
            print('Saving {0} record(s) to file'.format(str(len(toWrite))))

        return toWrite

# UWAGI OGÓLNE:
# 0. a może dodać jakiś security parametr jeżli będę chciał pobierać niebezpieczne numery? self.security na przykład = 1 i wtedy main.py link, 1
# 1. ogarnać ten burdel, dodać specjalną funkcje (o ile się da to przerobić) do pobierania danych ze strony o niebezpiecznych numerach, tą pierwszą z finddata, orarnąć też ten self.part i self.counter (counter jest do sprawdzenia ile razy nie udało się wczytać strony)
# 2. dopisać sprawdzanie danych w zwykłym pliku txt, czyli dodać jakieś znaczniki w funkcjach, dzięki którym będzie wiadomo czy sprawdzać csv czy txt

# set the program to run every e.g. 5 minutes
