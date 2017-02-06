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
        '-l',
        '--list',
        action='store_true',
        help="List installed packages",
    )
    parser.add_argument(
        '-r',
        '--releases',
        nargs=1,
        metavar="<package_name>",
        dest="releases",
        help="List package latest release",
    )
    parser.add_argument(
        '-i',
        '--info',
        nargs=1,
        metavar = "<package_name>",
        dest="info",
        help="Shows package info",
    )
    parser.add_argument(
        '-t',
        '--dependency-tree',
        nargs=1,
        metavar="<package_name>",
        dest="tree",
        help="Returns the dependencies of a given package in a tree graph (up to the 2nd level)",
    )
    parser.add_argument(
        '-d',
        '--downloads',
        nargs=1,
        metavar="<package_name>",
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
        const=logging.DEBUG)

    parser.add_argument(
        '-R',
        '--release_series',
        nargs=1,
        metavar="<package_name>",
        dest="release_series",
        help="Return the 10 most recent releases of the package"
    )
    parser.add_argument(
        '-ggs',
        '--get_git_stats',
        nargs=2,
        dest="get_git_stats",
        metavar = ['<forks|watchers|stars>', '<package name>'],
        help="Get specified git stats. Arg 1 can be ['forks', 'watchers', 'stars']. Arg 2 is the package name")

    parser.add_argument(
        '-o',
        '--order-releases',
        dest="order_releases",
        type=int,
        nargs=3,
        metavar=["days", "#packages", "size"],
        help="""return the rank by recent releases.
        The first argument is the time in days the function will count the amount of releases.
        The second argument is the size of the list of random packages of PyPI the function will iterate,
        to iterate all packages use -None- as input
        The third argument is the amount of package of the rank the function will return,
        to get the full rank use -None- as input."""
    )

    parser.add_argument(
        '-pv',
        '--python_versions',
        nargs=1,
        metavar="<n_sample>",
        help="Return a graph with the numbers of packages that run on Python 2x.x and Python 3.x.x",
    )

    parser.add_argument(
        '-D',
        '--dependencies',
        nargs=1,
        metavar="<package_name>",
        dest="pkg_dependencies",
        help="Returns the direct dependencies of a given package and their versions",
    )

    parser.add_argument(
        '-c',
        '--count_releases',
        nargs=2,
        metavar=['<package_name>', '<period>'],
        dest="count_releases",
        help="The amount of releases a package received in the last <period> days"
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """
    Setup basic logging

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

    elif args.count_releases is not None:
        JSON = ind._get_JSON(args.count_releases[0])
        pprint(ind.count_releases(json=JSON, time_days=args.count_releases[1]))

    elif args.info is not None:
        results = ind.package_info(pkgn=args.info[0])
        print("Name: {} \nDescription: {}".format(*results))

    elif args.order_releases is not None:
        results = ind.rank_of_packages_by_recent_release(time_days = args.order_releases[0],
                                                         list_size = args.order_releases[1],
                                                         rank_size = args.order_releases[2])
        for n, package in enumerate(results):
            print("{}\t{}".format(n+1, package))

    elif args.tree is not None:
        print('{}\n(note: only two levels shown)'.format(ip.dependency_graph(package_name=args.tree[0])))

    elif args.python_versions is not None:
        result = ind.how_many_packages_version_py(n_sample=args.python_versions[0])
        pprint(ind.print_graphics(result[0], result[1]))

    elif args.release_series is not None:
        pprint(ind.release_series(package_name=args.release_series[0]))

    elif args.get_git_stats is not None:
        if ind.get_git_stats(args.get_git_stats[0], args.get_git_stats[1]) is not None:
            pprint('The {} package has {} {} on its GitHub Repo'.format(args.get_git_stats[1],
                                                                                  ind.get_git_stats(args.get_git_stats[0],
                                                                                                   args.get_git_stats[1]),
                                                                                  args.get_git_stats[0]))

    elif args.pkg_dependencies is not None:
        dep_dict = ip.get_dependencies(package_name=args.pkg_dependencies[0])
        print("PACKAGE: {}\nINSTALLED VERSION: {}".format(str(args.pkg_dependencies[0]).upper(),
                                                          str(dep_dict[args.pkg_dependencies[0]])))
        print("\nDEPENDENCIES:")
        row = "{:<20}" * 3
        print(row.format("", "Installed Version", "Required Version"))
        for dependency in dep_dict['dependencies']:
            print(row.format(dependency, str(dep_dict['dependencies'][dependency]['installed_version']),
                             str(dep_dict['dependencies'][dependency]['required_version'])))


    _logger.info("Done")
def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
