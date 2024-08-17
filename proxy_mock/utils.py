import json
import time
from functools import wraps

from flask import Response
from flask import current_app
from flask import request

from proxy_mock.models import InputRequestSchema


def get_request_data(func):
    """
    Декоратор для сохранения параметров текущего вызова
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Забираем параметры тел текущего запроса
        if request.is_json:
            request_body = request.get_json(silent=True)
            request_body = request_body or dict()
        elif request.data:
            try:
                data = request.data.decode()
                request_body = json.loads(data)
            except (UnicodeDecodeError, json.JSONDecodeError):
                request_body = str(request.data)
        else:
            request_body = None

        # Забираем параметры заголовков текущего запроса
        request_headers = {header: value for header, value in request.headers.items()}

        request_data = json.loads(
            InputRequestSchema(
                request_body=request_body,
                request_headers=request_headers,
                request_path=request.path,
            ).model_dump_json()
        )

        # Вызываем обработчик и передаем туда данные вызова
        result = func(*args, request_data)

        # Возвращаем результат, который вернул обработчик
        return result

    return wrapper


def log_request(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        duration = round((time.time() - start_time) * 1000, 1)
        data = {
            "method": request.method,
            "path": request.full_path.strip('?'),
            "body": request.get_json(silent=True) or {},
            "status": response.status_code if isinstance(response, Response) else response[1],
            "latency": duration,
        }
        current_app.logger.info(json.dumps(data))
        return response

    return wrapper


def is_integer(value: str) -> bool:
    """Является ли значение целым числом"""
    try:
        int(value)
        return True
    except ValueError:
        return False