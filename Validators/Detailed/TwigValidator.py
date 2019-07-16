from bs4 import BeautifulSoup, NavigableString
import re, HTMLParser


class TwigValidator:
    """Validator for the angular 1.5 html templates."""

    EXTENSIONS = ['html', 'twig', 'tpl']
    folder = ''

    def init(self):
        self.folder = raw_input('Please insert twig templates folder:')

    def getFileContent(self, filePath):
        """Method retrieves file contents by give filePath"""
        with open(filePath, 'r') as theFile:
            data = theFile.read().decode('utf-8')
            return data

    def execute(self, filePath, mode, result):
        """Main validator's logic entrypoint."""
        fileContent = self.getFileContent(filePath)
        soup = BeautifulSoup(fileContent, 'html.parser')
        searchResults = soup.find_all(
            lambda tag: len(tag.text) is not 0
                        and tag.find(text=True, recursive=False) is not NavigableString
                        and tag.find(text=True, recursive=False) is not '\n'
                        and tag.find(text=True, recursive=False) is not None
                        and len(re.findall(r'(\s*translate)', tag.text)) is 0
                        and tag.text.find('translate') is -1
                        and tag.name not in ['style', 'script']
        )

        searchResults = self.__filter_html_elements(searchResults)

        if len(searchResults) is not 0:
            numeratedResults = self.numerateResults(filePath, searchResults)
            result.set_file_path(filePath)
            result.add_translate_entry(numeratedResults)

        return result

    def numerateResults(self, filePath, searchResults):
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
