import os, importlib, argparse, glob


class Initialize:
    parser = ''
    scanners = []

    def __init__(self):
        self.parser = self.__setup_parser()

    def execute(self):
        if self.parser:
            args = self.parser.parse_args()
            self.__import_scanners()
            if args.__contains__('scan_type'):
                scanner = self.__get_scanner(args.scan_type)
            else:
                scanner = self.__get_scanner('flex')

            scanner.execute()

    def __import_scanners(self):
        module_list = os.listdir('./Scanners')

        for moduleItem in module_list:
            if moduleItem.find("init") is not -1 or moduleItem.find("pyc") is not -1:
                continue
            os.chdir('Scanners')
            module = importlib.import_module('Scanners.' + moduleItem[0:-3])
            class_name = getattr(module, moduleItem[0:-3])
            os.chdir('../')

            self.scanners.append(class_name())

    def __setup_parser(self):
        parser = argparse.ArgumentParser(description='Parse Bigcommerce application.')
        parser.add_argument(
            'scan_type',
            metavar='parser',
            type=str,
            default=self.__get_available_scanners(),
            help='Parser type'
        )

        parser.add_argument(
            '--type',
            dest='accumulate',
            action='store_const',
            const=sum,
            default=max,
            help='Provided scanner'
        )

        return parser

    def __get_available_scanners(self):
        list = os.listdir('./Scanners')
        if list[0] == '__init__.py':
            list.pop(0)

        for i, item in enumerate(list):
            item = item[0:-3]
            item = item[0].lower() + item[1:]
            list[i] = item

        return list

    def __get_scanner(self, scanner_type):
        scanner_type = scanner_type.capitalize()
        for scaner in self.scanners:
            if scaner.__class__.__name__ == scanner_type:
                return scaner

        print 'There is no such a scanner. Proceeding with flex'
        return self.scanners[1]



Initialize().execute()
