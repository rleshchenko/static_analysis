import requests
import json
import subprocess
import os
import signal

class PhpValidator:
    """Validator for the angular 1.5 html templates."""
    folders = ''
    url = '127.0.0.1:8000'
    process = None

    def __init__(self):
        self.process = subprocess.Popen(
            ['php -S ' + self.url + ' -t ../PHP_WORLD/'],
            shell=True,
            stdout=open(os.devnull, 'wb'),
            stderr=open(os.devnull, 'wb'),
        )

    def init(self):
        url = raw_input('Please provide php validator url(http://127.0.0.1:8000):')
        self.folders = raw_input('Please insert php folders, comma separated:')
        self.url = url if len(url) > 0 else self.url


    def execute(self, mode=''):
        if len(self.folders) is not 0 and len(self.url) is not 0:
            requestUrl = self.__build_url(mode)
            response = requests.get(requestUrl)
            if response.status_code == 200:
                response = json.loads(response.text)
            return response[0]

    def __del__(self):
        import os, signal
        try:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        except OSError:
            return

    def __build_url(self, mode):
        if len(mode) == 0:
            return 'http://' + self.url + '/' + '?folders=' + self.folders
        return 'http://' + self.url + '/' + '?folders=' + self.folders + '&mode=' + mode