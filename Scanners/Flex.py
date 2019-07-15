import os, fnmatch, glob, importlib

class Flex:
    mode = 'flex'
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

        if write_report == '1':
            return self.write_results(results)

        return self.print_results(results)

    def validate(self):
        results = []

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
        module_list = glob.glob(os.path.dirname('./Validators') + "/*.py")

        for moduleItem in module_list:
            if moduleItem.find("init") is not -1:
                continue
            module = importlib.import_module('Validators.' + moduleItem[2:-3])
            class_name = getattr(module, moduleItem[2:-3])

            self._validators.append(class_name())
        os.chdir('../')

    def _get_files_for_validator(self, folder_name, file_extensions):
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

    def print_results(self, results):
        """Renders result in the console"""
        print ("Following tags don't have proper translation: \n")
        html_elements_count = 0
        for result in results:
            print (result[0] + ': \n')
            for num, line in result[1]:
                print ('\t' + str(num) + '\t' + line)
                html_elements_count += 1
        print ('\n')

        print "Total count: " + str(html_elements_count)

    def write_results(self, results):
        """Renders result to the file"""
        file = open('report.txt', 'w')
        file.write('Following tags don\'t have proper translation: \n')
        html_elements_count = 0
        for result in results:
            file.write(result[0] + ': \n')
            if type(result[1][1]) is int:
                continue
            for num, line in result[1]:
                try:
                    file.write('\t' + str(num) + '\t' + line.encode('unicode-escape') + '\n')
                except UnicodeDecodeError:
                    continue
                except IndexError:
                    continue
                html_elements_count  += 1

            file.write('\n')

        file.write("Total count: " + str(html_elements_count))
        file.close()
