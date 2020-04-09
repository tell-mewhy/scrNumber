from GetWeb_Parser import getWeb_parser
import sys

def main():

    link = input('Podaj adres strony: \n')

    try:
        first = getWeb_parser.Getweb_parser(link, int(sys.argv[1]))
    except:
        first = getWeb_parser.Getweb_parser(link)

if __name__ == "__main__":

    main()
