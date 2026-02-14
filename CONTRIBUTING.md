# Contributing to xmindparser

Thank you for your interest in contributing to xmindparser! This document provides guidelines and instructions for contributing.

## Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/tobyqin/xmindparser.git
cd xmindparser
```

### 2. Install development dependencies

```bash
pip install -r requirements-dev.txt
```

### 3. Install pre-commit hooks

```bash
pre-commit install
```

This will automatically run linters and formatters before each commit.

## Code Quality

We use several tools to maintain code quality:

### Black (Code Formatter)

Black is used for consistent code formatting with a line length of 120 characters.

```bash
# Check formatting
black --check xmindparser tests

# Auto-format code
black xmindparser tests
```

### isort (Import Sorter)

isort organizes imports in a consistent manner.

```bash
# Check import sorting
isort --check-only xmindparser tests

# Auto-sort imports
isort xmindparser tests
```

### flake8 (Linter)

flake8 checks for code style and potential errors.

```bash
# Run linter
flake8 xmindparser tests
```

### Running All Checks

```bash
# Run all linting checks
black --check xmindparser tests && \
isort --check-only xmindparser tests && \
flake8 xmindparser tests
```

## Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_xmindparser.py -v

# Run with coverage
pytest tests/ --cov=xmindparser --cov-report=html
```

### Test Coverage

We aim for high test coverage. Please add tests for any new features or bug fixes.

## Pull Request Process

1. **Fork the repository** and create your branch from `master`
2. **Make your changes** following the code style guidelines
3. **Add tests** for any new functionality
4. **Run all tests** to ensure they pass
5. **Run linters** to ensure code quality
6. **Update documentation** if needed (README.md, CHANGELOG.md)
7. **Submit a pull request** with a clear description of changes

### PR Checklist

- [ ] Code follows the project's style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated with changes
- [ ] Commit messages are clear and descriptive

## Code Style Guidelines

- **Line length**: Maximum 120 characters
- **Imports**: Organized using isort (stdlib, third-party, local)
- **Formatting**: Use Black for consistent formatting
- **Docstrings**: Use clear, concise docstrings for functions and classes
- **Type hints**: Encouraged but not required
- **Comments**: Write clear comments for complex logic

## Commit Message Guidelines

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable (e.g., "Fix #123")
- Keep the first line under 72 characters
- Add detailed description in the body if needed

Example:

```
Fix config system to support dynamic logger reconfiguration

- Add apply_config() function
- Update documentation with usage examples
- Add comprehensive tests for config options

Fixes #123
```

## Release Process

1. Update version in `setup.py`
2. Update `CHANGELOG.md` with changes
3. Commit changes: `git commit -m "Release vX.Y.Z"`
4. Create tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
5. Push changes: `git push origin master --tags`
6. Create GitHub release from tag

## Questions?

If you have questions or need help, please:

- Open an issue on GitHub
- Check existing issues and documentation
- Contact the maintainers

Thank you for contributing! 🎉
