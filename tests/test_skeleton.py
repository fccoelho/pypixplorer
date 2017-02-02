#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pypixplore.skeleton import *
import logging

__author__ = "Flavio C. Coelho"
__copyright__ = "Flavio C. Coelho"
__license__ = "none"


def test_parse_args_without_args():
    args = parse_args([])
    assert isinstance(vars(args), dict)
    assert len(vars(args)) > 0

def test_main():
    args = parse_args(['-r', 'pip'])
    assert main(args) is None



def test_parse_args_releases():
    args = parse_args(['-i', 'pip'])
    assert len(vars(args)) > 0

def test_git_get_stats():
    args = parse_args(['-ggs', 'forks', 'ARCCSSive'])
    assert len(vars(args)) > 0


def test_parse_args_list_packages():
    args = parse_args(['-l'])
    assert len(vars(args)) > 0


def test_parse_args_downloads():
    args = parse_args(['-d progressbar2'])
    assert args.downloads is not None


def test_parse_args_get_dependencies():
    args = parse_args(['-D pip'])
    assert len(vars(args)) > 0


def test_parse_args_dependency_graph():
    args = parse_args(['-t pip'])
    assert len(vars(args)) > 0


def test_parse_args_order_releases():
    args = parse_args(['-o', '20', '20', '20'])
    assert args.order_releases is not None


def test_setup_logging():
    setup_logging(logging.DEBUG)
    assert True


def test_main():
    args = ['-l']
    main(args)
    args = ['-r', 'pysus']
    main(args)
