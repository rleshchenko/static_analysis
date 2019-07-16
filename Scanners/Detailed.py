import os, fnmatch, importlib, glob
import sys
from Dto.ResultObject import DetailedResultObject

class Detailed:
    mode = 'detailed'
    """Main entrypoint class for the static code analysis"""
    _validators = []
    _renderers = {}

    def execute(self):
        self.__import_validators()
        self.__import_renderers()
        write_report = raw_input('Create report file? (Yes => 1 / No => 0):')
        try:
            results = self.validate()
        except KeyboardInterrupt:
            print '\nProcess interrupted from the keyboard'
            return
        
        if write_report == '1':
            return self._renderers['ReportFile'].execute(results, self.mode)

        return self._renderers['Console'].execute(results, self.mode)

    def validate(self):
        results = []
        for validator in self._validators:
            validator.init()
            if hasattr(validator, 'folder') and validator.folder is not '':
                files = self.__get_files_for_validator(validator.folder, validator.EXTENSIONS)
                for filePath in files:
                    result = DetailedResultObject()
                    result = validator.execute(filePath, self.mode, result)
                    if len(result.untranslated_entires) is not 0:
                        result.set_file_path(filePath)
                        results.append(result)
                        del result
            if hasattr(validator, 'url') and len(validator.url) is not 0 \
                    and hasattr(validator, 'folders') and len(validator.folders) is not 0:
                results += validator.execute(self.mode)

        return results

    def __import_validators(self):
        """Returns list of the avaliable validators"""
        os.chdir('Validators')
        validator_type = self.mode.capitalize()
        validator_name = validator_type.capitalize()  # TODO check if os.path.join can work with multiple dirs
        os.chdir(validator_name)
        module_list = [f for f in glob.glob( "*.py")]
        for moduleItem in module_list:
            if moduleItem.find("init") is not -1:
                continue
            module = importlib.import_module(moduleItem[0:-3])
            class_name = getattr(module, moduleItem[0:-3])

            self._validators.append(class_name())
        os.chdir('../../')

    def __get_dto(self):
        os.chdir('Dto')
        dto_type = self.mode.capitalize()
        module = importlib.import_module('ResultObject')
        class_name = getattr(module, dto_type + 'ResultObject')
        os.chdir('../')

        return class_name

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

    def __import_renderers(self):
        os.chdir('Output')
        module_list = [f for f in glob.glob( "*.py")]
        for moduleItem in module_list:
            if moduleItem.find("init") is not -1:
                continue
            module = importlib.import_module(moduleItem[0:-3])
            renderer = getattr(module, moduleItem[0:-3])
            self._renderers[moduleItem[0:-3]] = renderer()
        os.chdir('../')
