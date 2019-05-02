from bs4 import BeautifulSoup
import re


class TwigValidator:
    """Validator for the angular 1.5 html templates."""

    EXTENSIONS = ['html', 'twig']
    folder = ''

    def init(self):
        self.folder = raw_input('Please insert twig templates folder:')

    def getFileContent(self, filePath):
        """Method retrieves file contents by give filePath"""
        with open(filePath, 'r') as theFile:
            data = theFile.read().decode('utf-8')
            return data

    def execute(self, filePath, mode=''):
        """Main validator's logic entrypoint."""
        fileContent = self.getFileContent(filePath)

        soup = BeautifulSoup(fileContent, 'html.parser')
        searchResults = soup.find_all(
            lambda tag: len(tag.text) is not 0
                        and len(re.findall('[\\n\\r]+', tag.text)) is 0
                        and len(re.findall(r'({%\s*translate)|({%\s*lang)|({{\s*lang.)|({%\s*jslang)', tag.text)) is 0
                        and len(re.findall(r'(\s*translate)|(\s*lang)|(\s*lang.)|(\s*jslang)', tag.text)) is 0
                        and tag.text.find('translate') is -1
                        and tag.name not in ['style', 'script']
        )
        if len(searchResults) is 0:
            return

        searchResults = self.__filter_html_elements(searchResults)

        if mode == 'count':
            return [
                len(open(filePath).readlines()),
                sum([(lambda item: 1+str(item).count('\n'))(item) for item in searchResults])
            ]
        if len(searchResults) is not 0:
            return self.numerateResults(filePath, searchResults)

    def numerateResults(self, filePath, searchResults):
        result = []
        for searchResult in searchResults:
            searchResult = str(searchResult)

            with open(filePath) as file:
                for num, line in enumerate(file, 1):
                    if searchResult[0:searchResult.find('\n')] in line:
                        result.append([num, searchResult])

        return result

    def __filter_html_elements(self, html_elements):
        filtered_results = []
        for element in html_elements:
            if element.text.isdigit():
                continue
            if element.text.find('function(') is not -1 or element.text.find('<script') is not -1:
                continue
            filtered_results.append(element)

        return filtered_results

    def getFolder(self):
        return self.folder
