#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main module."""

import sys
import fire
from vimanga.cli import find


class ViManga(object):
    """Parse object run cli mode"""
    def __init__(self):
        self.find = find

    def cli(self):
        """Cli interface"""
        sys.stderr.write('Cli interface is a future feature')
        return self

    def interface(self):
        """Window interface"""
        sys.stderr.write('Window interface is a future feature')
        return self


def main():
    """Entry point"""
    fire.Fire(ViManga())


if __name__ == '__main__':
    main()
