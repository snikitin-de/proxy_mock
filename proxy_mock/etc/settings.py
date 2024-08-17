import logging
from pathlib import Path

import toml

BASE_DIR = Path(__file__).resolve().parent
config_path = BASE_DIR.joinpath("config.toml")
config = toml.load(config_path)


class Config:
    DEBUG = config.get("DEBUG", True)


def configure_logger(app):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    for handler in gunicorn_logger.handlers:
        handler.setFormatter(formatter)
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel("DEBUG")


def get_version_from_pyproject(app):
    """Извлекает версию приложения из файла pyproject.toml."""
    with open('pyproject.toml', 'r') as file:
        pyproject_data = toml.load(file)
    app.logger.info(f"Proxy Mock version: {pyproject_data['tool']['poetry']['version']}")
    return pyproject_data['tool']['poetry']['version']
