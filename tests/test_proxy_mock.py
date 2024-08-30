import time
from copy import deepcopy

import pytest

from client.client import ProxyMock
from tests.constants import BYTE_RESPONSE
from tests.constants import EMPTY_BYTE_RESPONSE
from tests.constants import EXPECTED_RESPONSE
from tests.constants import EXPECTED_STATUSES
from tests.constants import INCOMPLETE_PROXY_HOST
from tests.constants import MOCK_PATHS
from tests.constants import MOCK_PATHS_PROTO
from tests.constants import PROXY_HOST_DATA
from tests.constants import TEST_CONFIGURE_BINARY_DATA
from tests.constants import TEST_CONFIGURE_DATA


def test_get_status(client: ProxyMock):
    assert client.get_status().get("success")


class TestConfigure:

    @pytest.mark.parametrize("mock_path", MOCK_PATHS)
    def test_configure_mock_by_paths(self, client: ProxyMock, mock_path):
        request_data = deepcopy(TEST_CONFIGURE_DATA)

        configure_response = client.configure_mock(mock_path, request_data["body"])
        assert configure_response.get("success"), configure_response

        test_response = client.execute_request_and_get_response_body("GET", mock_path)
        assert test_response == request_data["body"]

    @pytest.mark.parametrize("expected_response", EXPECTED_RESPONSE)
    def test_configure_mock_by_responses(self, client: ProxyMock, expected_response):
        request_data = deepcopy(TEST_CONFIGURE_DATA)

        configure_response = client.configure_mock(path=request_data["path"], body=expected_response)

        assert configure_response.get("success"), configure_response

        test_response = client.execute_request_and_get_response_body("GET", request_data["path"])
        assert test_response == expected_response

    @pytest.mark.parametrize("expected_status", EXPECTED_STATUSES)
    def test_configure_mock_by_statuses(self, client: ProxyMock, expected_status):
        request_data = deepcopy(TEST_CONFIGURE_DATA)

        configure_response = client.configure_mock(
            path=request_data["path"], body=request_data["body"], status_code=expected_status
        )

        assert configure_response.get("success"), configure_response

        test_response = client.execute_request("GET", request_data["path"])
        assert test_response.status_code == expected_status

    def test_configure_mock_by_params(self, client: ProxyMock):
        request_data = deepcopy(TEST_CONFIGURE_DATA)

        configure_response = client.configure_mock(**request_data)
        assert configure_response.get("success"), configure_response

        mock_response = client.execute_request("GET", request_data["path"])
        assert mock_response.json() == request_data["body"]
        assert mock_response.status_code == request_data["status_code"]

        request_params_response = client.get_traffic()
        assert request_params_response.get("data")
        for req_param in request_params_response["data"]:
            assert req_param["extra_info"] == request_data["extra_info"]

    def test_configure_mock_by_proxy_host(self, client: ProxyMock):
        request_data = {}
        proxy_host, path = PROXY_HOST_DATA

        request_data["proxy_host"] = proxy_host
        request_data["path"] = path

        configure_response = client.configure_mock(**request_data)
        assert configure_response.get("success"), configure_response

        mock_response = client.execute_request("GET", request_data["path"])
        assert mock_response.content
        assert mock_response.ok

    def test_configure_mock_by_timeout(self, client: ProxyMock):
        request_data = deepcopy(TEST_CONFIGURE_DATA)
        request_data["timeout"] = 0.57

        configure_response = client.configure_mock(**request_data)
        assert configure_response.get("success") is True

        start_time = time.time()
        mock_response = client.execute_request("GET", request_data["path"])
        end_time = time.time()
        elapsed_time = end_time - start_time

        assert elapsed_time >= request_data["timeout"]
        assert mock_response.json() == request_data["body"]
        assert mock_response.status_code == request_data["status_code"]

    def test_configure_with_custom_headers(self, client: ProxyMock):
        request_data = deepcopy(TEST_CONFIGURE_DATA)

        configure_response = client.configure_mock(**request_data)
        assert configure_response.get("success")

        mock_response = client.execute_request("GET", request_data["path"])

        for key, value in request_data["headers"].items():
            assert mock_response.headers[key] == value

        assert mock_response.json() == request_data["body"]
        assert mock_response.status_code == request_data["status_code"]

    def test_configure_mock_with_bad_proxy_host(self, client: ProxyMock):
        request_data = {}
        proxy_host, path = INCOMPLETE_PROXY_HOST

        request_data["proxy_host"] = proxy_host
        request_data["path"] = path

        configure_response = client.configure_mock(**request_data)
        assert not configure_response.get("success"), configure_response
        assert configure_response.get("error"), configure_response


