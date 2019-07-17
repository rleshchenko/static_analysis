from interface import implements
from Interfaces.DetailedResultEntryObjectInterface import DetailedResultEntryObjectInterface
from Interfaces.DetailedResultObjectInterface import DetailedResultObjectInterface
from Interfaces.StatsResultObjectInterface import StatsResultObjectInterface
from typing import List


class DetailedResultObject(implements(DetailedResultObjectInterface)):

    def __init__(self):
        self.untranslated_entires = []
        self.file_path = ''

    def get_translate_entries(self) -> List:
        return self.untranslated_entires

    def set_file_path(self, file_path: str) -> DetailedResultObjectInterface:
        self.file_path = file_path
        return self

    def get_file_path(self):
        return self.file_path

    def add_translate_entry(self, strings_array: List):
        for line_number, untranslated_line in strings_array:
            entry = DetailedResultEntryObject()
            entry.set_line_number(line_number)
            entry.set_untranslated_line(untranslated_line)
            self.untranslated_entires.append(entry)

    def add_single_translate_entry(self, entry: DetailedResultEntryObjectInterface = None):
        self.untranslated_entires.append(entry)
        return self


class DetailedResultEntryObject(implements(DetailedResultEntryObjectInterface)):

    def __init__(self):
        self.line_number = 0
        self.untranslated_line = ''

    def set_line_number(self, num: int) -> DetailedResultEntryObjectInterface:
        self.line_number = num
        return self

    def set_untranslated_line(self, line: str) -> DetailedResultEntryObjectInterface:
        self.untranslated_line = line
        return self

    def get_line_number(self) -> int:
        return self.line_number

    def get_untranslated_line(self) -> str:
        return self.untranslated_line


class StatsResultObject(implements(StatsResultObjectInterface)):
    # total lines count in processed files
    total_count = 0
    # translated lines count in processed files
    translated_count = 0
    # untranslated lines count in processed fiels 
    untranslated_count = 0

    def set_total_count(self, num: int) -> StatsResultObjectInterface:
        self.total_count = num
        return self

    def set_translated_count(self, num: int) -> StatsResultObjectInterface:
        self.translated_count = num
        return self

    def set_untranslated_count(self, num: int) -> StatsResultObjectInterface:
        self.untranslated_count = num
        return self

    def get_total_count(self) -> int:
        return self.total_count

    def get_translated_count(self) -> int:
        return self.translated_count

    def get_untranslated_count(self) -> int:
        return self.untranslated_count
