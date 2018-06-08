# xmindparser

Parse xmind file to programmable data type (e.g. json, xml). Python 3.x required.

# Installation

```shell
pip install xmindparser
```

# Usage - Command Line

```shell
cd /your/xmind/dir

xmindparser your.xmind -json
xmindparser your.xmind -xml #TODO
xmindparser your.xmin  -html #TODO
```

# Usage - via Python

```python
from xmindparser import xmind_to_dict

d = xmind_to_dict('/path/to/your/xmind')
print(d)
```

# Limitations

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

# Examples

- example xmind file
- xmind to json example
- xmind to xml example [TODO]
- xmind to html example [TODO]

# License

MIT