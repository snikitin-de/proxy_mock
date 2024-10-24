import json
import hashlib
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

        # Получаем параметры запроса
        key_req = request.args.keys()
        request_params = {}

        for key in key_req:
            request_params[key] = request.args.get(key)

        # Получаем данные формы
        request_form = {}

        for key in request.form:
            request_form[key] = request.form[key]

        request_data = json.loads(
            InputRequestSchema(
                request_body=request_body,
                request_headers=request_headers,
                request_form=request_form,
                request_path=request.path,
                request_params=request_params,
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
        duration = round((time.time() - start_time) * 1000, 2)
        data = {
            "method": request.method,
            "path": request.full_path.strip('?'),
            "body": request.get_json(silent=True) or {},
            "status": response.status_code if isinstance(response, Response) else response[1],
            "latency": f"{duration}ms",
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


def get_dict_hash(dictionary: dict | None):
    if dictionary not in ({}, None):
        return hashlib.md5(json.dumps(dictionary, sort_keys=True).encode('utf-8')).hexdigest()

    return None