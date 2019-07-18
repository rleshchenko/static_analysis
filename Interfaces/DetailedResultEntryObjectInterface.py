from interface import Interface


class DetailedResultEntryObjectInterface(Interface):
    def set_line_number(self, num: int):
        pass

    def set_untranslated_line(self, line: str):
        pass

    def get_line_number(self) -> int:
        pass

    def get_untranslated_line(self) -> str:
        pass
