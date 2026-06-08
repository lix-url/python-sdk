import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession

PROFILE_RESPONSE = '{"client":{"id":1022,"name":"Test Client","email":"test@lix.li","created_datetime":"2022-04-24T17:38:42+03:00"},"user":{"name":"John Doe","email":"test_user@lix.li","created_datetime":"2023-04-14T17:38:42+03:00"},"plan":{"id":2,"name":"Pro","start_datetime":"2026-05-09T13:12:46+03:00","end_datetime":"2027-05-09T13:12:46+03:00"},"usage":{"links":{"limit":null,"used":1,"remaining":null},"api_links":{"limit":500,"used":100,"remaining":400},"mass_links":{"limit":100,"used":10,"remaining":90}}}'


@pytest.fixture
def mock():
    return MockSession()


def test_profile_me_maps_dto(mock):
    mock.add_response(200, PROFILE_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    profile = client.profile().me()

    assert profile.client.id == 1022
    assert profile.client.name == 'Test Client'
    assert profile.client.email == 'test@lix.li'
    assert profile.client.created_datetime == '2022-04-24T17:38:42+03:00'

    assert profile.user.name == 'John Doe'
    assert profile.user.email == 'test_user@lix.li'
    assert profile.user.created_datetime == '2023-04-14T17:38:42+03:00'

    assert profile.plan.id == 2
    assert profile.plan.name == 'Pro'
    assert profile.plan.start_datetime == '2026-05-09T13:12:46+03:00'
    assert profile.plan.end_datetime == '2027-05-09T13:12:46+03:00'

    assert profile.usages.links.limit is None
    assert profile.usages.links.used == 1
    assert profile.usages.links.remaining is None

    assert profile.usages.api_links.limit == 500
    assert profile.usages.api_links.used == 100
    assert profile.usages.api_links.remaining == 400

    assert profile.usages.mass_links.limit == 100
    assert profile.usages.mass_links.used == 10
    assert profile.usages.mass_links.remaining == 90


def test_profile_me_request(mock):
    mock.add_response(200, PROFILE_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.profile().me()

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/me'
    assert requests[0]['method'] == 'GET'
    assert requests[0]['json'] is None
    assert requests[0]['headers']['X-Api-Key'] == 'lix_test_some_key1'
    assert requests[0]['headers']['User-Agent'] == 'lix-python-sdk/0.1.0'