class TestConfigureBinary:

    @pytest.mark.parametrize("mock_path", MOCK_PATHS_PROTO)
    def test_configure_binary_mock_by_paths(self, client: ProxyMock, mock_path):
        configure_response = client.configure_binary_mock(mock_path, BYTE_RESPONSE)
        assert configure_response.get("success"), configure_response

        mock_response = client.execute_request_and_get_response_body("GET", mock_path)
        assert mock_response == BYTE_RESPONSE

    @pytest.mark.parametrize("expected_status", EXPECTED_STATUSES)
    def test_configure_binary_mock_by_statuses(self, client: ProxyMock, expected_status):
        request_data = deepcopy(TEST_CONFIGURE_BINARY_DATA)

        configure_response = client.configure_binary_mock(
            path=request_data["path"], body=BYTE_RESPONSE, status_code=expected_status
        )

        assert configure_response.get("success"), configure_response

        test_response = client.execute_request("GET", request_data["path"])
        assert test_response.status_code == expected_status

    def test_configure_binary_mock_by_params(self, client: ProxyMock):
        request_data = deepcopy(TEST_CONFIGURE_BINARY_DATA)

        configure_response = client.configure_binary_mock(**request_data)
        assert configure_response.get("success"), configure_response

        mock_response = client.execute_request("GET", request_data["path"])
        assert mock_response.content == request_data["body"]
        assert mock_response.status_code == request_data["status_code"]

        request_params_response = client.get_traffic()
        assert request_params_response.get("data")
        for req_param in request_params_response["data"]:
            assert req_param["extra_info"] == request_data["extra_info"]

    def test_configure_binary_mock_by_proxy_host(self, client: ProxyMock):
        request_data = {}
        proxy_host, path = PROXY_HOST_DATA

        request_data["proxy_host"] = proxy_host
        request_data["path"] = path

        configure_response = client.configure_binary_mock(**request_data)
        assert configure_response.get("success"), configure_response

        mock_response = client.execute_request("GET", request_data["path"])
        assert mock_response.content
        assert mock_response.ok

    def test_configure_binary_mock_by_timeout(self, client: ProxyMock):
        request_data = deepcopy(TEST_CONFIGURE_BINARY_DATA)
        request_data["timeout"] = 0.12

        configure_response = client.configure_binary_mock(**request_data)
        assert configure_response.get("success")

        start_time = time.time()
        mock_response = client.execute_request("GET", request_data["path"])
        end_time = time.time()
        elapsed_time = end_time - start_time

        assert elapsed_time >= request_data["timeout"]
        assert mock_response.content == request_data["body"]
        assert mock_response.status_code == request_data["status_code"]

    def test_configure_binary_with_custom_headers(self, client: ProxyMock):
        request_data = deepcopy(TEST_CONFIGURE_BINARY_DATA)

        configure_response = client.configure_binary_mock(**request_data)
        assert configure_response.get("success")

        mock_response = client.execute_request("GET", request_data["path"])

        for key, value in request_data["headers"].items():
            assert mock_response.headers[key] == value

        assert mock_response.content == request_data["body"]
        assert mock_response.status_code == request_data["status_code"]

    def test_configure_binary_empty_response(self, client: ProxyMock):
        request_data = deepcopy(TEST_CONFIGURE_BINARY_DATA)
        request_data["body"] = EMPTY_BYTE_RESPONSE

        configure_response = client.configure_binary_mock(**request_data)
        assert configure_response.get("success")

        mock_response = client.execute_request("GET", request_data["path"])
        assert mock_response.content == EMPTY_BYTE_RESPONSE


