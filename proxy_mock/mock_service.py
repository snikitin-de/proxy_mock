import copy

import requests
from flask import Request
from yarl import URL

from proxy_mock.storage import mock_storage
from proxy_mock.utils import is_integer


def find_path(path: str) -> str | None:
    """Подбирает ручку в хранилище"""
    # Удаляем начальные и конечные слеши, если они есть
    path = path.strip("/")

    # Проверяем, есть ли путь в хранилище
    mock_params = mock_storage.get_mock_data(path)
    if mock_params:
        return path

    # Если нет, пытаемся найти путь, отрезая численные части
    new_path = "/".join(part for part in path.split("/") if not is_integer(part) and part)
    new_path = new_path.strip("/")

    # Проверяем, есть ли новый путь в хранилище
    mock_params = mock_storage.get_mock_data(new_path)
    if mock_params:
        return new_path

    # Полагаем, что ничего не найдено
    return None


def find_mock_data(path: str) -> dict | None:
    """Ищет ручку в хранилище"""
    if new_path := find_path(path):
        return mock_storage.get_mock_data(new_path)

    return None


def create_mock_data(**kwargs) -> dict:
    """Записывает ручку в хранилище"""
    return mock_storage.set_mock_data(**kwargs)


def cleanup_storage() -> bool:
    """Очищает хранилище"""
    return mock_storage.clean_storage()


def delete_mock_data(path: str) -> bool:
    """Удаляет мок из хранилища"""
    if new_path := find_path(path):
        return mock_storage.delete_mock_data(new_path)

    return False


def return_storage() -> dict:
    """Выводит хранилище"""
    storage = copy.deepcopy(mock_storage.get_storage())
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
