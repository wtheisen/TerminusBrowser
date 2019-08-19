#Config.py

import json, os

from customeTypes import SITE

import logging
log = logging.getLogger(__name__)

class Config():
    def __init__(self, location=None):
        if location and not os.path.isdir(location):
            self.location = location
        else:
            self.location = os.path.expanduser('~') + '/.config/TerminusBrowser/config.json'

        # load default config
        self.defaults = self._load('./src/default_config.json')
        if not self.defaults:
            log.debug('ERROR: No default file')

        # load user config
        self.config = self._load(self.location)
        if not self.config:
            self.config = self.defaults
            self._write(self.defaults)

        self.dirty = False

    def add_topic(self, key, topic):
        if isinstance(key, SITE):
            key = key.name

        self.config.get(key, {}).get('boards',[]).append(topic)
        self.dirty = True

    def get(self, key):
        ''' get value from config, falling back to defaults if needed '''
        if self.config.get(key, None):
            return self.config.get(key)
        else:
            log.debug('Key {} not found, trying defaults'.format(key))
            return self.defaults.get(key, None)

    def deep_get(self, key, inner_key):
        ''' deep get from config, falling back to defaults if needed '''
        if isinstance(key, SITE):
            key = key.name

        if self.config.get(key, {}).get(inner_key, None):
            return self.config.get(key).get(inner_key)
        else:
            log.debug('Key {}:{} not found, trying defaults'.format(key, inner_key))
            return self.defaults.get(key, {}).get(inner_key, None)

    def set(self, key, value):
        ''' set value in config, setting dirty bit if value is changed '''
        if self.config.get(key) == value:
            return
        self.config[key] = value
        self.dirty = True

    def deep_set(self, key, inner_key, value):
        ''' deep set value in config '''
        if isinstance(key, SITE):
            key = key.name

        if self.config.get(key, {}).get(inner_key) == value:
            return
        self.config.get(key, {})[inner_key] = value
        self.dirty = True

    def update_file(self):
        ''' Updates config file if dirty, returns True if updated '''
        if not self.dirty:
            return False

        self._write(self.config)
        self.dirty = False
        return True

    def _load(self, location):
        ''' load json from config file '''
        try:
            with open(location) as cfg:
                return json.load(cfg)
        except:
            # add default config to location
            log.debug('File {} does not exist'.format(location))
            return None

    def _write(self, data):
        ''' overwrites config file with data '''
        os.makedirs(os.path.dirname(self.location), exist_ok=True)
        with open(self.location, 'w') as cfg:
            json.dump(data, cfg, indent=4) 
