"""
Parse xmind to programmable data types.
"""

config = {'logName': __name__,
          'logLevel': None,
          'logFormat': '%(asctime)s %(levelname)-8s: %(message)s',
          'showTopicId': False,
          'hideEmptyField': True}


def xmind_to_dict(file_path):
    """Open and convert xmind to dict type."""
    from .xreader import open_xmind, get_sheets, sheet_to_dict

    open_xmind(file_path)
    data = []

    for s in get_sheets():
        data.append(sheet_to_dict(s))

    return data
