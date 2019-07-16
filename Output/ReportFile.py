import os, importlib


class ReportFile:
    processor = ''
    """Renders result in the console"""

    def execute(self, results, mode):
        self.processor = self.get_processor(mode)
        for item in results:
            print ('Total strings count: ' + str(results[0]) + ' \n')
            print ('Untranslated strings count: ' + str(results[1]) + ' \n')

    def get_processor(self, mode):
        os.chdir('Output')
        os.chdir('Processor')
        processor_type = mode.capitalize()
        module = importlib.import_module(processor_type)
        class_name = getattr(module, processor_type)
        os.chdir('../../')

        return class_name()
