# For Developers

## Publish New Version

This project uses GitHub Actions to automatically publish to PyPI when a new version tag is pushed.

1. Update version in [`setup.py`](setup.py:42) and [`CHANGELOG.md`](CHANGELOG.md)
2. Commit and push changes to GitHub
3. Create and push a new version tag:
   ```shell
   git tag v1.1.0
   git push origin v1.1.0
   ```
4. GitHub Actions will automatically:
   - Run tests on Python 3.9-3.13
   - Build and publish to PyPI
   - Create GitHub Release with source distribution

**Note:** Requires `PYPI_API_TOKEN` secret to be configured in repository settings.
