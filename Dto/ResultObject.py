class DetailedResultObject:

    def __init__(self):
        self.untranslated_entires = []
        self.file_path = ''

    def get_translate_entries(self):
        return self.untranslated_entires

    def set_file_path(self, file_path):
        self.file_path = file_path
        return self

    def get_file_path(self):
        return self.file_path

    def add_translate_entry(self, strings_array):
        for line_number, untranslated_line in strings_array:
            entry = DetailedResultEntryObject()
            entry.set_line_number(line_number)
            entry.set_untranslated_line(untranslated_line)
            self.untranslated_entires.append(entry)

    def add_single_translate_entry(self, entry = None):
        self.untranslated_entires.append(entry)
        return self


class DetailedResultEntryObject:

    def __init__(self):
        self.line_number = 0
        self.untranslated_line = ''

    def set_line_number(self, num):
        self.line_number = num
        return self

    def set_untranslated_line(self, line):
        self.untranslated_line = line
        return self

    def get_line_number(self):
        return self.line_number     

    def get_untranslated_line(self):
        return self.untranslated_line

class StatsResultObject:

    # total lines count in processed files
    total_count = 0 
    # translated lines count in processed files
    translated_count = 0 
    # untranslated lines count in processed fiels 
    untranslated_count = 0

    def set_total_count(self, num):
        self.total_count = num
        return self

    def set_translated_count(self, num):
        self.translated_count = num
        return self
    
    def set_untranslated_count(self, num):
        self.untranslated_count = num
        return self

    def get_total_count(self):
        return self.total_count

    def get_translated_count(self):
        return self.translated_count
    
    def get_untranslated_count(self):
        return self.untranslated_count    