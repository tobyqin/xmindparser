import logging
from json import dumps, loads
from os.path import join, dirname, exists
from pathlib import Path

from xmindparser import *
from xmindparser.xreader import logger, set_logger_level

xmind_file = join(dirname(__file__), 'test.xmind')
expected_json = join(dirname(dirname(__file__)), 'doc/example.json')
expected_json_with_id = join(dirname(dirname(__file__)), 'doc/example_with_id.json')
set_logger_level(logging.DEBUG)


def load_json(f):
    return loads(Path(f).read_text())


def test_xmind_to_dict_debug():
    config['showTopicId'] = True
    d = xmind_to_dict(xmind_file)
    logger.info(dumps(d))
    assert load_json(expected_json_with_id) == d


def test_xmind_to_dict_default():
    d = xmind_to_dict(xmind_file)
    logger.info(dumps(d))
    assert load_json(expected_json) == d


def convert_to_file(method, name):
    if exists(name):
        os.remove(name)

    method(xmind_file)
    assert os.path.exists(name)
    os.remove(name)


def test_xmind_to_json():
    convert_to_file(xmind_to_json, 'test.json')


def test_xmind_to_xml():
    convert_to_file(xmind_to_xml, 'test.xml')
