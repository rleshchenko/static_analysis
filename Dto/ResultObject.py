
class DetailedResultObject:

    untanslated_files = []

    def get_translate_entries(self):
        return self.untanslated_files

    def add_translate_entry(self, entry):
        self.untanslated_files.append(entry)

class DetailedResultEntryObject:

    line_number = 0
    untranslated_line = ''

    def set_line_number(self, num):
        self.line_number = num
        return self

    def set_untranslated_line(self, line):
        self.untranslated_line = line
        return self

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
    
    def get_untranslated_count(self, num):
        return self.untranslated_count    