"""
Parse xmind to programmable data types.
"""

import json
import os

config = {'logName': __name__,
          'logLevel': None,
          'logFormat': '%(asctime)s %(levelname)-8s: %(message)s',
          'showTopicId': False,
          'hideEmptyField': True}


def _get_out_file_name(xmind_file, suffix):
    assert isinstance(xmind_file, str) and xmind_file.endswith('.xmind'), "Invalid xmind file!"
    name = os.path.abspath(xmind_file[0:-5] + suffix)

    return name


def xmind_to_dict(file_path):
    """Open and convert xmind to dict type."""
    from .xreader import open_xmind, get_sheets, sheet_to_dict

    open_xmind(file_path)
    data = []

    for s in get_sheets():
        data.append(sheet_to_dict(s))

    return data


def xmind_to_file(file_path, file_type):
    if file_type == 'json':
        return xmind_to_json(file_path)
    else:
        raise ValueError('Not supported file type: {}'.format(file_type))


def xmind_to_json(file_path):
    target = _get_out_file_name(file_path, 'json')

    with open(target, 'w') as f:
        f.write(json.dumps(xmind_to_dict(file_path), indent=2))

    return target
