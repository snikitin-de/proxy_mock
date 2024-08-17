"""Роуты для прокси-мока."""


class Endpoints:
    status = "/status"
    configure_mock = "/configure_mock"
    configure_binary_mock = "/configure_mock/binary"
    cleanup_storage = "/cleanup_storage"
    cleanup_params = "/cleanup_params"
    mock_params = "/mock_params"
    storage = "/storage"
