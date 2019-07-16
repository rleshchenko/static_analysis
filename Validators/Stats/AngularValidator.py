from bs4 import BeautifulSoup, NavigableString
import HTMLParser
import re


class AngularValidator:
    """Validator for the angular 1.5 html templates."""

    EXTENSIONS = 'html'
    folder = ''

    def init(self):
        self.folder = raw_input('Please insert angular templates folder:')

    def getFileContent(self, filePath):
        pass

    def execute(self, filePath, mode=''):
        pass

    def filterHtmlElements(self, htmlElements, mode):
        pass

    def checkParentObject(self, element):
        pass

    def numerateResults(self, filePath, searchResults):
        pass

    def getFolder(self):
        pass
