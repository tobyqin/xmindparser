from xmindparser import xmind_to_dict
from xmindparser.xreader import logger, set_logger_level
from os.path import join, dirname
from json import dumps
import logging

file_path = join(dirname(__file__), 'test.xmind')
set_logger_level(logging.DEBUG)


def test_xmind_parser_to_dict():
    d = xmind_to_dict(file_path)
    logger.info(dumps(d))
