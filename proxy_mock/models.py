from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_serializer
from pydantic import field_validator
from yarl import URL


class MockDataSchema(BaseModel):
    body: Any = Field(None)
    status_code: int = Field(200)
    headers: dict = Field({})


class MockPathSchema(BaseModel):
    mock_data: MockDataSchema | dict = Field(MockDataSchema().model_dump())
    extra_info: dict = Field({})
    proxy_host: str | None = Field(None)
    timeout: float = Field(0.0)


class ConfigureMockRequestSchema(MockPathSchema):
    path: str = Field(...)

    @field_validator('proxy_host')
    def check_proxy_host(cls, value):
        if value and not URL(value).is_absolute():
            raise ValueError("Parameter 'proxy_host' must be an absolute URL")
        return value

    @field_serializer('path')
    def serialize_path(self, path: str, _info):
        return path.strip("/").split("?")[0]


class InputRequestSchema(BaseModel):
    request_body: Any = Field({})
    request_headers: dict = Field({})
    request_path: str = Field("")
    extra_info: dict = Field({})
