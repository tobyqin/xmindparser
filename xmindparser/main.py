"""
A tool to parse xmind file into programmable data types.
Check https://github.com/tobyqin/xmindparser to see supported types.

Usage:
 xmindparser [path_to_xmind_file] -[type]

Example:
 xmindparser C:\\tests\\my.xmind -json
 xmindparser C:\\tests\\my.xmind -xml

"""

import sys

from xmindparser import *


def main():
    if len(sys.argv) == 3 and sys.argv[1].endswith('.xmind'):
        xmind, out_types = sys.argv[1], sys.argv[2][1:]
        out = xmind_to_file(xmind, out_types)
        print('Generated: {}'.format(out))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
