import logging
import re
from xml.etree import ElementTree as  ET
from xml.etree.ElementTree import Element
from zipfile import ZipFile
from . import config
import sys

cache = {}
content_xml = "content.xml"
comments_xml = "comments.xml"

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


def open_xmind(file_path):
    """open xmind as zip file and cache the content."""
    cache.clear()
    with ZipFile(file_path) as xmind:
        for f in xmind.namelist():
            for key in [content_xml, comments_xml]:
                if f == key:
                    cache[key] = xmind.open(f).read().decode('utf-8')


def get_sheet_count():
    tree = xmind_content_to_etree(cache[content_xml])
    assert isinstance(tree, Element)
    count = 0

    for _ in tree.find('sheet'):
        if  _:
            count += 1

    return count


def get_sheet_title(sheet_index):
    tree = xmind_content_to_etree(cache[content_xml])
    return tree.find('./sheet[{}]'.format(sheet_index)).find('title').text


def get_root_topic(sheet_index):
    tree = xmind_content_to_etree(cache[content_xml])
    return tree.find('./sheet[{}]'.format(sheet_index)).find('topic')


# def check_xmind():
#     """check xmind contains valid topics and return root topic node."""
#     tree = xmind_content_to_etree(cache[content_xml])
#     assert isinstance(tree, Element)
#
#     try:
#         root_topic_node = tree.find('sheet').find('topic')
#         logging.info("Parse topic: {}".format(title_of(root_topic_node)))
#     except:
#         logging.error('Cannot find any topic in your xmind!')
#         raise
#
#     return root_topic_node


def node_to_dict(node):
    """parse Element to dict data type."""
    title = title_of(node)
    comment = comments_of(node)
    note = note_of(node)
    makers = maker_of(node)
    child = children_topics_of(node)
    d = {'title': title, 'comment': comment, 'note': note, 'makers': makers}
    if child:
        d['topics'] = []
        for c in child:
            d['topics'].append(node_to_dict(c))

    return d


def xmind_content_to_etree(content):
    # Remove the default namespace definition (xmlns="http://some/namespace")
    xml_content = re.sub(r'\sxmlns="[^"]+"', '', content, count=1)
    return ET.fromstring(xml_content.encode('utf-8'))


def xmind_xml_to_etree(xml_path):
    with open(xml_path) as f:
        content = f.read()
        return xmind_content_to_etree(content)


def comments_of(node):
    if cache.get(comments_xml, None):
        node_id = node.attrib.get('id', None)

        if node_id:
            xml_root = xmind_content_to_etree(cache[comments_xml])
            comment = xml_root.find('./comment[@object-id="{}"]'.format(node_id))

            if comment is not None:
                return comment.find('content').text


def title_of(node):
    title = node.find('title')

    if title is not None:
        return title.text


def note_of(topic_node):
    note_node = topic_node.find('notes')

    if note_node is not None:
        note = note_node.find('plain').text
        return note.strip()


def debug_node(node, comments):
    s = ET.tostring(node)
    logger.debug('{}: {}'.format(comments, s))


def maker_of(topic_node, maker_prefix=None):
    maker_node = topic_node.find('marker-refs')
    if maker_node is not None:
        makers = []
        for maker in maker_node:
            makers.append(maker.attrib['marker-id'])

        if maker_prefix:
            for m in makers:
                if m.startswith(maker_prefix):
                    return m
        else:
            return makers


def children_topics_of(topic_node):
    children = topic_node.find('children')

    if children is not None:
        return children.find('./topics[@type="attached"]')
