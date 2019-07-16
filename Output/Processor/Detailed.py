class Detailed:

    def execute(self, results):
        preparedResult = []
        for processed_file in results:
            preparedResult.append(processed_file.get_file_path() + ': \n')
            for translate_entry in processed_file.get_translate_entries():
                line = '\t' + str(translate_entry.get_line_number()) + '\t' + translate_entry.get_untranslated_line().encode('unicode-escape') + '\n'
                preparedResult.append(line)
            preparedResult.append('\n')
        return preparedResult

