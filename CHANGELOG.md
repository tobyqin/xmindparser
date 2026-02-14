## Change Log

1.2.1

- Fix config system to support dynamic logger reconfiguration.
- Add `apply_config()` function to apply logging configuration changes.
- Add comprehensive tests for all config options (hideEmptyValue, logFormat, logLevel, logName).
- Update documentation with proper config usage examples.

  1.2.0

- Add YAML export support with `xmind_to_yaml()` function.
- Add support for Xmind 2026 file format.
- Update documentation with local Chinese README and developer guide.
- Rename Xmind legacy to Xmind 8, Xmind Zen to Xmind.

  1.1.2

- Fix Chinese character encoding issue in JSON export by adding `ensure_ascii=False` to `json.dumps()`.

  1.1.1

- Add Python 3.14 support.

  1.1.0

- Add support for converting xmind to markdown format.
- New function `xmind_to_markdown()` to convert xmind file to markdown.
- Command line support: `xmindparser your.xmind -markdown`.

  1.0.9

- Update Python version classifiers to support 3.9, 3.10, 3.11, 3.12, 3.13.
- Fix DeprecationWarning for element truth value testing in Python 3.13.

  1.0.8

- Handle empty title name for xmind zen in some cases.

  1.0.6

- Keep empty topic title as null but not "[Blank]"

  1.0.5

- Support xmind zen file type.

  1.0.4

- Support parse label feature.

  1.0.2

- Rename config key names.

  1.0.1

- Support parse xmind to xml file type.

  1.0.0

- Support parse xmind to dict data type with Python.
- Support parse xmind to json file type.
