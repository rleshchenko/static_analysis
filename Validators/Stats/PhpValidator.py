import requests
import json
import subprocess
import os
import signal
from Dto.ResultObject import StatsResultObject


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

    def execute(self, mode=''):
        if len(self.folders) is not 0 and len(self.url) is not 0:
            requestUrl = self.__build_url(mode)
            response = requests.get(requestUrl)
            entryObject = StatsResultObject()

            if response.status_code == 200:
                response = json.loads(response.text)

                entryObject.set_total_count(response['total_strings_count'])
                entryObject.set_untranslated_count(response['untranslated_entries_count'])

            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

            return entryObject

    def __build_url(self, mode):
        if len(mode) == 0:
            return 'http://' + self.url + '/' + '?folders=' + self.folders
        return 'http://' + self.url + '/' + '?folders=' + self.folders + '&mode=' + mode
