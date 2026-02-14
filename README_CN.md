# xmindparser

[![PyPI](https://img.shields.io/pypi/v/xmindparser.svg)](https://pypi.org/project/xmindparser/)

将 xmind 文件转换为可编程的数据类型（如 json、xml）。需要 Python 3.x。支持 XmindZen 文件类型。

相关项目：[xmind2testlink](https://github.com/tobyqin/xmind2testlink)

English version: [README.md](README.md)

## 安装

```shell
pip install xmindparser
```

## 使用方法 - 命令行

```shell
cd /your/xmind/dir

xmindparser your.xmind -json
xmindparser your.xmind -xml
xmindparser your.xmind -markdown
```

注意：解析为 xml 文件类型需要安装 [dicttoxml](https://pypi.org/project/dicttoxml/)。

## 使用方法 - Python 代码

```python
from xmindparser import xmind_to_dict

d = xmind_to_dict('/path/to/your/xmind')
print(d)
```

查看示例输出：[json 示例](doc/example.json)

### 转换为 Markdown

```python
from xmindparser import xmind_to_markdown

# 将 xmind 转换为 markdown 文件
output_file = xmind_to_markdown('/path/to/your/xmind')
print(f'Generated: {output_file}')
```

或者使用通用的 `xmind_to_file` 函数：

```python
from xmindparser import xmind_to_file

# 转换为 markdown
output_file = xmind_to_file('/path/to/your/xmind', 'markdown')
print(f'Generated: {output_file}')
```

## 配置

如果您通过 Python 使用 `xmindparser`，它提供了一个 `config` 对象，请查看以下示例：

```python
import logging
from xmindparser import xmind_to_dict, config

config = {'logName': 'your_log_name',
          'logLevel': logging.DEBUG,
          'logFormat': '%(asctime)s %(levelname)-8s: %(message)s',
          'showTopicId': True, # 包含内部 id，默认为 False
          'hideEmptyValue': False  # 隐藏空值，默认为 True
          }

d = xmind_to_dict('/path/to/your/xmind')
print(d)

```

## 限制（针对 Xmind 传统版本）

请注意，以下 xmind 功能将不被支持或仅部分支持。

- 不会解析 Pro 功能，例如任务信息、音频笔记
- 不会解析浮动主题
- 不会解析链接主题
- 不会解析摘要信息
- 不会解析关系信息
- 不会解析边界信息
- 不会解析附件对象，仅将其命名为 `[Attachment] - name`
- 不会解析图片对象，仅将其命名为 `[Image]`
- 笔记中的富文本格式将解析为纯文本

## XmindZen 支持

`xmindparser` 会自动检测 XmindZen 或 XmindPro 创建的 xmind 文件，您可以像平常一样传入 ZEN 文件。

```python
from xmindparser import xmind_to_dict

d = xmind_to_dict('/path/to/your/xmind_zen_file')
print(d)
```

请注意，xmind 传统版和 xmind zen 之间存在一些差异。

- 评论功能已移除，因此我不会在 ZEN 中解析它
- 新增功能 - 贴纸，我将其解析为 `image` 字典类型
- 新增功能 - 标注，我将其解析为 `list` 类型（不确定传统版中是否存在？）

由于 XmindZen 已将内部内容文件升级为 json，您可以通过以下代码读取：

```python
import json

def get_xmind_zen_json(file_path):
    name = "content.json"
    with ZipFile(file_path) as xmind:
        if name in xmind.namelist():
            content = xmind.open(name).read().decode('utf-8')
            return json.loads(content)

        raise AssertionError("Not a xmind zen file type!")

# xmindparser 也提供了快捷方式
from xmindparser import get_xmind_zen_builtin_json

content_json = get_xmind_zen_builtin_json(xmind_zen_file)
```

## 示例

![Xmind 示例](doc/xmind.png)

- [下载 xmind pro 示例](tests/xmind_pro.xmind)
- [下载 xmind zen 示例](tests/xmind_zen.xmind)
- 输出：[json 示例](doc/example.json)
- 输出：[xml 示例](doc/example.xml)
- 输出：[markdown 示例](doc/example.md)

## 许可证

MIT
