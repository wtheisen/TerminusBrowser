import json, os, sys

sys.path.append('src')
from config import Config

import pytest

DEFAULT = os.path.expanduser('~') + '/.config/commandChan/config.json'
test_list = [
    ('', DEFAULT),
    ('/tmp/', DEFAULT),
    ('/tmp/cfg.json', '/tmp/cfg.json')
]

@pytest.mark.parametrize("test_input, expected", test_list)
def test_location(test_input, expected):
    assert Config(test_input).location == expected
