import getopt
import sys
from works.GoogleFinanceScrapper import GoogleFinanceScrapper
from works.TopsyScrapper import TopsyScrapper

__author__ = 'Tuly'


class Main:
    def __init__(self):
        pass

    def runSpider(self, argv):
        try:
            opts, args = getopt.getopt(argv, 'hs:f:', ['help', 'spider=', 'file='])
        except Exception, x:
            print x
            self.usage()
            sys.exit(2)
        arg1 = None
        arg2 = None
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.usage()
                sys.exit()
            elif opt in ('-s', '--spider'):
                arg1 = arg
            elif opt in ('-f', '--file'):
                arg2 = arg
        self.startScrapper(arg1, arg2)

    def startScrapper(self, arg1, arg2):
        if arg1 == 'topsy':
            self.scrapTopsy(arg2)
        elif arg1 == 'google':
            self.scrapGoogleFinance(arg2)
        else:
            print 'Unknown spider type.'
            self.usage()

    def usage(self):
        print 'Usage: '
        print '\nTo run spider write: python -s spidername -f filepath or python --spider spidername --file filepath'

    def scrapTopsy(self, filename):
        print 'Running spider for Topsy...'
        scrapper = TopsyScrapper(filename)
        scrapper.scrapData()

    def scrapGoogleFinance(self, filename):
        print 'Running spider for Google Finance...'
        scrapper = GoogleFinanceScrapper(filename)
        scrapper.scrapData()


if __name__ == "__main__":
    main = Main()
    main.runSpider(sys.argv[1:])

