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


def test_parse_args_releases():
    args = parse_args(['-r', 'pandas'])
    assert len(vars(args)) > 0


def test_parse_args_list_packages():
    args = parse_args(['-l'])
    assert len(vars(args)) > 0


def test_parse_args_downloads():
    args = parse_args(['-d progressbar2'])
    assert args.downloads is not None

def test_parse_args_rank_releases():
    args = parse_args(['-Rr 20 20 20'])
    assert args.rank_releases is not None

def test_setup_logging():
    setup_logging(logging.DEBUG)
    assert True

def test_main():
    args = ['-l']
    main(args)
    args = ['-r', 'pysus']
    main(args)