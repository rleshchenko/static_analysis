from bs4 import BeautifulSoup, NavigableString
import html.parser as HTMLParser
from typing import AnyStr as String, List


class AngularValidator:
    """Validator for the angular 1.5 html templates."""

    EXTENSIONS = 'html'
    folder = ''

    def init(self):
        self.folder = input('Please insert angular templates folder:')

    def getFileContent(self, filePath: String) -> String:
        """Method retrieves file contents by give filePath"""
        with open(filePath, 'r') as theFile:
            data = theFile.read()
            return data

    def execute(self, filePath: String, result):
        """Main validator's logic entrypoint."""
        fileContent = self.getFileContent(filePath)

        soup = BeautifulSoup(fileContent, 'html.parser')
        searchResults = soup.find_all(
            lambda tag: len(tag.text) is not 0
                        and tag.find(text=True, recursive=False) is not NavigableString
                        and tag.find(text=True, recursive=False) is not '\n'
                        and tag.find(text=True, recursive=False) is not None
                        and 'translate' not in tag.attrs
                        and (tag.translate is not ""
                             or tag.text.find('translate') is not -1)

        )

        filteredResults = self.filterHtmlElements(searchResults)

        if len(filteredResults) != 0:
            result.add_translate_entry(self.numerateResults(filePath, filteredResults))
        return result

    def filterHtmlElements(self, htmlElements: List) -> List:
        filteredResults = []
        for element in htmlElements:
            if element.text.find('{{', 0, -1) != -1 and element.text.find('translate') != -1:
                continue
            else:
                if len(element.find(text=True, recursive=False).strip()) is 0:
                    continue

                if self.checkParentObject(element):
                    filteredResults.append(element)
                    continue

        return filteredResults

    def checkParentObject(self, element) -> bool:
        parentElement = element.parent
        childCount = 0
        for child in list(parentElement.children):
            if isinstance(child, NavigableString):
                continue
            else:
                childCount += 1

        if 'translate' in parentElement.attrs and childCount > 1:
            return True

        if 'translate' not in parentElement.attrs:
            return True

        return False

    def numerateResults(self, filePath: String, searchResults: List) -> List:
        result = []
        fileLinesNumber = sum(1 for line in open(filePath, 'r'))
        for searchResult in searchResults:
            searchResult = HTMLParser.HTMLParser().unescape(str(searchResult))
            with open(filePath) as file:
                for num, line in enumerate(file, 1):
                    if searchResult.find('\n') is not -1 and searchResult[0:searchResult.find('\n')] in line:
                        result.append([num, searchResult])
                        break
                    if searchResult in line:
                        result.append([num, searchResult])
                        break
                    if num == fileLinesNumber:
                        result.append(['??', searchResult])

        return result

    def getFolder(self) -> String:
        return self.folder
