from distutils.core import setup
from glob import glob
import py2exe

''' 'selenium', 'selenium.common', 'selenium.webdriver',
              'selenium.webdriver.common.html5', 'selenium.webdriver.remote', 'selenium.webdriver.common',
              'selenium.webdriver.firefox', 'selenium.webdriver.chrome', 'selenium.webdriver.ie',
              'selenium.webdriver.opera', 'selenium.webdriver.phantomjs', 'selenium.webdriver.safari','''

setup(
    windows=['Main.py'],
    options={"py2exe": {
        "includes": ["sip", "PyQt4.QtGui", "PyQt4.QtCore", "bs4.*", 'bs4.builder.*', 'codecs', 'cStringIO', 'sqlite3.*', 'htmllib.*'],
        'skip_archive': True,
        'optimize': 2, }},
    name='Scrapper',
    version='1.0',
    packages=['spiders', 'logs', 'utils', 'works', 'views'],
    data_files=[('selenium/webdriver/firefox/x86', ['selenium/webdriver/firefox/x86/x_ignore_nofocus.so']),
                ('selenium/webdriver/firefox/amd64', ['selenium/webdriver/firefox/amd64/x_ignore_nofocus.so']),
                ("selenium/webdriver/firefox",
                 ["selenium/webdriver/firefox/webdriver_prefs.json", "selenium/webdriver/firefox/webdriver.xpi"])],
    url='',
    license='',
    author='Rabbi',
    author_email='',
    description=''
)
