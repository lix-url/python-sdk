import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession

GET_RESPONSE = '{"data":{"id":79697,"alias":"demo2","short_url":"https://lix.li/demo2","url":"https://example.com","is_public":true,"title":null,"created_datetime":"2026-05-27T22:16:22+03:00","active_before_datetime":null,"deleted_datetime":null,"group":null,"tags":["sale","promo"],"meta":[]}}'


@pytest.fixture
def mock():
    return MockSession()


def test_get_link_maps_dto(mock):
    mock.add_response(200, GET_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    link = client.links().get(79697)

    assert link.id == 79697
    assert link.alias == 'demo2'
    assert link.short_url == 'https://lix.li/demo2'
    assert link.url == 'https://example.com'
    assert link.is_public is True
    assert link.group is None
    assert link.tags == ['sale', 'promo']


def test_get_link_request(mock):
    mock.add_response(200, GET_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.links().get(123)

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/links/123'
    assert requests[0]['method'] == 'GET'
    assert requests[0]['json'] is None
    assert requests[0]['headers']['X-Api-Key'] == 'lix_test_some_key1'
    assert requests[0]['headers']['User-Agent'] == 'lix-python-sdk/0.1.0'
