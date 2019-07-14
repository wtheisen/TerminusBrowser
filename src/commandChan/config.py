#Config.py

import json, os
import pkg_resources

class Config():
    def __init__(self, location=None):
        if location:
            self.location = location     
        else:
            self.location = os.path.expanduser('~') + '/.config/commandChan/config.json'
        
        self.config = self.load()

    def load(self):
        ''' load json from config file '''
        try:
            with open(self.location) as cfg:
                return json.load(cfg)
        except:
            # add default config to location
            filename = pkg_resources.resource_filename(
                __name__,
                'config.json'
            )
            with open(filename) as cfg:
                data = json.load(cfg)
                self.write(data)
                return data

    def write(self, data):
        ''' overwrites config file with data '''
        os.makedirs(os.path.dirname(self.location), exist_ok=True)
        with open(self.location, 'w') as cfg:
            json.dump(data, cfg)
