from btmonitor.config import setup_logging
from unittest.mock import patch


def test_default_logging():
    with patch('logging.basicConfig') as basic, patch(
        'logging.config.fileConfig'
    ) as file:
        setup_logging()
        basic.assert_called_once()
        file.assert_not_called()


def test_file_logging():
    with patch('logging.basicConfig') as basic, patch(
        'logging.config.fileConfig'
    ) as file, patch('os.path.exists', return_value=True):
        setup_logging()
        file.assert_called_with('logging.ini')
        basic.assert_not_called()


def test_conf_file_logging():
    with patch('logging.basicConfig') as basic, patch(
        'logging.config.fileConfig'
    ) as file, patch('os.path.exists', return_value=True), patch(
        'os.getenv', return_value='logging.cfg'
    ):
        setup_logging()
        file.assert_called_with('logging.cfg')
        basic.assert_not_called()
