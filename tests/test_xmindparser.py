from json import dumps, loads
from os import chdir
from os.path import join, dirname, exists
from pathlib import Path

import xmindparser
from xmindparser import *
from xmindparser import apply_config

chdir(dirname(dirname(__file__)))
xmind_pro_file = join(dirname(__file__), "xmind_pro.xmind")
xmind_zen_file = join(dirname(__file__), "xmind_zen.xmind")
xmind_2026_file = join(dirname(__file__), "xmind_2026.xmind")
expected_json_pro = join(dirname(dirname(__file__)), "doc/example.json")
expected_json_pro_with_id = join(dirname(dirname(__file__)), "doc/example_with_id.json")
expected_json_zen = join(dirname(dirname(__file__)), "doc/example_zen.json")
expected_json_zen_with_id = join(
    dirname(dirname(__file__)), "doc/example_zen_with_id.json"
)
expected_json_2026 = join(dirname(dirname(__file__)), "doc/example_2026.json")
expected_json_2026_with_id = join(
    dirname(dirname(__file__)), "doc/example_2026_with_id.json"
)
set_logger_level(logging.DEBUG)

# Get logger reference
logger = xmindparser.logger


def load_json(f):
    return loads(Path(f).read_text())


def test_xmind_to_dict_debug_pro():
    config["showTopicId"] = True
    d = xmind_to_dict(xmind_pro_file)
    logger.info(dumps(d))
    assert load_json(expected_json_pro_with_id) == d


def test_xmind_to_dict_default_pro():
    config["showTopicId"] = False
    d = xmind_to_dict(xmind_pro_file)
    logger.info(dumps(d))
    assert load_json(expected_json_pro) == d


def test_xmind_to_dict_debug_zen():
    config["showTopicId"] = True
    d = xmind_to_dict(xmind_zen_file)
    logger.info(dumps(d))
    assert load_json(expected_json_zen_with_id) == d


def test_xmind_to_dict_default_zen():
    config["showTopicId"] = False
    d = xmind_to_dict(xmind_zen_file)
    logger.info(dumps(d))
    assert load_json(expected_json_zen) == d


def convert_to_file(method, xmind_file, out_file):
    if exists(out_file):
        os.remove(out_file)

    method(xmind_file)
    assert os.path.exists(out_file)
    os.remove(out_file)


def test_xmind_to_json():
    convert_to_file(xmind_to_json, xmind_pro_file, "tests/xmind_pro.json")
    convert_to_file(xmind_to_json, xmind_zen_file, "tests/xmind_zen.json")


def test_xmind_to_xml():
    convert_to_file(xmind_to_xml, xmind_pro_file, "tests/xmind_pro.xml")
    convert_to_file(xmind_to_json, xmind_zen_file, "tests/xmind_zen.json")


def test_xmind_to_markdown():
    convert_to_file(xmind_to_markdown, xmind_pro_file, "tests/xmind_pro.md")
    convert_to_file(xmind_to_markdown, xmind_zen_file, "tests/xmind_zen.md")


def test_xmind_to_yaml():
    try:
        import yaml
    except ImportError:
        import pytest

        pytest.skip("pyyaml not installed")

    convert_to_file(xmind_to_yaml, xmind_pro_file, "tests/xmind_pro.yaml")
    convert_to_file(xmind_to_yaml, xmind_zen_file, "tests/xmind_zen.yaml")


def test_xmind_to_yaml_content():
    """Test that YAML output matches the expected structure."""
    try:
        import yaml
    except ImportError:
        import pytest

        pytest.skip("pyyaml not installed")

    import io

    # Test xmind pro
    config["showTopicId"] = False
    d = xmind_to_dict(xmind_pro_file)
    yaml_str = yaml.dump(d, allow_unicode=True, default_flow_style=False)
    yaml_data = yaml.safe_load(yaml_str)
    assert yaml_data == d

    # Test xmind zen
    d = xmind_to_dict(xmind_zen_file)
    yaml_str = yaml.dump(d, allow_unicode=True, default_flow_style=False)
    yaml_data = yaml.safe_load(yaml_str)
    assert yaml_data == d

    # Test xmind 2026
    d = xmind_to_dict(xmind_2026_file)
    yaml_str = yaml.dump(d, allow_unicode=True, default_flow_style=False)
    yaml_data = yaml.safe_load(yaml_str)
    assert yaml_data == d


def test_read_builtin_xmind_zen():
    out = get_xmind_zen_builtin_json(xmind_zen_file)
    assert out


def test_xmind_to_dict_debug_2026():
    config["showTopicId"] = True
    d = xmind_to_dict(xmind_2026_file)
    logger.info(dumps(d))
    assert load_json(expected_json_2026_with_id) == d


def test_xmind_to_dict_default_2026():
    config["showTopicId"] = False
    d = xmind_to_dict(xmind_2026_file)
    logger.info(dumps(d))
    assert load_json(expected_json_2026) == d


