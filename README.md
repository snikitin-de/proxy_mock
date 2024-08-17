# Proxy Mock

Сервис-прокси и одновременно мок-сервер для определенных (сконфигурированных заранее) эндпоинтов

## Начало работы

### Предварительные требования
- Python >= 3.9
- Poetry ^1.8.x

### Установка и локальный запуск

Установить виртуальное окружение с зависимостями:
```
poetry install --no-root
```

Активировать виртуальное окружение
```
poetry shell
```

Запустить сервис:
```
make run
```

### Запуск в Docker

Билд образа:
```
make docker_run
```

Сервис будет доступен по адресу `http://localhost:5000`.


# API


### 1. `/status` (GET)

### Проверка доступности сервера прокси-мока

- URL: `/status`
- Метод: `GET`

#### Ответ:
- Код ответа: `200 (OK)`
- Тип контента: `application/json`
- Тело:
```json
{
    "success": true,
    "version": ""
}
```


### 2. `/configure` (POST)

### Конфигурация мок-запроса в прокси-моке

- URL: `/configure`
- Метод: `POST`
- Тип контента: `application/json`

### Тело запроса:

JSON:
- body: `str | dict | list | bool`
- path*: `str`
- service: `str`
- status: `int`
- proxy_host: `str`

Пример:
```json
{
    "body": {
        "key": "value"
    },
    "path": "/path",
    "service": "service",
    "status": 302,
    "proxy_host": "http://other.host.ru"
}
```

### Ответ:

#### Успешный:
- Код ответа: `200 (OK)`
- Тип контента: `application/json`
- Тело:
```json
{
    "success": true
}
```

#### Неуспешный:
- Код ответа: `400 (BAD REQUEST)`
- Тип контента: `application/json`
- Тело:
```json
{
    "success": false,
    "error": "Parameter 'path' is always required"
}
```


### 3. `/configure/binary` (POST)

### Конфигурация мок-запроса с бинарным содержимым в прокси-моке

- URL: `/configure/binary`
- Метод: `POST`
- Тип контента: `application/protobuf`
- Query-параметры:
    - path*: `str`
    - service: `str`
    - status: `int`
    - proxy_host: `str`

### Тело запроса:

BYTES object

Пример:
```bytes
b'\xd0\xa2\xd0\xb5\xd1\x81\xd1\x82\xd0\\xba\xd1\x80\xd1\x83\xd1\x82\xd0\xbe!'
```

### Ответ:

#### Успешный:
- Код ответа: `200 (OK)`
- Тип контента: `application/json`
- Тело:
```json
{
    "success": true
}
```

#### Неуспешный:
- Код ответа: `400 (BAD REQUEST)`
- Тип контента: `application/json`
- Тело:
```json
{
    "success": false,
    "error": "Parameter 'path' is always required"
}
```


### 4. `/cleanup_params` (POST)

### Очистка хранилища параметров запросов

- URL: `/cleanup_params`
- Метод: POST
- Query-параметры:
    - service: `str`

### Ответ:

#### Успешный:
- Код ответа: `200 (OK)`
- Тип контента: `application/json`
- Тело:
```json
{
    "success": true
}
```

#### Неуспешный:
- Код ответа: `404 (Not Found)`
- Тип контента: `application/json`
- Тело:
```json
{
    "success": false
}
```


### 5. `/cleanup_storage` (POST)

### Очистка хранилища моков

- URL: `/cleanup_storage`
- Метод: POST
- Query-параметры:
    - path: `str`

### Ответ:

#### Успешный:
- Код ответа: `200 (OK)`
- Тип контента: `application/json`
- Тело:
```json
{
    "success": true
}
```

#### Неуспешный:
- Код ответа: `404 (Not Found)`
- Тип контента: `application/json`
- Тело:
```json
{
    "success": false
}
```


### 6. `/storage` (GET)

### Вывод хранилища моков

- URL: `/storage`
- Метод: GET
- Query-параметры:
    - path: `str`

### Ответ:

#### Успешный:
- Код ответа: `200 (OK)`
- Тип контента: `application/json`
- Тело:
```json
{
    "data": {
        "body": "ok",
        "service": "proxy_mock",
        "status": 200
    },
    "success": true
}
```

#### Неуспешный:
- Код ответа: `404 (Not Found)`
- Тип контента: `application/json`
- Тело:
```json
{
    "data": {},
    "success": false
}
```


### 7. `/mock_params` (GET)

### Вывод хранилища параметров запросов

- URL: `/storage`
- Метод: GET
- Query-параметры:
    - service: `str`

### Ответ:

#### Успешный:
- Код ответа: `200 (OK)`
- Тип контента: `application/json`
- Тело:
```json
{
    "proxy_mock": [
        {}
    ]
}
```

#### Неуспешный:
- Код ответа: `404 (Not Found)`
- Тип контента: `application/json`
- Тело:
```json
[]
```


### 8. `/<path:path>` (GET и POST)

### Перехват всех остальных запросов

- URL: `/<path:path>`
- Метод: GET или POST

### Ответ:

#### Если подготовленный ответ не найден:
    
- Код ответа: `404 (NOT FOUND)`
- Тип контента: `application/json`
- Тело:
```json
{
    "error": "Не найден мок /mock_path"
}
```

#### Если подготовленный ответ найден:

#### Если есть проксирующий хост (`not null`):
- Код ответа: `Код состояния ответа от внешнего хоста`
- Тип контента: `Тип контента ответа от внешнего хоста`
- Тело: `Тело ответа от внешнего хоста`

#### Если нет проксирующего хоста:
- Код ответа: `Подготовленный код ответа`
- Тип контента: `application/json` или `text/html; charset=utf-8`
- Тело: `Подготовленные данные ответа`
