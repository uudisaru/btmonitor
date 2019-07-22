#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `btmonitor` package."""
from .auth import read_key
from btmonitor import main
from click.testing import CliRunner

import pytest


@pytest.fixture()
def private_key():
    return read_key('test.key')


def test_cli():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(main.main)
    assert result.exit_code == 0
    assert 'us traffic monitor commands' in result.output
    help_result = runner.invoke(main.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
