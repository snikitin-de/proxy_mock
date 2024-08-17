from copy import deepcopy

from proxy_mock.constants import MOCK_STORAGE
from proxy_mock.models import MockDataSchema
from proxy_mock.models import MockPathSchema


class MockStorage:

    def __init__(self) -> None:
        self._storage = deepcopy(MOCK_STORAGE)

    def set_response(
        self,
        path: str,
        mock_data: dict,
        extra_info: dict,
        proxy_host: str | None,
        timeout: float,
    ) -> dict:
        """Записать мок для ручки в хранилище"""
        self._storage[path] = MockPathSchema(
            mock_data=MockDataSchema(**mock_data).model_dump(),
            extra_info=extra_info,
            proxy_host=proxy_host,
            timeout=timeout,
        ).model_dump()
        return self._storage[path]

    def get_response(self, path: str) -> dict | None:
        """Достать подготовленный ответ"""
        return self._storage.get(path)

    def get_storage(self) -> dict:
        """Вывод хранилища моков"""
        return self._storage

    def clear_storage(self) -> bool:
        """Очистка хранилища моков"""
        self._storage = deepcopy(MOCK_STORAGE)
        return True

    def delete_mock_from_storage(self, path: str) -> bool:
        """Удаляет мок из хранилища"""
        return True if self._storage.pop(path, None) else False


STORAGE = MockStorage()
