import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession

GROUPS_RESPONSE = '{"data":[{"id":1503,"alias":"demo","url":"https://lix.li/g/demo","name":"Seller group","is_rotate":false,"description":"Marketing group","created_datetime":"2026-05-21T22:08:37+03:00","deactivated_datetime":null}],"meta":{"total":1,"limit":20,"next_url":null}}'


@pytest.fixture
def mock():
    return MockSession()


def test_list_groups_maps_dto(mock):
    mock.add_response(200, GROUPS_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    result = client.groups().list()

    assert len(result.groups) == 1
    assert result.groups[0].id == 1503
    assert result.groups[0].name == 'Seller group'
    assert result.groups[0].url == 'https://lix.li/g/demo'
    assert result.meta.total == 1
    assert result.meta.limit == 20
    assert result.meta.next_url is None


def test_list_groups_request_no_pagination(mock):
    mock.add_response(200, GROUPS_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.groups().list()

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/groups'
    assert requests[0]['method'] == 'GET'
    assert requests[0]['json'] is None


def test_list_groups_request_with_pagination(mock):
    mock.add_response(200, GROUPS_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.groups().list(limit=10, from_id=1000)

    requests = mock.get_requests()
    assert requests[0]['url'] == 'https://lix.li/api/1.0/groups?limit=10&from_id=1000'
