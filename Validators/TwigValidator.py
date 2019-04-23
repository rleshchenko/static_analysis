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
            data = theFile.read()
            return data

    def execute(self, filePath):
        """Main validator's logic entrypoint."""
        fileContent = self.getFileContent(filePath)

        soup = BeautifulSoup(fileContent, 'html.parser')
        searchResults = soup.find_all(
            lambda tag: len(tag.text) is not 0
                        and len(re.findall('[\\n\\r]+', tag.text)) is 0
                        and len(re.findall(r'({%\s*translate)|({%\s*lang)|({{\s*lang.)|({%\s*jslang)', tag.text)) is 0)

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

    def getFolder(self):
        return self.folder