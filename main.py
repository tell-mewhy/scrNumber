from GetWeb_Parser import getWeb_parser
from RegexPage import regexPage as rp
import sys

def main():

    link = input('Podaj adres strony: \n')
    first = getWeb_parser.Getweb_parser(link) #sys.argv[1],sys.argv[2],sys.argv[3])

if __name__ == "__main__":

    main()
es
