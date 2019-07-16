import os, fnmatch, glob, importlib
from Output import Console.Console, ReportFile.ReportFile

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

        
        if write_report == '1':
            return ReportFile().execute(results)

        return Console().execute(results)

    def validate(self):
        pass

    def __import_validators(self):
        """Returns list of the avaliable validators"""
        os.chdir('Validators')
        validator_type = self.mode.capitalize()
        validator_dir = './Validators' + '/' + validator_type # TODO check if os.path.join can work with multiple dirs
        module_list = glob.glob(os.path.dirname(validator_dir) + "/*.py")
        for moduleItem in module_list:
            if moduleItem.find("init") is not -1:
                continue
            module = importlib.import_module('Validators.' + moduleItem[2:-3])
            class_name = getattr(module, moduleItem[2:-3])

            self._validators.append(class_name())
        os.chdir('../')

    def _get_files_for_validator(self, folder_name, file_extensions):
        pass
