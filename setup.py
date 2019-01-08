"""
Documentation
-------------
xmindparser is a tool to help you convert xmind file to programmable data type, e.g. json, xml.

Detail usage: https://github.com/tobyqin/xmindparser

"""
from codecs import open
from os import path

from setuptools import setup, find_packages

current_dir = path.abspath(path.dirname(__file__))
long_description = __doc__

with open(path.join(current_dir, "CHANGELOG.md"), encoding="utf-8") as f:
    long_description += "\n" + f.read()

classifiers = ["License :: OSI Approved :: MIT License",
               "Topic :: Software Development",
               "Topic :: Utilities",
               "Operating System :: Microsoft :: Windows",
               "Operating System :: MacOS :: MacOS X"] + [
                  ("Programming Language :: Python :: %s" % x) for x in "3.4 3.5 3.6 3.7 3.8".split()]


def command_line():
    target = "xmindparser.main:main"
    entry_points = []
    entry_points.append("xmindparser=%s" % target)
    return entry_points


def main():
    setup(
        name="xmindparser",
        description="Convert xmind to programmable data types, support xmind pro and xmind zen file types.",
        keywords="xmind parser converter json xml",
        long_description=long_description,
        classifiers=classifiers,
        version="1.0.5",
        author="Toby Qin",
        author_email="toby.qin@live.com",
        url="https://github.com/tobyqin/xmindparser",
        packages=find_packages(exclude=['tests', 'tests.*']),
        package_data={},
        install_requires=[],
        entry_points={"console_scripts": command_line(), },
        zip_safe=False
    )


if __name__ == "__main__":
    main()
