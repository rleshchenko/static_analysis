import os, importlib


class Console:

    def execute(self, results, mode):
        self.processor = self.get_processor(mode)
        output_content = self.processor.execute(results)
        for item in output_content:
            print(item)

    def get_processor(self, mode):
        os.chdir('Output')
        os.chdir('Processor')
        processor_type = mode.capitalize()
        module = importlib.import_module(processor_type)
        class_name = getattr(module, processor_type)
        os.chdir('../../')

        return class_name()
