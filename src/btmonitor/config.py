import logging.config
import os


def setup_logging(
    default_path: str = 'logging.ini',
    default_level: int = logging.INFO,
    env_key: str = 'LOG_CFG',
) -> None:
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        logging.config.fileConfig(path)
    else:
        logging.basicConfig(
            format='%(asctime)-15s - %(name)s - %(levelname)s - %(message)s',
            level=default_level,
        )
