from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, Qt, QDir
from PyQt4.QtGui import *
import sys
import time
from works.GoogleFinanceScrapper import GoogleFinanceScrapper
from works.TopsyScrapper import TopsyScrapper

__author__ = 'Tuly'


class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.createGui()
        self.googleFileName = None
        self.topsyFileName = None
        self.googleOutputDirectory = None
        self.topsyOutputDirectory = None
        self.googleFinance = None
        self.topsy = None

    def createGui(self):
        ## Google Finance
        self.labelGoogleFile = QLabel('<b>Google Finance Input File: </b>')
        self.btnGoogleBrowse = QPushButton('&Browse')
        self.btnGoogleBrowse.clicked.connect(self.googleInputFile)

        self.labelGoogleDir = QLabel('<b>Google Finance Output Directory: </b>')
        self.btnGoogleBrowseDir = QPushButton('&Browse')
        self.btnGoogleBrowseDir.clicked.connect(self.googleOutputdir)

        ## Topsy
        self.labelTopsyFile = QLabel('<b>Topsy Input File: </b>')
        self.btnTopsyBrowse = QPushButton('&Browse')
        self.btnTopsyBrowse.clicked.connect(self.topsyInputFile)

        self.labelTopsyDir = QLabel('<b>Topsy Output Directory: </b>')
        self.btnTopsyBrowseDir = QPushButton('&Browse')
        self.btnTopsyBrowseDir.clicked.connect(self.topsyOutputdir)

        layoutTop = QGridLayout()
        layoutTop.addWidget(self.labelGoogleFile, 0, 0, Qt.AlignLeft)
        layoutTop.addWidget(self.btnGoogleBrowse, 0, 1, Qt.AlignLeft)
        layoutTop.addWidget(self.labelGoogleDir, 0, 2, Qt.AlignRight)
        layoutTop.addWidget(self.btnGoogleBrowseDir, 0, 3, Qt.AlignLeft)

        layoutTop.addWidget(self.labelTopsyFile, 0, 4, Qt.AlignRight)
        layoutTop.addWidget(self.btnTopsyBrowse, 0, 5, Qt.AlignLeft)
        layoutTop.addWidget(self.labelTopsyDir, 0, 6, Qt.AlignRight)
        layoutTop.addWidget(self.btnTopsyBrowseDir, 0, 7, Qt.AlignLeft)

        self.btnScrapGoogle = QPushButton('&Scrap Google Data')
        self.btnScrapGoogle.clicked.connect(self.scrapGoogleAction)
        self.btnStopGoogle = QPushButton('&Stop Google Data')
        self.btnStopGoogle.clicked.connect(self.stopGoogleAction)
        self.btnScrapTopsy = QPushButton('&Scrap Topsy Data')
        self.btnScrapTopsy.clicked.connect(self.scrapTopsyAction)
        self.btnStopTopsy = QPushButton('&Stop Topsy Data')
        self.btnStopTopsy.clicked.connect(self.stopTopsyAction)

        layout = QHBoxLayout()
        layout.addWidget(self.btnScrapGoogle)
        layout.addWidget(self.btnStopGoogle)
        layout.addWidget(self.btnScrapTopsy)
        layout.addWidget(self.btnStopTopsy)

        self.browserGoogle = QTextBrowser()
        self.browserTopsy = QTextBrowser()
        layoutBrowser = QHBoxLayout()
        layoutBrowser.addWidget(self.browserGoogle)
        layoutBrowser.addWidget(self.browserTopsy)

        layoutMain = QVBoxLayout()
        layoutMain.addLayout(layoutTop)
        layoutMain.addLayout(layout)
        layoutMain.addLayout(layoutBrowser)
        widget = QWidget()
        widget.setLayout(layoutMain)

        self.setCentralWidget(widget)
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() - 300, screen.height() - 300)
        self.setWindowTitle('Scrapper')
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Question?',
                                           "Are you sure you want to quit application?", QtGui.QMessageBox.Yes |
                                                                                         QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            print 'closing..'
            self.stopGoogleAction()
            self.stopTopsyAction()
            if self.googleFinance is not None:
                self.googleFinance = None
            if self.topsy is not None:
                self.topsy = None
            event.accept()
        else:
            event.ignore()

    def scrapGoogleAction(self):
        try:
            if self.googleFileName is not None and self.googleOutputDirectory is not None:
                self.googleFinance = GoogleFinanceScrapper(self.googleFileName, self.googleOutputDirectory)
                self.googleFinance.notify.connect(self.notifyGoogleInfo)
                self.googleFinance.start()
            else:
                QtGui.QMessageBox.warning(self, 'Warning', 'Please select your input file and output directory!')
        except Exception, x:
            print x

    def stopGoogleAction(self):
        try:
            if self.googleFinance is not None:
                self.browserGoogle.append('<font color=blue><b>Please wait.. Let it finish.</b></font>')
                self.googleFinance.isFinished = True
        except Exception, x:
            print x

    def scrapTopsyAction(self):
        try:
            if self.topsyFileName is not None and self.topsyOutputDirectory is not None:
                print self.topsyOutputDirectory
                self.topsy = TopsyScrapper(self.topsyFileName, self.topsyOutputDirectory)
                self.topsy.notify.connect(self.notifyTopsyInfo)
                self.topsy.start()
            else:
                QtGui.QMessageBox.warning(self, 'Warning', 'Please select your input file and output directory!')
        except Exception, x:
            print x

    def stopTopsyAction(self):
        try:
            if self.topsy is not None:
                self.browserTopsy.append('<font color=red><b>Please wait.. Let it finish.</b></font>')
                self.topsy.isFinished = True
        except Exception, x:
            print x

    def googleInputFile(self):
        self.googleFileName = QtGui.QFileDialog.getOpenFileName(self, "Select Text File", QDir.homePath() + "/Desktop")

    def googleOutputdir(self):
        self.googleOutputDirectory = QtGui.QFileDialog.getExistingDirectory(self, "Select Google Finance Output directory",
                                                                       QDir.homePath() + "/Desktop")

    def topsyInputFile(self):
        self.topsyFileName = QtGui.QFileDialog.getOpenFileName(self, "Select Text File", QDir.homePath() + "/Desktop")

    def topsyOutputdir(self):
        self.topsyOutputDirectory = QtGui.QFileDialog.getExistingDirectory(self, "Select Topsy Output Directory",
                                                                           QDir.homePath() + "/Desktop")

    def notifyGoogleInfo(self, data):
        try:
            self.browserGoogle.document().setMaximumBlockCount(1000)
            self.browserGoogle.append(data)
        except Exception, x:
            print x.message

    def notifyTopsyInfo(self, data):
        try:
            self.browserTopsy.document().setMaximumBlockCount(1000)
            self.browserTopsy.append(data)
        except Exception, x:
            print x.message


class MainView:
    def __init__(self):
        pass

    def showMainView(self):
        app = QApplication(sys.argv)
        form = Form()
        form.show()
        sys.exit(app.exec_())
