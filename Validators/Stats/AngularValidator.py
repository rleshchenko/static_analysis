from bs4 import BeautifulSoup, NavigableString
from Dto.ResultObject import StatsResultObject


class AngularValidator:
    """Validator for the angular 1.5 html templates."""

    EXTENSIONS = 'html'
    folder = ''

    def init(self):
        self.folder = input('Please insert angular templates folder:')

    def getFileContent(self, filePath):
        """Method retrieves file contents by give filePath"""
        with open(filePath, 'r') as theFile:
            data = theFile.read()
            return data

    def execute(self, filePath):
        result = StatsResultObject()
        """Main validator's logic entrypoint."""
        fileContent = self.getFileContent(filePath)

        soup = BeautifulSoup(fileContent, 'html.parser')
        linesLen = len(open(filePath).readlines())

        translated_elements = soup.find_all(
            lambda tag: len(tag.text) is not 0
                        and tag.find(text=True, recursive=False) is not NavigableString
                        and tag.find(text=True, recursive=False) is not '\n'
                        and tag.find(text=True, recursive=False) is not None
                        and ('translate' in tag.attrs
                             or tag.text.find('translate') is not -1)
        )

        untranslated_elements = soup.find_all(
            lambda tag: len(tag.text) is not 0
                        and tag.find(text=True, recursive=False) is not NavigableString
                        and tag.find(text=True, recursive=False) is not '\n'
                        and tag.find(text=True, recursive=False) is not None
                        and 'translate' not in tag.attrs
                        and tag.translate is not ""

        )

        translated_elements = self.filterTranslatedHtmlElements(translated_elements)
        untranslated_elements = self.filterUntranslatedHtmlElements(untranslated_elements)

        result.set_total_count(linesLen)
        result.set_translated_count(len(translated_elements))
        result.set_untranslated_count(len(untranslated_elements))

        return result

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

    def filterUntranslatedHtmlElements(self, htmlElements):
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

    def filterTranslatedHtmlElements(self, htmlElements):
        filteredResults = []
        for element in htmlElements:
            if element.text.find('{{', 0, -1) != -1 and element.text.find('translate') != -1:
                filteredResults.append(element)
                continue
            else:
                if len(element.find(text=True, recursive=False).strip()) is 0:
                    continue

                if self.checkParentObject(element):
                    continue

        return filteredResults
