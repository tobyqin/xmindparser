import logging
from json import dumps
from os.path import join, dirname, exists

from xmindparser import *
from xmindparser.xreader import logger, set_logger_level

file_path = join(dirname(__file__), 'test.xmind')
set_logger_level(logging.DEBUG)


def test_xmind_to_dict_debug():
    config['showTopicId'] = True
    d = xmind_to_dict(file_path)
    logger.info(dumps(d))


def test_xmind_to_dict_default():
    d = xmind_to_dict(file_path)
    logger.info(dumps(d))


def test_xmind_to_json():
    if exists('test.json'):
        os.remove('test.json')

    xmind_to_json(file_path)
    assert os.path.exists('test.json')
    os.remove('test.json')
