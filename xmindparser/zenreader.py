import json
from zipfile import ZipFile

from . import config, cache

content_json = "content.json"


def open_xmind(file_path):
    """open xmind as zip file and cache the content."""
    cache.clear()
    with ZipFile(file_path) as xmind:
        for f in xmind.namelist():
            for key in [content_json]:
                if f == key:
                    cache[key] = xmind.open(f).read().decode('utf-8')


def get_sheets():
    """get all sheet as generator and yield."""
    for sheet in json.loads(cache[content_json]):
        yield sheet


def sheet_to_dict(sheet):
    """convert a sheet to dict type."""
    topic = sheet['rootTopic']
    result = {'title': sheet['title'], 'topic': node_to_dict(topic), 'structure': get_sheet_structure(sheet)}

    if config['showTopicId']:
        result['id'] = sheet['id']

    if config['hideEmptyValue']:
        result = {k: v for k, v in result.items() if v}

    return result


def get_sheet_structure(sheet):
    root_topic = sheet['rootTopic']
    return root_topic.get('structureClass', None)


def node_to_dict(node):
    """parse Element to dict data type."""
    child = children_topics_of(node)

    d = {'title': node.get('title', ''),
         'note': note_of(node),
         'makers': maker_of(node),
         'labels': labels_of(node),
         'link': link_of(node),
         'image': image_of(node),
         'callout': callout_of(node)}

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
        d['id'] = node['id']

    if config['hideEmptyValue']:
        d = {k: v for k, v in d.items() if v or k == 'title'}

    return d


def children_topics_of(topic_node):
    children = topic_node.get('children', None)

    if children:
        return children.get('attached', None)


def link_of(node):
    return node.get('href', None)


def image_of(node):
    return node.get('image', None)


def labels_of(node):
    return node.get('labels', None)


def note_of(node):
    note_node = node.get('notes', None)

    if note_node:
        note = note_node.get('plain', None)
        if note:
            return note.get('content', '').strip()


def maker_of(topic_node):
    maker_node = topic_node.get('markers', None)
    if maker_node is not None:
        makers = []
        for maker in maker_node:
            makers.append(maker.get('markerId', None))

        return makers


def callout_of(topic_node):
    callout = topic_node.get('children', None)
    if callout:
        callout = callout.get('callout', None)
        if callout:
            return [x['title'] for x in callout]
