import os, fnmatch, glob, importlib


class Detailed:
    mode = 'detailed'
    """Main entrypoint class for the static code analysis"""
    _validators = []

    def execute(self):
        self.__import_validators()
        write_report = raw_input('Create report file? (Yes => 1 / No => 0):')
        try:
            results = self.validate()
        except KeyboardInterrupt:
            print '\nProcess interrupted from the keyboard'
            return

<<<<<<< HEAD
=======
        
        result_strings = {''} 
>>>>>>> Update data transfer object
        if write_report == '1':
            return  # ReportFile().execute(results)

        return  # Console().execute(results)

    def validate(self):
        results = self.__import_dto()
        for validator in self._validators:
            validator.init()
            if hasattr(validator, 'folder') and validator.folder:
                files = self._get_files_for_validator(validator.folder, validator.EXTENSIONS)
                for filePath in files:
                    validated_result = validator.execute(filePath, self.mode)
                    if validated_result is None:
                        continue
                    if len(validated_result) is not 0:
                        results.append([filePath, validated_result])
            if hasattr(validator, 'url') and len(validator.url) is not 0 \
                    and hasattr(validator, 'folders') and len(validator.folders) is not 0:
                results += (validator.execute(self.mode))

        return results

    def __import_validators(self):
        """Returns list of the avaliable validators"""
        os.chdir('Validators')
        validator_type = self.mode.capitalize()
        validator_name = validator_type.capitalize()  # TODO check if os.path.join can work with multiple dirs
        os.chdir(validator_name)
        module_list = os.listdir('./')
        for moduleItem in module_list:
            if moduleItem.find("init") is not -1:
                continue
            module = importlib.import_module(moduleItem[0:-3])
            class_name = getattr(module, moduleItem[0:-3])

            self._validators.append(class_name())
        os.chdir('../../')

    def __import_dto(self):
        os.chdir('Dto')
        dto_type = self.mode.capitalize()
        module = importlib.import_module(dto_type)
        class_name = getattr(module, dto_type)

        return class_name()

    def _get_files_for_validator(self, folder_name, file_extensions):
        pass
