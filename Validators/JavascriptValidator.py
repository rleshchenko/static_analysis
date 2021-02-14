import requests
import json
import subprocess
import os

class JavascriptValidator:
    """Validator for the angular/react models, viewmodels, written in JS/TS"""
    folders = ''
    url = '127.0.0.1:8124'
    process = None

    def __init__(self):
        self.process = subprocess.Popen(
            ['node  ../JS_WORLD/index.js'],
            shell=True,
        )

    def init(self):
        self.folders = raw_input('Please insert js/ts folders, comma separated:')

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
        return 'http://' + self.url + '/' + '?folders=' + self.folders
