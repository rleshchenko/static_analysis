class Detailed:

    def execute(self, results):
        preparedResult = []
        html_elements_count = 0
        for processed_file in results:
            preparedResult.append(processed_file.get_file_path() + ': \n')
            untrunslated_entries = processed_file.get_translate_entries()
            for translate_entry in untrunslated_entries:
                try:
                    line = '\t' + str(
                        translate_entry.get_line_number()) + '\t' + translate_entry.get_untranslated_line() + '\n'
                    preparedResult.append(line)
                    html_elements_count += 1
                except UnicodeDecodeError:
                    continue
            preparedResult.append('\n')
        preparedResult.append('\nTotal elements count: ' + str(html_elements_count))
        return preparedResult
