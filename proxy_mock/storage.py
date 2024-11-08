from proxy_mock.models import MockDataSchema
from proxy_mock.models import MockPathSchema
from proxy_mock.utils import get_dict_hash

import json
import os

class MockStorage:
    storage_path = 'storage.json'

    def __init__(self) -> None:
        self._storage = {}

        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as fp:
                    file_storage = json.loads(fp.read())

                    if len(file_storage):
                        self._storage = file_storage
        except OSError as exOS:
            print("OS error: " + str(exOS))
        except Exception as ex:
            print(ex)

    def set_mock_data(
        self,
        path: str,
        mock_data: dict,
        extra_info: dict,
        proxy_host: str | None,
        timeout: float,
    ) -> dict:
        """Записать мок для ручки в хранилище"""
        key = json.dumps({
            'path': path,
            'request_params_hash': get_dict_hash(mock_data.get('request_params')),
            'request_body_hash': get_dict_hash(mock_data.get('request_body')),
            'request_form_hash': get_dict_hash(mock_data.get('request_form'))
        }, sort_keys=True)

        self._storage[key] = MockPathSchema(
            mock_data=MockDataSchema(**mock_data).model_dump(),
            extra_info=extra_info,
            proxy_host=proxy_host,
            timeout=timeout,
        ).model_dump()

        try:
            with open('storage.json', 'w') as fp:
                fp.write(json.dumps(self._storage, indent=4))
        except OSError as exOS:
            print("OS error: " + str(exOS))
        except Exception as ex:
            print(ex)

        return self._storage[key]

    def get_mock_data(self, path: str, mock_data: dict = None) -> dict | None:
        """Достать подготовленный ответ"""

        if mock_data:
            request_params_hash = get_dict_hash(mock_data['request_params'])
            request_body_hash = get_dict_hash(mock_data['request_body'])
            request_form_hash = get_dict_hash(mock_data['request_form'])

            for key in self._storage.keys():
                key_json = json.loads(key)
                mock_path = key_json['path']
                mock_request_params_hash = key_json['request_params_hash']
                mock_request_body_hash = key_json['request_body_hash']
                mock_request_form_hash = key_json['request_form_hash']

                if mock_path == path:
                    if ((mock_request_params_hash == request_params_hash and mock_request_params_hash is not None) or
                        (mock_request_body_hash == request_body_hash and mock_request_body_hash is not None) or
                        (mock_request_form_hash == request_form_hash and mock_request_form_hash is not None)):
                        return self._storage.get(key)

        return None

    def get_storage(self) -> dict:
        """Вывод хранилища моков"""
        return self._storage

    def clean_storage(self) -> bool:
        """Очистка хранилища моков"""
        self._storage = {}
        return True

    def delete_mock_data(self, path: str) -> bool:
        """Удаляет мок из хранилища"""
        return True if self._storage.pop(path, None) else False


mock_storage = MockStorage()
