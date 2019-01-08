# xmindparser

[![PyPI](https://img.shields.io/pypi/v/xmindparser.svg)](https://pypi.org/project/xmindparser/)

Parse xmind file to programmable data type (e.g. json, xml). Python 3.x required. Now we support XmindZen file type as well.

See also: [xmind2testlink](https://github.com/tobyqin/xmind2testlink) / [中文文档](https://betacat.online/posts/2018-07-01/parse-xmind-to-programmable-data-type/)

## Installation

```shell
pip install xmindparser
```

## Usage - Command Line

```shell
cd /your/xmind/dir

xmindparser your.xmind -json
xmindparser your.xmind -xml
```

Note: Parse to xml file type require [dicttoxml](https://pypi.org/project/dicttoxml/).

## Usage - via Python

```python
from xmindparser import xmind_to_dict

d = xmind_to_dict('/path/to/your/xmind')
print(d)
```

## Configurations

If you use `xmindparser` via Python, it provides a `config` object, see this example:

```python
import logging
from xmindparser import xmind_to_dict,config

config = {'logName': 'your_log_name',
          'logLevel': logging.DEBUG,
          'logFormat': '%(asctime)s %(levelname)-8s: %(message)s',
          'showTopicId': True, # internal id will be included, default = False
          'hideEmptyValue': False  # empty values will be hidden, default = True
          }

d = xmind_to_dict('/path/to/your/xmind')
print(d)

```

## Limitations (for XmindPro, legacy version)

Please note, following xmind features will not be supported or partially supported.

- Will not parse Pro features, e.g. Task Info, Audio Note
- Will not parse floating topics.
- Will not parse linked topics.
- Will not parse summary info.
- Will not parse relationship info.
- Will not parse boundary info.
- Will not parse attachment object, only name it as `[Attachment] - name`
- Will not parse image object, only name it as `[Image]`
- Rich text format in notes will be parsed as plain text.

# XmindZen Updates

XmindParser will auto detect xmind file created by XmindZen, so you just pass in the file, use it as usual.

```python
from xmindparser import xmind_to_dict

d = xmind_to_dict('/path/to/your/xmind_zen_file')
print(d)
```

Please note, there are a few differences between xmind pro and xmind zen.

- Remove comments, so I will not parse comments.
- Add sticker, but I will not parse it.
- Add callout, this is supported.

Since XmindZen has upgraded the file manifest as json, you can read the built-in json by code like this:

```python
import json

def open_xmind(file_path):
    name = "content.json"
    with ZipFile(file_path) as xmind:
        if name in xmind.namelist():
            content = xmind.open(name).read().decode('utf-8')
            return json.loads(content)

        raise AssertionError("Not a xmind zen file type!")

# xmindparser also provides a shortcut
from xmindparser import get_xmind_zen_builtin_json

content_json = get_xmind_zen_builtin_json(xmind_zen_file)
```

## Examples

![Xmind Example](doc/xmind.png)
[(Download xmind pro file)](tests/xmind_pro.xmind)
[(Download xmind zen file)](tests/xmind_zen.xmind)

- xmind to [json example](doc/example.json)
- xmind to [xml example](doc/example.xml)

## License

MIT
