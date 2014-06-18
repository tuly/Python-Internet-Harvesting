import datetime
import time
import urllib
from logs.LogManager import LogManager
from utils.Csv import Csv
from utils.Utils import Utils
from spiders.Spider import Spider
from utils.Regex import Regex
from bs4 import BeautifulSoup
from selenium import webdriver

__author__ = 'Tuly'


class TopsyScrapper:
    isFinished = False

    def __init__(self, filename):
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        self.filename = filename
        self.url = 'http://topsy.com/s?'
        self.csvWriter = Csv('topsy.csv')
        csvDataHeader = ['Keyword', 'Tweets in last 30 days', 'Topsy Sentiment Score', ' Date of scrape']
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
                if len(line) > 0:
                    params = urllib.urlencode({'q': line, 'window': 'm', 'type': 'tweet'})
                    url = self.url + params
                    self.scrapBrowserData(url, line)
        except Exception, x:
            print x

    def scrapBrowserData(self, url, keyword, retry=0):
        try:
            if self.isFinished: return
            driver = webdriver.Firefox()
            driver.get(url)
            assert driver.title
            data = driver.find_element_by_xpath("/html")
            soup = BeautifulSoup(data.get_attribute('outerHTML'))
            driver.close()
            data = soup.find('div', id='module-searchsummary')
            if data is not None:
                count = data.find('span', class_='total-number')
                if count is not None:
                    count = count.text
                    print 'Total tweets for keyword[' + keyword + ']: ' + count
                sentimental_score = data.find('span', class_='sentiment-score')
                if sentimental_score is not None:
                    sentimental_score = sentimental_score.text
                current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                csvData = [keyword, count, sentimental_score, current_date]
                print 'Writting data to csv file...'
                print csvData
                self.csvWriter.writeCsvRow(csvData)
        except Exception, x:
            self.logger.error(x)
            print x
            if retry < 5:
                time.sleep(5)
