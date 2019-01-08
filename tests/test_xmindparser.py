from json import dumps, loads
from os import chdir
from os.path import join, dirname, exists
from pathlib import Path

from xmindparser import *
from xmindparser.xreader import logger

chdir(dirname(dirname(__file__)))
xmind_pro_file = join(dirname(__file__), 'xmind_pro.xmind')
xmind_zen_file = join(dirname(__file__), 'xmind_zen.xmind')
expected_json_pro = join(dirname(dirname(__file__)), 'doc/example.json')
expected_json_pro_with_id = join(dirname(dirname(__file__)), 'doc/example_with_id.json')
expected_json_zen = join(dirname(dirname(__file__)), 'doc/example_zen.json')
expected_json_zen_with_id = join(dirname(dirname(__file__)), 'doc/example_zen_with_id.json')
set_logger_level(logging.DEBUG)


def load_json(f):
    return loads(Path(f).read_text())


def test_xmind_to_dict_debug_pro():
    config['showTopicId'] = True
    d = xmind_to_dict(xmind_pro_file)
    logger.info(dumps(d))
    assert load_json(expected_json_pro_with_id) == d


def test_xmind_to_dict_default_pro():
    config['showTopicId'] = False
    d = xmind_to_dict(xmind_pro_file)
    logger.info(dumps(d))
    assert load_json(expected_json_pro) == d


def test_xmind_to_dict_debug_zen():
    config['showTopicId'] = True
    d = xmind_to_dict(xmind_zen_file)
    logger.info(dumps(d))
    assert load_json(expected_json_zen_with_id) == d


def test_xmind_to_dict_default_zen():
    config['showTopicId'] = False
    d = xmind_to_dict(xmind_zen_file)
    logger.info(dumps(d))
    assert load_json(expected_json_zen) == d


def convert_to_file(method, xmind_file, out_file):
    if exists(out_file):
        os.remove(out_file)

    method(xmind_file)
    assert os.path.exists(out_file)
    os.remove(out_file)


def test_xmind_to_json():
    convert_to_file(xmind_to_json, xmind_pro_file, 'tests/xmind_pro.json')
    convert_to_file(xmind_to_json, xmind_zen_file, 'tests/xmind_zen.json')


def test_xmind_to_xml():
    convert_to_file(xmind_to_xml, xmind_pro_file, 'tests/xmind_pro.xml')
    convert_to_file(xmind_to_json, xmind_zen_file, 'tests/xmind_zen.json')


def test_read_builtin_xmind_zen():
    out = get_xmind_zen_builtin_json(xmind_zen_file)
    assert out
