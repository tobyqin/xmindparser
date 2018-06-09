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
    from .xreader import open_xmind, get_sheet_count, get_sheet_title, get_root_topic, node_to_dict
    open_xmind(file_path)

    data = []
    count = get_sheet_count()
    for i in range(1, count + 1):
        name = get_sheet_title(i)
        root = get_root_topic(i)
        d = {'title': name, 'topic': node_to_dict(root)}
        data.append(d)

    return data
