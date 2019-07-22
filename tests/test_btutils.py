#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `btmonitor` package."""
from .auth import read_key
from btmonitor import btutils
from click.testing import CliRunner

import os
import pytest


@pytest.fixture()
def private_key():
    return read_key('test.key')


def test_cli_token(private_key):
    """Test the token command."""
    runner = CliRunner()
    result = runner.invoke(btutils.main, args=['token'])
    # Key expected
    assert result.exit_code == 1
    result = runner.invoke(btutils.main, args=['-k', private_key, 'token'])
    assert result.exit_code == 0
    assert result.output.count('.') == 2


def test_cli_token_file():
    """Test the token command."""
    runner = CliRunner()
    path = os.path.dirname(os.path.abspath(__file__))
    key_file = os.path.join(path, 'auth', 'test.key')
    result = runner.invoke(btutils.main, args=['-f', key_file, 'token'])
    assert result.exit_code == 0


def test_cli_encrypted():
    """Test the token command."""
    runner = CliRunner()
    path = os.path.dirname(os.path.abspath(__file__))
    key_file = os.path.join(path, 'auth', 'test.enc.key')
    result = runner.invoke(
        btutils.main, args=['-f', key_file, '-p', '1234', 'token']
    )
    assert result.exit_code == 0
