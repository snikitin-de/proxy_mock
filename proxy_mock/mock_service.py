import copy
import logging

import requests
from flask import Request
from yarl import URL

from proxy_mock.storage import STORAGE
from proxy_mock.utils import is_integer

logger = logging.getLogger(__name__)


def path_finder(path: str) -> str | None:
    """Подбирает ручку в хранилище"""
    # Удаляем начальные и конечные слеши, если они есть
    path = path.strip("/")

    # Проверяем, есть ли путь в хранилище
    mock_params = STORAGE.get_response(path)
    if mock_params:
        return path

    # Если нет, пытаемся найти путь, отрезая численные части
    new_path = "/".join(part for part in path.split("/") if not is_integer(part) and part)
    new_path = new_path.strip("/")

    # Проверяем, есть ли новый путь в хранилище
    mock_params = STORAGE.get_response(new_path)
    if mock_params:
        return new_path

    # Полагаем, что ничего не найдено
    return None


def find_response(path: str) -> dict | None:
    """Ищет ручку в хранилище"""
    if new_path := path_finder(path):
        return STORAGE.get_response(new_path)

    return None


def create_response(**kwargs) -> dict:
    """Записывает ручку в хранилище"""
    return STORAGE.set_response(**kwargs)


def cleanup_storage() -> bool:
    """Очищает хранилище"""
    return STORAGE.clear_storage()


def delete_mock(path: str) -> bool:
    """Удаляет мок из хранилища"""
    if new_path := path_finder(path):
        return STORAGE.delete_mock_from_storage(new_path)

    return False


def return_storage() -> dict:
    """Выводит хранилище"""
    storage = copy.deepcopy(STORAGE.get_storage())
    for mock in storage.values():
        if isinstance(mock["mock_data"]["body"], bytes):
            mock["mock_data"]["body"] = str(mock["mock_data"]["body"])

    return storage


def make_proxy_request_url(request_url: str, proxy_host: str) -> str:
    """Сборка URL для проксирования запроса на заданный хост."""
    request_url = URL(request_url)
    proxy_url = URL(proxy_host).with_path(request_url.path).with_query(request_url.query)

    return proxy_url.human_repr()


def proxy_request_to_host(request_data: Request, proxy_host: str) -> requests.Response:
    """Проксирует запрос на заданный хост."""
    request_url = make_proxy_request_url(request_data.url, proxy_host)
    response = requests.request(
        method=request_data.method,
        url=request_url,
        data=request_data.data,
        headers=dict(request_data.headers),
        allow_redirects=False,
    )
    return response
