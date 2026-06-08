import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession

UPDATE_RESPONSE = '{"data":{"id":1503,"alias":"demo","url":"https://lix.li/g/demo","name":"Seller group","is_rotate":false,"description":"Updated description","created_datetime":"2026-05-21T22:08:37+03:00","deactivated_datetime":null}}'


@pytest.fixture
def mock():
    return MockSession()


def test_update_group_maps_dto(mock):
    mock.add_response(200, UPDATE_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    group = client.groups().update(10, description='Updated description')

    assert group.id == 1503
    assert group.name == 'Seller group'
    assert group.description == 'Updated description'


def test_update_group_request(mock):
    mock.add_response(200, UPDATE_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.groups().update(10, description='Updated description')

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/groups/10'
    assert requests[0]['json'] == {'name': None, 'description': 'Updated description', 'is_rotate': False}
    assert requests[0]['method'] == 'PATCH'
    assert requests[0]['headers']['X-Api-Key'] == 'lix_test_some_key1'
    assert requests[0]['headers']['User-Agent'] == 'lix-python-sdk/0.1.0'
