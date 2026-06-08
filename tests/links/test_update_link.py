import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession

UPDATE_RESPONSE = '{"data":{"id":79697,"alias":"demo2","short_url":"https://lix.li/demo2","url":"https://example.com","is_public":true,"title":"Updated title","created_datetime":"2026-05-27T22:16:22+03:00","active_before_datetime":null,"deleted_datetime":null,"group":null,"tags":[],"meta":[]},"usage":{"limit":500,"used":3,"remaining":497}}'


@pytest.fixture
def mock():
    return MockSession()


def test_update_link_maps_dto(mock):
    mock.add_response(200, UPDATE_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    result = client.links().update(123, title='Updated title')

    assert result.link.id == 79697
    assert result.link.title == 'Updated title'
    assert result.link.short_url == 'https://lix.li/demo2'
    assert result.usage.limit == 500
    assert result.usage.used == 3
    assert result.usage.remaining == 497


def test_update_link_request(mock):
    mock.add_response(200, UPDATE_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.links().update(123, title='Updated title')

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/links/123'
    assert requests[0]['method'] == 'PATCH'
    assert requests[0]['headers']['X-Api-Key'] == 'lix_test_some_key1'
    assert requests[0]['headers']['User-Agent'] == 'lix-python-sdk/0.1.0'
    body = requests[0]['json']
    assert body['title'] == 'Updated title'
    assert body['url'] is None
    assert body['group_id'] is None
    assert body['is_public'] is True
