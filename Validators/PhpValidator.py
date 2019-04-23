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

    def init(self):
        url = raw_input('Please provide php validator url(http://127.0.0.1:8000):')
        self.folders = raw_input('Please insert php folders, comma separated:')
        self.url = url if len(url) > 0 else self.url
        self.process = subprocess.Popen(
            ['php -S ' + self.url + ' -t ../PHP_WORLD/'],
            shell=True,
            stdout=open(os.devnull, 'wb'),
            stderr=open(os.devnull, 'wb'),
        )

    def execute(self):
        if self.folders is not '' and self.url is not '':
            response = requests.get('http://' + self.url + '/' + '?folders=' + self.folders)
            if response.status_code == 200:
                response = json.loads(response.text)

            return response[0]

    def __del__(self):
        if self.process is not None:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)