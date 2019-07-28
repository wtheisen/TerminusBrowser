import json, os

from config import Config

import pytest

@pytest.fixture
def cfg():
    cfg = Config()
    return cfg

def test_dir_location(cfg):
    cfg = Config('/tmp/')
    assert cfg.location == '/tmp/'


def test_init_no_location(cfg):
    cfg = Config()
    assert cfg.location == os.path.expanduser('~') + '/.config/commandChan/config.json'

def test_init_wrong_location(cfg):
    cfg = Config('./fake.json')

def test_init_wrong_filetype(cfg):
    cfg = Config('./debug.log')