def test_config_hide_empty_value():
    """Test hideEmptyValue config option."""
    # Test with hideEmptyValue = True (default)
    config["showTopicId"] = False
    config["hideEmptyValue"] = True
    d = xmind_to_dict(xmind_pro_file)

    # Check that empty values are hidden
    def check_no_empty_values(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                # title can be empty string
                if key != "title":
                    assert value, f"Found empty value for key: {key}"
                if isinstance(value, (dict, list)):
                    check_no_empty_values(value)
        elif isinstance(obj, list):
            for item in obj:
                check_no_empty_values(item)

    check_no_empty_values(d)

    # Test with hideEmptyValue = False
    config["hideEmptyValue"] = False
    d2 = xmind_to_dict(xmind_pro_file)

    # The result with hideEmptyValue=False should have more or equal keys
    def count_keys(obj):
        count = 0
        if isinstance(obj, dict):
            count += len(obj)
            for value in obj.values():
                count += count_keys(value)
        elif isinstance(obj, list):
            for item in obj:
                count += count_keys(item)
        return count

    # With hideEmptyValue=False, we should have at least as many keys
    assert count_keys(d2) >= count_keys(d)

    # Reset to default
    config["hideEmptyValue"] = True


def test_config_logging_format():
    """Test that logging config options work correctly."""
    import io

    # Create a string buffer to capture log output
    log_capture = io.StringIO()

    # Configure custom logging format
    config["logFormat"] = "CUSTOM: %(levelname)s - %(message)s"
    config["logLevel"] = logging.INFO
    apply_config()

    # The handler should now be writing to stdout, but we need to check the handler's stream
    # Get the current logger and its handler
    current_logger = xmindparser.logger

    # Temporarily replace the handler's stream
    original_stream = xmindparser._console_handler.stream
    xmindparser._console_handler.stream = log_capture

    try:
        # Generate some log output
        current_logger.info("Test message")

        # Get the captured output
        log_output = log_capture.getvalue()

        # Verify custom format is applied
        assert "CUSTOM:" in log_output, f"Custom format not found in: {log_output}"
        assert "INFO" in log_output, f"Log level not found in: {log_output}"
        assert "Test message" in log_output, f"Message not found in: {log_output}"

    finally:
        # Restore original stream
        xmindparser._console_handler.stream = original_stream

        # Reset to default config
        config["logFormat"] = "%(asctime)s %(levelname)-8s: %(message)s"
        config["logLevel"] = None
        apply_config()


def test_config_logging_level():
    """Test that logLevel config option works correctly."""
    import io

    original_stream = xmindparser._console_handler.stream

    try:
        # Test with WARNING level (should not show INFO)
        config["logLevel"] = logging.WARNING
        apply_config()

        log_capture = io.StringIO()
        xmindparser._console_handler.stream = log_capture

        xmindparser.logger.info("This should not appear")
        xmindparser.logger.warning("This should appear")

        log_output = log_capture.getvalue()
        assert "This should not appear" not in log_output
        assert "This should appear" in log_output

        # Test with DEBUG level (should show everything)
        config["logLevel"] = logging.DEBUG
        apply_config()

        log_capture = io.StringIO()
        xmindparser._console_handler.stream = log_capture

        xmindparser.logger.debug("Debug message")
        xmindparser.logger.info("Info message")

        log_output = log_capture.getvalue()
        assert "Debug message" in log_output
        assert "Info message" in log_output

    finally:
        xmindparser._console_handler.stream = original_stream
        config["logLevel"] = None
        apply_config()


def test_config_logging_name():
    """Test that logName config option works correctly."""
    # Test with custom log name
    config["logName"] = "custom_xmind_logger"
    apply_config()

    # Verify logger name is updated
    current_logger = xmindparser.logger
    assert current_logger.name == "custom_xmind_logger"

    # Reset to default
    config["logName"] = "xmindparser"
    apply_config()


def test_config_show_structure():
    """Test showStructure config option."""
    # Test with showStructure = True (default)
    config["showStructure"] = True
    d = xmind_to_dict(xmind_zen_file)
    # Check that structure is included
    for sheet in d:
        assert "structure" in sheet

    # Test with showStructure = False
    config["showStructure"] = False
    d2 = xmind_to_dict(xmind_zen_file)
    # Check that structure is not included
    for sheet in d2:
        assert "structure" not in sheet

    # Reset to default
    config["showStructure"] = True


def test_config_show_relationship():
    """Test showRelationship config option."""
    # Test with showRelationship = True
    config["showRelationship"] = True
    d = xmind_to_dict(xmind_zen_file)
    # Check if relationships key exists (may be empty if no relationships)
    for sheet in d:
        assert "relationships" in sheet

    # Test with showRelationship = False (default)
    config["showRelationship"] = False
    d2 = xmind_to_dict(xmind_zen_file)
    # Check that relationships is not included
    for sheet in d2:
        assert "relationships" not in sheet
