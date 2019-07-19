#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `btmonitor` package."""
import os

import pytest

from .auth import read_key
from btmonitor import main
from click.testing import CliRunner


@pytest.fixture()
def private_key():
    return read_key("test.key")


def test_cli():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(main.main)
    assert result.exit_code == 0
    assert 'us traffic monitor commands' in result.output
    help_result = runner.invoke(main.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_cli_token(private_key):
    """Test the token command."""
    runner = CliRunner()
    result = runner.invoke(main.main, args=["token"])
    # Key expected
    assert result.exit_code == 1
    result = runner.invoke(main.main, args=["token", "-p", private_key])
    assert result.exit_code == 0
    assert result.output.count(".") == 2


def test_cli_token_file():
    """Test the token command."""
    runner = CliRunner()
    path = os.path.dirname(os.path.abspath(__file__))
    key_file = os.path.join(path, "auth", "test.key")
    result = runner.invoke(main.main, args=["token", "-f", key_file])
    assert result.exit_code == 0