class TestGetStorage:

    def test_get_storage(self, client: ProxyMock):
        response = client.get_storage()

        assert response["success"]
        assert not response["data"]

    def test_get_storage_by_existing_path(self, client: ProxyMock, configure_mock):
        response = client.get_storage(configure_mock["path"])

        assert response["success"]
        assert response["data"]

        data = response["data"]
        assert data["extra_info"] == configure_mock["extra_info"]
        assert data["mock_data"]["body"] == configure_mock["body"]
        assert data["mock_data"]["headers"] == configure_mock["headers"]
        assert data["mock_data"]["status_code"] == configure_mock["status_code"]
        assert data["proxy_host"] == configure_mock["proxy_host"]
        assert data["timeout"] == configure_mock["timeout"] or data["timeout"] == 0.0

    def test_get_storage_by_non_existent_path(self, client: ProxyMock, configure_mock):
        response = client.get_storage(configure_mock["path"] + "/test")

        assert response["success"]
        assert not response["data"]

    def test_get_storage_with_binary_body(self, client: ProxyMock, configure_binary_mock):
        response = client.get_storage()

        assert response["success"]
        assert response["data"]

    def test_get_storage_with_binary_body_by_path(self, client: ProxyMock, configure_binary_mock):
        response = client.get_storage(configure_binary_mock["path"])

        assert response["success"]
        assert response["data"]["mock_data"]["body"] == str(configure_binary_mock["body"])


class TestGetRequestParams:

    def test_get_request_params(self, client: ProxyMock):
        response = client.get_traffic()

        assert response["success"]
        assert not response["data"]

    def test_get_request_params_by_existing_service(self, client: ProxyMock, configure_mock):
        client.execute_request_and_get_response_body("GET", configure_mock["path"])
        response = client.get_traffic()

        assert response["success"]
        assert response["data"]

        for req_param in response["data"]:
            assert req_param["extra_info"] == configure_mock["extra_info"]
            assert req_param["request_body"] is None
            assert req_param["request_headers"]
            assert req_param["request_path"] == configure_mock["path"]

    def test_send_proto_request(self, client: ProxyMock, configure_binary_mock):
        client.execute_request("POST", configure_binary_mock["path"], data=BYTE_RESPONSE)

        response = client.get_traffic()

        assert response["success"]
        assert response["data"]

        for req_param in response["data"]:
            assert req_param["request_body"] == str(BYTE_RESPONSE)
            assert req_param["request_path"] == configure_binary_mock["path"]
            assert req_param["request_headers"]

    def test_send_request_with_headers(self, client: ProxyMock, configure_mock):
        test_header, value = "X-Test-Header", "123"
        client.execute_request("POST", configure_mock["path"], headers={test_header: value})

        response = client.get_traffic()

        assert response["success"]
        assert response["data"]

        for req_param in response["data"]:
            assert req_param["request_path"] == configure_mock["path"]
            assert req_param["request_headers"][test_header] == value


class TestClearStorage:

    def test_clear_storage(self, client: ProxyMock, configure_mock, configure_binary_mock):
        storage = client.get_storage()
        assert len(storage["data"]) == 2

        response = client.clean_storage()
        assert response.get("success")

        storage = client.get_storage()
        assert not storage["data"]

    def test_delete_existing_mock(self, client: ProxyMock, configure_mock):
        response = client.clean_storage(configure_mock["path"])
        assert response.get("success")

        storage = client.get_storage(configure_mock["path"])
        assert not storage["data"]

    def test_delete_non_existent_mock(self, client: ProxyMock, configure_mock):
        response = client.clean_storage(configure_mock["path"] + "/test")
        assert not response.get("success")

        storage = client.get_storage(configure_mock["path"])
        assert storage["data"]


class TestClearParams:
    request_test_data = {"test_key": "test_value"}

    def test_clear_params(self, client: ProxyMock, configure_mock, configure_binary_mock):
        mock_response = client.execute_request_and_get_response_body("GET", configure_mock["path"])
        assert mock_response

        mock_response = client.execute_request_and_get_response_body("GET", configure_binary_mock["path"])
        assert mock_response

        traffic_storage = client.get_traffic()
        assert len(traffic_storage) == 2

        response = client.clean_traffic()
        assert response.get("success")

        traffic_storage = client.get_traffic()
        assert not traffic_storage["data"]


def test_catch_unknown_path(client: ProxyMock):
    path = "/unknown"
    response = client.execute_request("POST", path)

    assert response.status_code == 404
    assert response.json().get("error") == f"Не найден мок {path}"
