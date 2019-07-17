import requests
import json
import subprocess
import os
import signal
from Dto.ResultObject import DetailedResultObject, DetailedResultEntryObject

class PhpValidator:
    """Validator for the angular 1.5 html templates."""
    folders = ''
    url = '127.0.0.1:8000'
    process = None

    def __init__(self):
        self.process = subprocess.Popen(
            ['php -S ' + self.url + ' -t ../../PHP_WORLD/'],
            shell=True,
            stdout=open(os.devnull, 'wb'),
            stderr=open(os.devnull, 'wb'),
        )

    def init(self):
        self.folders = input('Please insert php folders, comma separated:')

    def execute(self, mode):
        result_data = []
        if len(self.folders) is not 0 and len(self.url) is not 0:
            requestUrl = self.__build_url(mode)
            response = requests.get(requestUrl)
            if response.status_code == 200:
                response = json.loads(response.text)
            if len(response) == 0:
                return result_data
            items = response['report']
            for parsed_file in items: 
                result_object = DetailedResultObject()
                result_object.set_file_path(parsed_file['file_path'])
                for untranslated_item in parsed_file['entries']:
                    entryObject = DetailedResultEntryObject()
                    entryObject.set_line_number(untranslated_item['line_number'])
                    entryObject.set_untranslated_line(untranslated_item['line_value'])
                    result_object.add_single_translate_entry(entryObject)

                result_data.append(result_object)

       ## os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

        return result_data

    def __build_url(self, mode):
        if len(mode) == 0:
            return 'http://' + self.url + '/' + '?folders=' + self.folders
        return 'http://' + self.url + '/' + '?folders=' + self.folders + '&mode=' + mode