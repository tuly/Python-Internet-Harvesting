import datetime
import time
import urllib
from logs.LogManager import LogManager
from utils.Csv import Csv
from utils.Utils import Utils
from spiders.Spider import Spider
from utils.Regex import Regex
from bs4 import BeautifulSoup

__author__ = 'Tuly'


class GoogleFinanceScrapper:
    isFinished = False

    def __init__(self, filename):
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        self.filename = filename
        self.url = 'https://www.google.com/finance?'
        self.main_url = 'https://www.google.com'
        self.csvWriter = Csv('google_finance.csv')
        csvDataHeader = ['Ticker Symbol', 'Quarter End', 'Revenue', 'Total Revenue', 'Date of Scrape']
        self.csvWriter.writeCsvRow(csvDataHeader)

    def run(self):
        self.scrapData()
        self.csvWriter.closeWriter()

    def scrapData(self):
        try:
            file = open(self.filename, 'rb')
            for line in file.readlines():
                if self.isFinished: return
                line = self.regex.replaceData('\r+', '', line)
                line = self.regex.reduceNewLine(line)
                line = self.regex.reduceBlankSpace(line)
                line = line.strip()
                params = urllib.urlencode({'q': line})
                url = self.url + params
                self.scrapBykeyword(url, line)
        except Exception, x:
            print x
            self.logger.error('Error: ' + x.message)

    def scrapBykeyword(self, url, keyword, retry=0):
        try:
            print 'Main URL: ', url
            data = self.spider.fetchData(url)
            if data and len(data) > 0:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                soup = BeautifulSoup(data)
                links = soup.find_all('li', class_='fjfe-nav-sub')
                for link in links:
                    if link is None or link.a is None: continue
                    if self.regex.isFoundPattern('(?i)\/finance\?q=.*?$', link.a.get('href')):
                        financial_url = link.a.get('href')
                        print self.main_url + financial_url
                        self.scrapRevenue(self.main_url + financial_url, keyword)
        except Exception, x:
            print x
            self.logger.error('Error: ' + x.message)
            if retry < 5:
                time.sleep(5)
                self.scrapBykeyword(url, keyword, retry + 1)

    def scrapRevenue(self, url, keyword):
        try:
            data = self.spider.fetchData(url)
            if data and len(data) > 0:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                data = self.regex.replaceData('<!--', '', data)
                data = self.regex.replaceData('-->', '', data)
                self.logger.debug(data)
                soup = BeautifulSoup(data)
                main_content = soup.find('table', id='fs-table')
                if main_content is not None:
                    cols = main_content.find_all('tr')[0].find_all('th')
                    lists = []
                    for i in range(1, len(cols)):
                        row1 = main_content.find_all('tr')[0].find_all('th')[i]
                        row2 = main_content.find_all('tr')[1].find_all('td')[i]
                        row3 = main_content.find_all('tr')[3].find_all('td')[i]
                        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        lists.append(
                            [keyword, self.regex.getSearchedData('(?i)(\d{4}-\d{2}-\d{2})', row1.text), row2.text,
                             row3.text, current_date])
                    for list in lists:
                        print 'writting data to csv file...'
                        print list
                        self.csvWriter.writeCsvRow(list)
        except Exception, x:
            print x
            self.logger.error('Error scrapping revenue: ' + x.message)



