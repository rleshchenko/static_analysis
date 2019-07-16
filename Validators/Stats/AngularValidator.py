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

    def execute(self, filePath, result):
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

        result.set_total_count(result.get_total_count() + linesLen)
        result.set_translated_count(result.get_translated_count() + len(translated_elements))
        result.set_untranslated_count(result.get_untranslated_count() + len(untranslated_elements))

        return result
