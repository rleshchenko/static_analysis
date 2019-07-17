from interface import Interface
from typing import List
from Interfaces.DetailedResultEntryObjectInterface import DetailedResultEntryObjectInterface


class DetailedResultObjectInterface(Interface):
    def get_translate_entries(self) -> List:
        pass

    def set_file_path(self, file_path: str):
        pass

    def get_file_path(self) -> str:
        pass

    def add_translate_entry(self, strings_array: List):
        pass

    def add_single_translate_entry(self, entry: DetailedResultEntryObjectInterface = None):
        pass
