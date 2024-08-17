import subprocess
import time
from copy import deepcopy

import pytest

from client.client import ProxyMock
from tests import HOST
from tests.constants import TEST_CONFIGURE_BINARY_DATA
from tests.constants import TEST_CONFIGURE_DATA


@pytest.fixture(scope="session")
def client():
    return ProxyMock(HOST)


@pytest.fixture(scope="session", autouse=True)
def run_server():
    try:
        server_process = subprocess.Popen(["gunicorn", "-c", "proxy_mock/etc/gunicorn.conf.py"])
        time.sleep(1)
    except subprocess.SubprocessError as err:
        pytest.fail(err)
    finally:
        yield
        server_process.terminate()


@pytest.fixture
def configure_mock(client):
    request_data = deepcopy(TEST_CONFIGURE_DATA)

    configure_response = client.configure_mock(**request_data)
    assert configure_response.get("success")

    return request_data


@pytest.fixture
def configure_binary_mock(client):
    request_data = deepcopy(TEST_CONFIGURE_BINARY_DATA)

    configure_response = client.configure_binary_mock(**request_data)
    assert configure_response.get("success")

    return request_data


@pytest.fixture(autouse=True)
def setup_server(client):
    client.clear_mocks()
    client.clear_params()