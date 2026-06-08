import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession


@pytest.fixture
def mock():
    return MockSession()


def test_delete_group_request(mock):
    mock.add_response(200, '{}')
    client = Client('lix_test_some_key1', mock)

    client.groups().delete(10)

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/groups/10'
    assert requests[0]['method'] == 'DELETE'
    assert requests[0]['json'] is None
    assert requests[0]['headers']['X-Api-Key'] == 'lix_test_some_key1'
    assert requests[0]['headers']['User-Agent'] == 'lix-python-sdk/0.1.0'


def test_delete_group_returns_none(mock):
    mock.add_response(200, '{}')
    client = Client('lix_test_some_key1', mock)

    result = client.groups().delete(10)

    assert result is None
