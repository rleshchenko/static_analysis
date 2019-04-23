import os, fnmatch, glob, importlib


class Initialize:
    """Main entrypoint class for the static code analysis"""
    _validators = []

    def __init__(self):
        """Initialize class constructor"""
        self.__import_validators()

    def execute(self):
        write_report = raw_input('Create report file? (Yes => 1 / No => 0):')
        try:
            results =  self.__validate()
        except KeyboardInterrupt:
            print '\nProcess interrupted from the keyboard'
            return
        except Exception, e:
            print e
            return

        if write_report == '1':
            return self.__writeResults(results)

        return self.__print_results(results)

    def __validate(self):
        results = []

        for validator in self._validators:
            validator.init()
            if hasattr(validator, 'folder') and validator.folder:
                files = self.__get_files_for_validator(validator.folder, validator.EXTENSIONS)
                for filePath in files:
                    validated_result = validator.execute(filePath)
                    if len(validated_result):
                        results.append([filePath, validated_result])

            if hasattr(validator, 'url') and validator.url is not '':
                results += (validator.execute())

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

    def __get_files_for_validator(self, folder_name, file_extensions):
        """Returns file list depends on given extension """
        files = []

        if isinstance(file_extensions, str):
            file_extensions = [file_extensions]

        for fileExtension in file_extensions:
            for root, dirnames, filenames in os.walk(folder_name):
                for filename in fnmatch.filter(filenames, '*.' + fileExtension):
                    if folder_name in ['dist', 'node_modules']:
                        continue

                    files.append(os.path.join(root, filename))

        return files

    def __print_results(self, results):
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

    def __writeResults(self, results):
        """Renders result to the file"""
        file = open('report.txt', 'w')
        file.write('Following tags don\'t have proper translation: \n')
        html_elements_count = 0
        for result in results:
            file.write(result[0] + ': \n')
            for num, line in result[1]:
                file.write('\t' + str(num) + '\t' + line + '\n')
                html_elements_count  += 1

            file.write('\n')

        file.write("Total count: " + str(html_elements_count))
        file.close()


Initialize().execute()
