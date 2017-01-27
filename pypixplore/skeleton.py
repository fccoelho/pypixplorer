#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.cfg:

    console_scripts =
     fibonacci = pypixplore.skeleton:run

Then run `python setup.py install` which will install the command `ppxplore`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging

from pypixplore import __version__
from pypixplore.local import InstalledPackages
from pypixplore.remote import Index
from pprint import pprint

__author__ = "Flavio C. Coelho"
__copyright__ = "Flavio C. Coelho"
__license__ = 'GPL v3'

_logger = logging.getLogger(__name__)



def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Copyright (C) 2017 Flavio C. Coelho\nThis program comes with ABSOLUTELY NO WARRANTY;\nThis is free software, and you are welcome to redistribute it under certain conditions;\nFor details access: https://www.gnu.org/licenses/gpl-3.0.en.html\nExplore Python Package Index")
    parser.add_argument(
        '--version',
        action='version',
        version='pypixplore {ver}'.format(ver=__version__)
    )
    parser.add_argument(
        '-s',
        '--status',
        dest="name",
        help="Show Status for a given package.",
        type=str,
    )
    parser.add_argument(
        '-l',
        '--list',
        action='store_true',
        help="List installed packages",
    )
    parser.add_argument(
        '-r',
        '--releases',
        nargs=1,
        dest="releases",
        help="List package latest release",
    )
    parser.add_argument(
        '-i',
        '--info',
        nargs=1,
        dest="info",
        help="Shows package info",
    )

    parser.add_argument(
        '-p',
        '--popularity',
        nargs=1,
        dest="popularity",
        help="Return the popularity of a package as the number of recent downloads",
    )
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)

    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)

    parser.add_argument(
        '-pg',
        '--python-graphics',
        help="Return a graph with the numbers of packages that run on Python 2x.x and Python 3.x.x")
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external callreleasess

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting Analysis...")
    ip = InstalledPackages()
    ind = Index()
    if args.list:
        pprint(ip.list_installed())
    elif args.releases is not None:
        pprint(ind.get_latest_releases(package_name=args.releases[0]))
    elif args.popularity is not None:
        pprint(ind.get_popularity(package_name=args.popularity[0]))
    elif args.info is not None:
        results = ind.package_info(pkgn=args.info[0])
        print("Name: {} \nDescription: {}".format(*results))
    elif args.python-graphics is not None:
        pprint(ind.how_many_packages_version_py())
    _logger.info("Done")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
