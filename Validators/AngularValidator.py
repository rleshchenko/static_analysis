from bs4 import BeautifulSoup, NavigableString


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

    def execute(self, filePath):
        """Main validator's logic entrypoint."""
        fileContent = self.getFileContent(filePath)

        soup = BeautifulSoup(fileContent, 'html.parser')
        searchResults = soup.find_all(
            lambda tag: len(tag.text) is not 0
                        and tag.find(text=True, recursive=False) is not NavigableString
                        and tag.find(text=True, recursive=False) is not '\n'
                        and tag.find(text=True, recursive=False) is not None
                        and 'translate' not in tag.attrs
                        and tag.translate is not ""
        )

        filteredResults = self.filterHtmlElements(searchResults)
        numeredResults = self.numerateResults(filePath, filteredResults)

        return numeredResults

    def filterHtmlElements(self, htmlElements):
        filteredResults = []
        for element in htmlElements:
            if element.text.find('{{', 0, -1) != -1 and element.text.find('translate') != -1 \
                    or element.text.find('{{ ::', 0, -1) != -1:
                continue
            else:
                if element.find(text=True, recursive=False).strip() == '':
                    continue

                if self.checkParentObject(element):
                    filteredResults.append(element)
                    continue

        return filteredResults

    def checkParentObject(self, element):
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
