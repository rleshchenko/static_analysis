from Flex import Flex


class Full(Flex):
    mode = 'count'

    def validate(self):
        whole_string_count = 0
        untranslated_string_count = 0

        for validator in self._validators:
            validator.init()
            validated_result  = ''
            if hasattr(validator, 'folder') and validator.folder:
                files = self._get_files_for_validator(validator.folder, validator.EXTENSIONS)
                for filePath in files:
                    validated_result = validator.execute(filePath, self.mode)
                    if validated_result is None:
                        continue
                    if len(validated_result) is not 0:
                        whole_string_count+=validated_result[0]
                        untranslated_string_count+=validated_result[1]
            if hasattr(validator, 'url') and len(validator.url) is not 0 \
                    and hasattr(validator, 'folders') and len(validator.folders) is not 0:
                validated_result = (validator.execute('count'))
                whole_string_count += validated_result[0]
                untranslated_string_count += validated_result[1]

        return [
            whole_string_count,
            untranslated_string_count
        ]

    def print_results(self, results):
        """Renders result in the console"""
        print ('Total strings count: ' + str(results[0]) + ' \n')
        print ('Untranslated strings count: ' + str(results[1]) + ' \n')

    def write_results(self, results):
        """Renders result to the file"""
        file = open('report.txt', 'w')
        file.write('Total strings count: ' + str(results[0]) + ' \n')

        file.write('Untranslated strings count: ' + str(results[1]) + ' \n')
        file.close()
