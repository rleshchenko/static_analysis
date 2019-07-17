from bs4 import BeautifulSoup, NavigableString
import re, html.parser as HTMLParser


class TwigValidator:
    """Validator for the angular 1.5 html templates."""

    EXTENSIONS = ['html', 'twig', 'tpl']
    folder = ''

    def init(self):
        self.folder = input('Please insert twig templates folder:')

    def getFileContent(self, filePath):
        """Method retrieves file contents by give filePath"""
        with open(filePath, 'r') as theFile:
            data = theFile.read()
            return data

    def execute(self, filePath, result):
        """Main validator's logic entrypoint."""
        fileContent = self.getFileContent(filePath)
        linesLen = len(open(filePath).readlines())
        soup = BeautifulSoup(fileContent, 'html.parser')
        untranslated_elements = soup.find_all(
                lambda tag: len(tag.text) is not 0
                            and tag.find(text=True, recursive=False) is not NavigableString
                            and tag.find(text=True, recursive=False) is not '\n'
                            and tag.find(text=True, recursive=False) is not None
                            and len(re.findall(r'(\s*translate)', tag.text)) is 0
                            and tag.text.find('translate') is -1
                            and tag.name not in ['style', 'script']
            )

        translated_elements = soup.find_all(
            lambda tag: len(tag.text) is not 0
                        and tag.find(text=True, recursive=False) is not NavigableString
                        and tag.find(text=True, recursive=False) is not '\n'
                        and tag.find(text=True, recursive=False) is not None
                        and len(re.findall(r'(\s*translate)', tag.text)) is not 0
                        and tag.text.find('translate') is not -1
                        and tag.name not in ['style', 'script']
        )


        untranslated_elements = self.__filter_html_elements(untranslated_elements)
        translated_elements = self.__filter_html_elements(translated_elements)

        result.set_total_count(result.get_total_count() + linesLen)
        result.set_translated_count(result.get_translated_count() + len(translated_elements))
        result.set_untranslated_count(result.get_untranslated_count() + len(untranslated_elements))

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
            if len(element.text.strip()) is 0:
                continue
            filtered_results.append(element.text.strip())

        return filtered_results

    def getFolder(self):
        return self.folder
