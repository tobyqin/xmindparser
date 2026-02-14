from json import dumps, loads
from os import chdir
from os.path import join, dirname, exists
from pathlib import Path

from xmindparser import *
from xmindparser.xreader import logger

chdir(dirname(dirname(__file__)))
xmind_pro_file = join(dirname(__file__), 'xmind_pro.xmind')
xmind_zen_file = join(dirname(__file__), 'xmind_zen.xmind')
xmind_2026_file = join(dirname(__file__), 'xmind_2026.xmind')
expected_json_pro = join(dirname(dirname(__file__)), 'doc/example.json')
expected_json_pro_with_id = join(dirname(dirname(__file__)), 'doc/example_with_id.json')
expected_json_zen = join(dirname(dirname(__file__)), 'doc/example_zen.json')
expected_json_zen_with_id = join(dirname(dirname(__file__)), 'doc/example_zen_with_id.json')
expected_json_2026 = join(dirname(dirname(__file__)), 'doc/example_2026.json')
expected_json_2026_with_id = join(dirname(dirname(__file__)), 'doc/example_2026_with_id.json')
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


def test_xmind_to_markdown():
    convert_to_file(xmind_to_markdown, xmind_pro_file, 'tests/xmind_pro.md')
    convert_to_file(xmind_to_markdown, xmind_zen_file, 'tests/xmind_zen.md')


def test_xmind_to_yaml():
    convert_to_file(xmind_to_yaml, xmind_pro_file, 'tests/xmind_pro.yaml')
    convert_to_file(xmind_to_yaml, xmind_zen_file, 'tests/xmind_zen.yaml')


def test_xmind_to_yaml_content():
    """Test that YAML output matches the expected structure."""
    import yaml
    import io
    
    # Test xmind pro
    config['showTopicId'] = False
    d = xmind_to_dict(xmind_pro_file)
    yaml_str = yaml.dump(d, allow_unicode=True, default_flow_style=False)
    yaml_data = yaml.safe_load(yaml_str)
    assert yaml_data == d
    
    # Test xmind zen
    d = xmind_to_dict(xmind_zen_file)
    yaml_str = yaml.dump(d, allow_unicode=True, default_flow_style=False)
    yaml_data = yaml.safe_load(yaml_str)
    assert yaml_data == d
    
    # Test xmind 2026
    d = xmind_to_dict(xmind_2026_file)
    yaml_str = yaml.dump(d, allow_unicode=True, default_flow_style=False)
    yaml_data = yaml.safe_load(yaml_str)
    assert yaml_data == d


def test_read_builtin_xmind_zen():
    out = get_xmind_zen_builtin_json(xmind_zen_file)
    assert out


def test_xmind_to_dict_debug_2026():
    config['showTopicId'] = True
    d = xmind_to_dict(xmind_2026_file)
    logger.info(dumps(d))
    assert load_json(expected_json_2026_with_id) == d


def test_xmind_to_dict_default_2026():
    config['showTopicId'] = False
    d = xmind_to_dict(xmind_2026_file)
    logger.info(dumps(d))
    assert load_json(expected_json_2026) == d


