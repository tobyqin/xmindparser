import re
from xml.etree import ElementTree as  ET
from xml.etree.ElementTree import Element
from zipfile import ZipFile

from . import config, logger, cache

content_xml = "content.xml"
comments_xml = "comments.xml"


def open_xmind(file_path):
    """open xmind as zip file and cache the content."""
    cache.clear()
    with ZipFile(file_path) as xmind:
        for f in xmind.namelist():
            for key in [content_xml, comments_xml]:
                if f == key:
                    cache[key] = xmind.open(f).read().decode('utf-8')


def get_sheets():
    """get all sheet as generator and yield."""
    tree = xmind_content_to_etree(cache[content_xml])
    assert isinstance(tree, Element)

    for sheet in tree.findall('sheet'):
        yield sheet


def sheet_to_dict(sheet):
    """convert a sheet to dict type."""
    topic = sheet.find('topic')
    result = {'title': title_of(sheet), 'topic': node_to_dict(topic), 'structure': get_sheet_structure(sheet)}

    if config['showTopicId']:
        result['id'] = sheet.attrib['id']

    if config['hideEmptyValue']:
        result = {k: v for k, v in result.items() if v}

    return result


def get_sheet_structure(sheet):
    root_topic = sheet.find('topic')
    return root_topic.attrib.get('structure-class', None)


def node_to_dict(node):
    """parse Element to dict data type."""
    child = children_topics_of(node)

    d = {'title': title_of(node),
         'comment': comments_of(node),
         'note': note_of(node),
         'makers': maker_of(node),
         'labels': labels_of(node),
         'link': link_of(node)}

    if d['link']:

        if d['link'].startswith('xmind'):
            d['link'] = '[To another xmind topic!]'

        if d['link'].startswith('xap:attachments'):
            del d['link']
            d['title'] = '[Attachment]{0}'.format(d['title'])

    if child:
        d['topics'] = []
        for c in child:
            d['topics'].append(node_to_dict(c))

    if config['showTopicId']:
        d['id'] = id_of(node)

    if config['hideEmptyValue']:
        d = {k: v for k, v in d.items() if v or k == 'title'}

    return d


def xmind_content_to_etree(content):
    # Remove the default namespace definition (xmlns="http://some/namespace")
    xml_content = re.sub(r'\sxmlns="[^"]+"', '', content, count=1)

    # Replace xml tag with namespace
    xml_content = xml_content.replace('<xhtml:img', '<img')

    # Replace link attrib with namespace
    xml_content = xml_content.replace('xlink:href', 'href')
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
            result = []

            for c in xml_root.findall('comment'):

                if c.attrib['object-id'] == node_id:
                    i = {'author': c.attrib['author'], 'content': c.find('content').text}

                    if config['showTopicId']:
                        i['id'] = c.attrib['object-id']

                    result.append(i)

            return result if result else None


def id_of(node):
    return node.attrib.get('id', None)


def image_of(node):
    img = node.find('img')

    if img is not None:
        return '[Image]'


def link_of(node):
    return node.attrib.get('href', None)


def title_of(node):
    if image_of(node):
        return image_of(node)

    title = node.find('title')

    if title is not None:
        return title.text


def labels_of(node):
    label_node = node.find('labels')

    if label_node is not None:
        labels = []
        for _ in label_node.findall('label'):
            labels.append(_.text)

        return labels if labels else None


def note_of(node):
    note_node = node.find('notes')

    if note_node is not None:
        note = note_node.find('plain').text
        return note.strip()


def debug_node(node, comments):
    s = ET.tostring(node)
    logger.debug('{}: {}'.format(comments, s))
    return s


def maker_of(topic_node):
    maker_node = topic_node.find('marker-refs')
    if maker_node is not None:
        makers = []
        for maker in maker_node:
            makers.append(maker.attrib['marker-id'])

        return makers


def children_topics_of(topic_node):
    children = topic_node.find('children')

    if children is not None:
        return children.find('./topics[@type="attached"]')
