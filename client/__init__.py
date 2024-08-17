import json

import requests


class Route():

    def __init__(self, host: str) -> None:
        """host - URL адрес прокси-мока."""
        self.host = host

    def __get_proxy_url(self, command: str):
        """Сборка URL для прокси-мока."""
        command = command.strip('/')
        base_url = self.host.rstrip('/')
        return f'{base_url}/{command}'

    @staticmethod
    def __make_request(
        req_type,
        url,
        params=None,
        data=None,
        json=None,
        headers=None,
        **kwargs,
    ):
        """Сборка запроса."""
        try:
            return requests.request(
                method=req_type,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                **kwargs,
            )

        except (requests.HTTPError, requests.ConnectionError) as err:
            assert False, f"Proxy-mock request error:\n{err}"

    @staticmethod
    def __get_response(response: requests.Response) -> dict | str | list | bytes:
        """
        Получение ответа.

        :param response: объект ответа на запрос
        :return: str, dict, list, bytes возвращает ответ
        """
        if response.content:
            try:
                if "json" in response.headers["Content-Type"]:
                    return response.json()
                elif "text" in response.headers["Content-Type"]:
                    return response.text
                else:
                    return response.content
            except json.JSONDecodeError:
                return response.text
        else:
            return None

    def execute_request(self, req_type: str, route: str, **kwargs):
        """Выполнение запроса и вывод простого ответа."""
        url = self.__get_proxy_url(route)
        return self.__make_request(req_type=req_type, url=url, **kwargs)

    def execute_request_and_get_response_body(self, req_type: str, route: str, json: dict = None, **kwargs):
        """Выполнение запроса и вывод ответа."""
        response = self.execute_request(req_type=req_type, route=route, json=json, **kwargs)
        return self.__get_response(response)
