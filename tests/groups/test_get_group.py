import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession

GROUP_RESPONSE = '{"data":{"id":10,"alias":"demo","url":"https://lix.li/g/demo","name":"Seller group","is_rotate":false,"description":"Marketing group","created_datetime":"2026-05-21T22:08:37+03:00","deactivated_datetime":null}}'


@pytest.fixture
def mock():
    return MockSession()


def test_get_group_maps_dto(mock):
    mock.add_response(200, GROUP_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    group = client.groups().get(10)

    assert group.id == 10
    assert group.name == 'Seller group'
    assert group.alias == 'demo'
    assert group.url == 'https://lix.li/g/demo'
    assert group.is_rotate is False
    assert group.deactivated_datetime is None
    assert group.created_datetime == '2026-05-21T22:08:37+03:00'


def test_get_group_request(mock):
    mock.add_response(200, GROUP_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.groups().get(10)

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/groups/10'
    assert requests[0]['method'] == 'GET'
    assert requests[0]['json'] is None
    assert requests[0]['headers']['X-Api-Key'] == 'lix_test_some_key1'
    assert requests[0]['headers']['User-Agent'] == 'lix-python-sdk/0.1.0'
