# xmindparser

[![PyPI](https://img.shields.io/pypi/v/xmindparser.svg)](https://pypi.org/project/xmindparser/)

将 xmind 文件转换为可编程的数据类型（如 json、xml）。需要 Python 3.x。支持 Xmind（包括 Xmind Zen 和 Xmind 2026）文件类型。

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
xmindparser your.xmind -yaml
xmindparser your.xmind -markdown
```

注意：解析为 xml/yaml 文件类型需要安装额外依赖：

- xml：[dicttoxml](https://pypi.org/project/dicttoxml/)
- yaml：[pyyaml](https://pypi.org/project/pyyaml/)

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
from xmindparser import xmind_to_dict, config, apply_config

# 修改配置设置
config['logName'] = 'your_log_name'
config['logLevel'] = logging.DEBUG
config['logFormat'] = '%(asctime)s %(levelname)-8s: %(message)s'
config['showTopicId'] = True  # 包含内部 id，默认为 False
config['hideEmptyValue'] = False  # 隐藏空值，默认为 True

# 应用配置更改（日志相关设置需要调用此函数才能生效）
apply_config()

d = xmind_to_dict('/path/to/your/xmind')
print(d)

```

**注意：** 修改日志相关的配置选项（`logName`、`logLevel`、`logFormat`）后，必须调用 `apply_config()` 来应用更改。`showTopicId` 和 `hideEmptyValue` 选项无需调用 `apply_config()` 即可立即生效。

## 限制（针对 Xmind 8）

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

## Xmind 支持（包括 Zen 和 2026）

`xmindparser` 会自动检测 Xmind（包括 Zen/2026 版本）或 Xmind 8 创建的 xmind 文件，您可以像平常一样传入文件。

```python
from xmindparser import xmind_to_dict

d = xmind_to_dict('/path/to/your/xmind_zen_file')
print(d)
```

请注意，Xmind 8 和 Xmind（Zen/2026）之间存在一些差异。

- 评论功能已移除，因此我不会在 ZEN 中解析它
- 新增功能 - 贴纸，我将其解析为 `image` 字典类型
- 新增功能 - 标注，我将其解析为 `list` 类型（不确定传统版中是否存在？）

由于 Xmind（Zen/2026）使用 json 作为内部内容文件，您可以通过以下代码读取：

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

- [下载 xmind 8 示例](tests/xmind_pro.xmind)
- [下载 xmind（Zen/2026）示例](tests/xmind_zen.xmind)
- [下载 xmind 2026 示例](tests/xmind_2026.xmind)
- 输出：[json 示例](doc/example.json)
- 输出：[xml 示例](doc/example.xml)
- 输出：[yaml 示例](doc/example.yaml)
- 输出：[markdown 示例](doc/example.md)

## 许可证

MIT
