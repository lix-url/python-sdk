import pytest
from lix_sdk.client import Client
from lix_sdk.exceptions import (
    NotFoundException,
    RateLimitException,
    ServerException,
    UnauthorizedException,
    ValidationException,
)
from tests.mock_session import MockSession

VALIDATION_RESPONSE = '{"error":"invalid_parameters","parameter_errors":{"name":{"code":"required","message":"field required"}},"error_message":null}'


@pytest.fixture
def mock():
    return MockSession()


def test_validation_exception_contains_data(mock):
    mock.add_response(400, VALIDATION_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    with pytest.raises(ValidationException) as exc_info:
        client.groups().create('test')

    assert exc_info.value.data == {'name': {'code': 'required', 'message': 'field required'}}


@pytest.mark.parametrize('status_code,resource,method,args,exc_class', [
    (401, 'groups', 'get', (1,), UnauthorizedException),
    (404, 'groups', 'get', (1,), NotFoundException),
    (429, 'groups', 'get', (1,), RateLimitException),
    (500, 'groups', 'get', (1,), ServerException),

    (401, 'groups', 'list', (), UnauthorizedException),
    (404, 'groups', 'list', (), NotFoundException),
    (429, 'groups', 'list', (), RateLimitException),
    (500, 'groups', 'list', (), ServerException),

    (401, 'groups', 'delete', (1,), UnauthorizedException),
    (404, 'groups', 'delete', (1,), NotFoundException),
    (429, 'groups', 'delete', (1,), RateLimitException),
    (500, 'groups', 'delete', (1,), ServerException),

    (401, 'groups', 'create', ('test',), UnauthorizedException),
    (404, 'groups', 'create', ('test',), NotFoundException),
    (429, 'groups', 'create', ('test',), RateLimitException),
    (500, 'groups', 'create', ('test',), ServerException),

    (401, 'groups', 'update', (1,), UnauthorizedException),
    (404, 'groups', 'update', (1,), NotFoundException),
    (429, 'groups', 'update', (1,), RateLimitException),
    (500, 'groups', 'update', (1,), ServerException),

    (401, 'links', 'get', (1,), UnauthorizedException),
    (404, 'links', 'get', (1,), NotFoundException),
    (429, 'links', 'get', (1,), RateLimitException),
    (500, 'links', 'get', (1,), ServerException),

    (401, 'links', 'list', (), UnauthorizedException),
    (404, 'links', 'list', (), NotFoundException),
    (429, 'links', 'list', (), RateLimitException),
    (500, 'links', 'list', (), ServerException),

    (401, 'links', 'delete', (1,), UnauthorizedException),
    (404, 'links', 'delete', (1,), NotFoundException),
    (429, 'links', 'delete', (1,), RateLimitException),
    (500, 'links', 'delete', (1,), ServerException),

    (401, 'links', 'create', ('https://example.com',), UnauthorizedException),
    (404, 'links', 'create', ('https://example.com',), NotFoundException),
    (429, 'links', 'create', ('https://example.com',), RateLimitException),
    (500, 'links', 'create', ('https://example.com',), ServerException),

    (401, 'links', 'update', (1,), UnauthorizedException),
    (404, 'links', 'update', (1,), NotFoundException),
    (429, 'links', 'update', (1,), RateLimitException),
    (500, 'links', 'update', (1,), ServerException),
])
def test_api_errors(mock, status_code, resource, method, args, exc_class):
    mock.add_response(status_code, '')
    client = Client('lix_test_some_key1', mock)

    with pytest.raises(exc_class):
        getattr(getattr(client, resource)(), method)(*args)
