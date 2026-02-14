# xmindparser

[![PyPI](https://img.shields.io/pypi/v/xmindparser.svg)](https://pypi.org/project/xmindparser/)

Parse xmind file to programmable data type (e.g. json, xml). Python 3.x required. Now it supports Xmind (including Xmind Zen and Xmind 2026) file type as well.

See also: [xmind2testlink](https://github.com/tobyqin/xmind2testlink) / [中文文档](README_CN.md)

## Installation

```shell
pip install xmindparser
```

## Usage - Command Line

```shell
cd /your/xmind/dir

xmindparser your.xmind -json
xmindparser your.xmind -xml
xmindparser your.xmind -yaml
xmindparser your.xmind -markdown
```

Note: Parse to xml/yaml file types require additional packages:

- xml: [dicttoxml](https://pypi.org/project/dicttoxml/)
- yaml: [pyyaml](https://pypi.org/project/pyyaml/)

## Usage - via Python

```python
from xmindparser import xmind_to_dict

d = xmind_to_dict('/path/to/your/xmind')
print(d)
```

See example output: [json](doc/example.json)

### Convert to Markdown

```python
from xmindparser import xmind_to_markdown

# Convert xmind to markdown file
output_file = xmind_to_markdown('/path/to/your/xmind')
print(f'Generated: {output_file}')
```

Or use the generic `xmind_to_file` function:

```python
from xmindparser import xmind_to_file

# Convert to markdown
output_file = xmind_to_file('/path/to/your/xmind', 'markdown')
print(f'Generated: {output_file}')
```

## Configuration

If you use `xmindparser` via Python, it provides a `config` object, check this example:

```python
import logging
from xmindparser import xmind_to_dict, config, apply_config

# Modify config settings
config['logName'] = 'your_log_name'
config['logLevel'] = logging.DEBUG
config['logFormat'] = '%(asctime)s %(levelname)-8s: %(message)s'
config['showTopicId'] = True  # internal id will be included, default = False
config['hideEmptyValue'] = False  # empty values will be hidden, default = True

# Apply the config changes (required for logging settings to take effect)
apply_config()

d = xmind_to_dict('/path/to/your/xmind')
print(d)

```

**Note:** After modifying logging-related config options (`logName`, `logLevel`, `logFormat`), you must call `apply_config()` to apply the changes. The `showTopicId` and `hideEmptyValue` options take effect immediately without calling `apply_config()`.

## Limitations (for Xmind 8)

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

## Xmind (including Zen and 2026)

`xmindparser` will auto detect xmind file created by Xmind (including Zen/2026 version) or Xmind 8, you can pass in the file as usual.

```python
from xmindparser import xmind_to_dict

d = xmind_to_dict('/path/to/your/xmind_zen_file')
print(d)
```

Please note, there are a few differences between Xmind 8 and Xmind (Zen/2026).

- Comments feature removed, so I will not parse it in ZEN.
- Add feature - sticker, I parse it as `image` dict type.
- Add feature - callout, I parse it as `list` type. (not sure existed in legacy?)

Since Xmind (Zen/2026) uses json as the internal content file, you can read it by code like this:

```python
import json

def get_xmind_zen_json(file_path):
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

- [Download xmind 8 example](tests/xmind_pro.xmind)
- [Download xmind (Zen/2026) example](tests/xmind_zen.xmind)
- [Download xmind 2026 example](tests/xmind_2026.xmind)
- Output: [json example](doc/example.json)
- Output: [xml example](doc/example.xml)
- Output: [yaml example](doc/example.yaml)
- Output: [markdown example](doc/example.md)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, code style guidelines, and the pull request process.

## License

MIT
