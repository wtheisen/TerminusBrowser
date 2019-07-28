import json, os

from config import Config

import pytest

@pytest.fixture
def cfg():
    cfg = Config()
    return cfg

def test_init_location(cfg):
    cfg = Config('/tmp/')
    assert cfg.location == '/tmp/'


def test_init_no_location(cfg):
    cfg = Config()
    assert cfg.location == os.path.expanduser('~') + '/.config/commandChan/config.json'

# I think we need a check config for if file exists
def test_init_wrong_location(cfg):
    cfg = Config('/tmp/')

