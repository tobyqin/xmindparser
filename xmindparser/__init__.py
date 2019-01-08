"""
Parse xmind to programmable data types.
"""

import json
import logging
import os
import sys
from zipfile import ZipFile

config = {'logName': __name__,
          'logLevel': None,
          'logFormat': '%(asctime)s %(levelname)-8s: %(message)s',
          'showTopicId': False,
          'hideEmptyValue': True}

cache = {}
_log_name = config['logName'] or __file__
_log_level = config['logLevel'] or logging.WARNING
_log_fmt = config['logFormat'] or '%(asctime)s %(levelname)-8s: %(message)s'

logger = logging.getLogger(_log_name)
logger.setLevel(_log_level)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(config['logFormat']))
logger.addHandler(console_handler)


def set_logger_level(new_level):
    logger.setLevel(new_level)


def is_xmind_zen(file_path):
    """Determine if this is a xmind zen file type."""
    with ZipFile(file_path) as xmind:
        return 'content.json' in xmind.namelist()


def get_xmind_zen_builtin_json(file_path):
    """Read internal content.json from xmind zen file."""
    name = "content.json"
    with ZipFile(file_path) as xmind:
        if name in xmind.namelist():
            content = xmind.open(name).read().decode('utf-8')
            return json.loads(content)

        raise AssertionError("Not a xmind zen file type!")


def _get_out_file_name(xmind_file, suffix):
    assert isinstance(xmind_file, str) and xmind_file.endswith('.xmind'), "Invalid xmind file!"
    name = os.path.abspath(xmind_file[0:-5] + suffix)

    return name


def xmind_to_dict(file_path):
    """Open and convert xmind to dict type."""
    if is_xmind_zen(file_path):
        from .zenreader import open_xmind, get_sheets, sheet_to_dict
    else:
        from .xreader import open_xmind, get_sheets, sheet_to_dict

    open_xmind(file_path)
    data = []

    for s in get_sheets():
        data.append(sheet_to_dict(s))

    return data


def xmind_to_file(file_path, file_type):
    if file_type == 'json':
        return xmind_to_json(file_path)

    elif file_type == 'xml':
        return xmind_to_xml(file_path)

    else:
        raise ValueError('Not supported file type: {}'.format(file_type))


def xmind_to_json(file_path):
    target = _get_out_file_name(file_path, 'json')

    with open(target, 'w', encoding='utf8') as f:
        f.write(json.dumps(xmind_to_dict(file_path), indent=2))

    return target


def xmind_to_xml(file_path):
    try:
        from dicttoxml import dicttoxml
        from xml.dom.minidom import parseString
        target = _get_out_file_name(file_path, 'xml')
        xml = dicttoxml(xmind_to_dict(file_path), custom_root='root')
        xml = parseString(xml.decode('utf8')).toprettyxml(encoding='utf8')

        with open(target, 'w', encoding='utf8') as f:
            f.write(xml.decode('utf8'))

        return target
    except ImportError:
        raise ImportError('Parse xmind to xml require "dicttoxml", try install via pip:\n' +
                          '> pip install dicttoxml')
