import pickle
from typing import Any

from yarl import URL

from client.route import Route
from client.service_endpoints import Endpoints


class ProxyMock(Route):

    def get_status(self):
        """Cтатус приложения."""
        return super().execute_request_and_get_response_body("GET", Endpoints.status)

    def configure_mock(
        self,
        path: str,
        body: Any = None,
        headers: dict | None = None,
        status_code: int | None = None,
        extra_info: dict | None = None,
        proxy_host: str | None = None,
        timeout: float | None = None,
        **kwargs,
    ):
        """Конфигурация запроса в прокси-моке.

        :param path: Путь мока
        :param body: Тело ответа мока
        :param headers: Заголовки ответа мока
        :param extra_info: Дополнительная инфа
        :param status_code: Код ответа мока
        :param proxy_host: URL-адрес внешнего хоста
        :param timeout: Ожидание в секундах перед тем, как вернуть ответ.
        :return: Ответ в формате json
        """
        mock_data = {
            **{"body": body},
            **({"status_code": status_code} if status_code else {}),
            **({"headers": headers} if headers else {}),
        }
        request_data = {
            "path": path,
            **({"mock_data": mock_data} if mock_data else {}),
            **({"extra_info": extra_info} if extra_info else {}),
            **({"proxy_host": proxy_host} if proxy_host else {}),
            **({"timeout": timeout} if timeout else {}),
            **kwargs,
        }

        return super().execute_request_and_get_response_body("POST", Endpoints.configure_mock, request_data)

    def configure_binary_mock(
        self,
        path: str,
        body: bytes | None = None,
        headers: dict | None = None,
        status_code: int | None = None,
        extra_info: dict | None = None,
        proxy_host: str | None = None,
        timeout: float | None = None,
        **kwargs,
    ):
        """Конфигурация бинарного запроса в прокси-моке.

        :param path: Путь мока
        :param body: Тело ответа мока
        :param headers: Заголовки ответа мока
        :param extra_info: Дополнительная инфа
        :param status_code: Код ответа мока
        :param proxy_host: URL-адрес внешнего хоста
        :param timeout: Ожидание в секундах перед тем, как вернуть ответ.
        :return: Ответ в формате json
        """
        mock_data = {
            **({"body": body} if body else {}),
            **({"status_code": status_code} if status_code else {}),
            **({"headers": headers} if headers else {}),
        }
        request_data = {
            "path": path,
            **({"mock_data": mock_data} if mock_data else {}),
            **({"extra_info": extra_info} if extra_info else {}),
            **({"proxy_host": proxy_host} if proxy_host else {}),
            **({"timeout": timeout} if timeout else {}),
            **kwargs,
        }
        request_data = pickle.dumps(request_data)

        return super().execute_request_and_get_response_body(
            "POST", Endpoints.configure_mock_binary, data=request_data
        )

    def get_traffic(self):
        """Вывод параметров мока.

        :param service: Имя сервиса
        :return: Ответ в формате json
        """
        return super().execute_request_and_get_response_body("GET", Endpoints.traffic)

    def get_storage(self, path: str | None = None):
        """Вывод хранилища моков.

        :param path: Путь мока
        :return: Ответ в формате json
        """
        query_params = {**({"path": path} if path else {})}
        full_path = URL().with_path(Endpoints.storage).with_query(query_params).human_repr()

        return super().execute_request_and_get_response_body("GET", full_path)

    def clean_storage(self, path: str | None = None):
        """Очистка моков.

        :param path: Путь мока
        :return: Ответ в формате json
        """
        query_params = {**({"path": path} if path else {})}
        full_path = URL().with_path(Endpoints.storage_clean).with_query(query_params).human_repr()

        return super().execute_request_and_get_response_body("POST", full_path)

    def clean_traffic(self):
        """Очистка параметров запросов.

        :param service: Имя сервиса
        :return: Ответ в формате json
        """
        return super().execute_request_and_get_response_body("POST", Endpoints.traffic_clean)
