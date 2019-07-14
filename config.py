#Config.py

import json, os

class Config():
    def __init__(self, location=None):
        if location:
            self.location = location     
        else:
            self.location = '/.config/commandChan/config.json'
        
        self.config = self.load()

    def load(self):
        ''' load json from config file '''
        with open(os.path.expanduser('~') + self.location) as cfg:
            return json.load(cfg)

    def write(self, data):
        ''' overwrites config file with data '''
        with open(os.path.exanduser('~') + self.location, 'w') as cfg:
            json.dump(data)
