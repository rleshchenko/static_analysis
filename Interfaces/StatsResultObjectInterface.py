from interface import Interface


class StatsResultObjectInterface(Interface):
    def set_total_count(self, num: int):
        pass

    def set_translated_count(self, num: int):
        pass

    def set_untranslated_count(self, num: int):
        pass

    def get_total_count(self) -> int:
        pass

    def get_translated_count(self) -> int:
        pass

    def get_untranslated_count(self) -> int:
        pass
