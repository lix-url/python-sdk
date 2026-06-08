import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession

GROUP_RESPONSE = '{"data":{"id":1503,"alias":"demo","url":"https://lix.li/g/demo","name":"Seller group","is_rotate":false,"description":"Marketing group","created_datetime":"2026-05-21T22:08:37+03:00","deactivated_datetime":null}}'


@pytest.fixture
def mock():
    return MockSession()


def test_create_group_maps_dto(mock):
    mock.add_response(200, GROUP_RESPONSE)
    client = Client('lix_test_123', mock)

    group = client.groups().create('Seller group', 'Marketing group', True)

    assert group.id == 1503
    assert group.name == 'Seller group'
    assert group.description == 'Marketing group'
    assert group.alias == 'demo'
    assert group.url == 'https://lix.li/g/demo'
    assert group.is_rotate is False
    assert group.deactivated_datetime is None
    assert group.created_datetime == '2026-05-21T22:08:37+03:00'


def test_create_group_request(mock):
    mock.add_response(200, GROUP_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.groups().create('Seller group', 'Marketing group', True)

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/groups'
    assert requests[0]['json'] == {'name': 'Seller group', 'description': 'Marketing group', 'is_rotate': True}
    assert requests[0]['method'] == 'POST'
    assert requests[0]['headers']['X-Api-Key'] == 'lix_test_some_key1'
    assert requests[0]['headers']['User-Agent'] == 'lix-python-sdk/0.1.0'
