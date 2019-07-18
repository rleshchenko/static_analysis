import os, fnmatch, importlib, glob
from Dto.ResultObject import StatsResultObject
from typing import List


class Stats:
    mode = 'stats'
    """Main entrypoint class for the static code analysis"""
    _validators = []
    _renderers = {}

    def execute(self):
        self.__import_validators()
        self.__import_renderers()
        write_report = input('Create report file? (Yes => 1 / No => 0):')
        try:
            results = self.validate()
        except KeyboardInterrupt:
            print('\nProcess interrupted from the keyboard')
            return

        if write_report == '1':
            return self._renderers['ReportFile'].execute(results, self.mode)

        return self._renderers['Console'].execute(results, self.mode)

    def validate(self) -> StatsResultObject:
        result = StatsResultObject()
        for validator in self._validators:
            validator.init()
            if hasattr(validator, 'folder') and validator.folder is not '':
                files = self.__get_files_for_validator(validator.folder, validator.EXTENSIONS)
                for filePath in files:
                    validatorResult = validator.execute(filePath)
                    result = self.merge_total_result(result, validatorResult)
            if hasattr(validator, 'url') and len(validator.url) is not 0 \
                    and hasattr(validator, 'folders') and len(validator.folders) is not 0:
                validatorResult = validator.execute(self.mode)
                result = self.merge_total_result(result, validatorResult)

        return result

    def merge_total_result(self, result, validator_result):
        result.set_total_count(result.get_total_count() + validator_result.get_total_count())
        result.set_translated_count(result.get_translated_count() + validator_result.get_translated_count())
        result.set_untranslated_count(result.get_untranslated_count() + validator_result.get_untranslated_count())
        return result

    def __import_validators(self):
        os.chdir('Validators')
        validator_type = self.mode.capitalize()
        validator_name = validator_type.capitalize()  # TODO check if os.path.join can work with multiple dirs
        os.chdir(validator_name)
        module_list = [f for f in glob.glob("*.py")]
        for moduleItem in module_list:
            if moduleItem.find("init") is not -1:
                continue
            module = importlib.import_module(moduleItem[0:-3])
            class_name = getattr(module, moduleItem[0:-3])

            self._validators.append(class_name())
        os.chdir('../../')

    def _get_files_for_validator(self, folder_name: str, file_extensions) -> List:
        files = []

        if isinstance(file_extensions, str):
            file_extensions = [file_extensions]

        for fileExtension in file_extensions:
            for root, dirnames, filenames in os.walk(folder_name):
                if any(prohibitedFolderName in root for prohibitedFolderName in [
                    'dist',
                    'node_modules',
                    'tests',
                    'git',
                    'bower_components'
                ]):
                    continue
                for filename in fnmatch.filter(filenames, '*.' + fileExtension):
                    if any(prohibited in filename for prohibited in [
                        'eslint',
                        'jest',
                        'gulpfile',
                        'min',
                        'module',
                        '.directive.'
                        'mock',
                        'config'
                    ]):
                        continue

                    files.append(os.path.join(root, filename))

        return files

    def __import_renderers(self):
        os.chdir('Output')
        module_list = [f for f in glob.glob("*.py")]
        for moduleItem in module_list:
            if moduleItem.find("init") is not -1:
                continue
            module = importlib.import_module(moduleItem[0:-3])
            renderer = getattr(module, moduleItem[0:-3])
            self._renderers[moduleItem[0:-3]] = renderer()
        os.chdir('../')

    def __get_files_for_validator(self, folder_name, file_extensions):
        """Returns file list depends on given extension """
        files = []

        if isinstance(file_extensions, str):
            file_extensions = [file_extensions]

        for fileExtension in file_extensions:
            for root, dirnames, filenames in os.walk(folder_name):
                if any(prohibitedFolderName in root for prohibitedFolderName in [
                    'dist',
                    'node_modules',
                    'tests',
                    'git',
                    'bower_components'
                ]):
                    continue
                for filename in fnmatch.filter(filenames, '*.' + fileExtension):
                    if any(prohibited in filename for prohibited in [
                        'eslint',
                        'jest',
                        'gulpfile',
                        'min',
                        'module',
                        '.directive.'
                        'mock',
                        'config'
                    ]):
                        continue

                    files.append(os.path.join(root, filename))

        return files
