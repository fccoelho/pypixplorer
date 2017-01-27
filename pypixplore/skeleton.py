#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        nargs=1,
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
        '-t',
        '--dependency-tree',
        nargs=1,
        dest="tree",
        help="Returns the dependencies of a given package in a tree graph (up to the 2nd level)",
    )
    parser.add_argument(
        '-d',
        '--downloads',
        nargs=1,
        dest="downloads",
        help="Return a package number of recent downloads",
    )
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO
    )
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG
    )
    parser.add_argument(
        '-rs',
        '--release_series',
        nargs=1,
        dest="release_series",
        help="Return the 10 most recent releases of the package"
    )
    parser.add_argument(
        '-d',
        '--dependencies',
        nargs=1,
        dest="pkg_dependencies",
        help="Returns the direct dependencies of a given package and their versions",
    )

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
    """Main entry point allowing external call releasess

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
    elif args.downloads is not None:
        pprint(ind.get_downloads(package_name=args.downloads[0]))
    elif args.info is not None:
        results = ind.package_info(pkgn=args.info[0])
        print("Name: {} \nDescription: {}".format(*results))
    elif args.tree is not None:
        print('{}\n(note: only two levels shown)'.format(ip.dependency_graph(package_name=args.tree[0])))
    elif args.release_series is not None:
        pprint(ind.release_series(package_name=args.release_series[0]))
    elif args.pkg_dependencies is not None:
        dep_dict = ip.get_dependencies(package_name=args.pkg_dependencies[0])
        print("PACKAGE: {}\nINSTALLED VERSION: {}".format(str(args.pkg_dependencies[0]).upper(), str(dep_dict[args.pkg_dependencies[0]])))
        print("\nDEPENDENCIES:")
        row = "{:<20}" * 3
        print(row.format("", "Installed Version", "Required Version"))
        for dependency in dep_dict['dependencies']:
            print(row.format(dependency, str(dep_dict['dependencies'][dependency]['installed_version']), str(dep_dict['dependencies'][dependency]['required_version'])))

    _logger.info("Done")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
