MOCK_PATHS = [
    "/test",
    "test",
    "test/",
    "/test/",
    "/test/test",
    "/test/test/",
    "test/test",
    "test/test/",
    "test/1/2/3",
    "test?arg=1",
]

MOCK_PATHS_PROTO = [
    "/proto",
    "proto",
    "proto/",
    "/proto/",
    "/proto/test",
    "/proto/test/",
    "proto/test",
    "proto/test/",
    "proto/1/2/3",
    "proto?arg=1",
]

EXPECTED_RESPONSE = [
    "test",
    {"test": "test"},
    {},
    ["test"],
    [{"test": "test"}],
    [],
    None,
]

EXPECTED_STATUSES = [201, 302, 425, 599]

BYTE_RESPONSE = "Any Proto Object".encode()

TEST_CONFIGURE_DATA = {
    "path": "/test",
    "body": {"test_key": "test_value"},
    "headers": {"Test": "Header"},
    "extra_info": {"service": "test_service"},
    "status_code": 201,
    "proxy_host": None,
    "timeout": None,
}

TEST_CONFIGURE_BINARY_DATA = {
    "path": "/proto/test/binary",
    "body": BYTE_RESPONSE,
    "headers": {"Test": "Header"},
    "extra_info": {"service": "test_service"},
    "status_code": 201,
    "proxy_host": None,
    "timeout": None,
}

PROXY_HOST_DATA = "http://ivi.ru", "/profile/notifications"
