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
        """Method retrieves file contents by give filePath"""
        with open(filePath, 'r') as theFile:
            data = theFile.read()
            return data

    def execute(self, filePath, mode=''):
        """Main validator's logic entrypoint."""
        fileContent = self.getFileContent(filePath)

        soup = BeautifulSoup(fileContent, 'html.parser')
        linesLen = len(open(filePath).readlines())
        if mode != 'reverse':
            searchResults = soup.find_all(
                lambda tag: len(tag.text) is not 0
                            and tag.find(text=True, recursive=False) is not NavigableString
                            and tag.find(text=True, recursive=False) is not '\n'
                            and tag.find(text=True, recursive=False) is not None
                            and 'translate' not in tag.attrs
                            and tag.translate is not ""

            )

        if mode == 'reverse':
            searchResults = soup.find_all(
                lambda tag: len(tag.text) is not 0
                            and tag.find(text=True, recursive=False) is not NavigableString
                            and tag.find(text=True, recursive=False) is not '\n'
                            and tag.find(text=True, recursive=False) is not None
                            and 'translate' in tag.attrs
                            and tag.text.find('translate') is not -1

            )

        filteredResults = self.filterHtmlElements(searchResults, mode)

        if mode != 'flex' and (filteredResults is None or len(filteredResults) is 0):
            return [linesLen, 0]

        if mode == 'flex' and (filteredResults is None or len(filteredResults) is 0):
            return

        if mode == 'count' or mode == 'reverse':
            return [
                linesLen,
                len(searchResults)

            ]

        return self.numerateResults(filePath, filteredResults)

    def filterHtmlElements(self, htmlElements, mode):
        pass

    def checkParentObject(self, element):
        pass

    def numerateResults(self, filePath, searchResults):
        pass

    def getFolder(self):
        pass
