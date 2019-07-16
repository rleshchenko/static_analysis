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
                validated_result = (validator.execute(self.mode))
                whole_string_count += validated_result[0]
                untranslated_string_count += validated_result[1]

        return [
            whole_string_count,
            untranslated_string_count
        ]
