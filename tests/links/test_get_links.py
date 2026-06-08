import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession

LINKS_RESPONSE = '{"data":[{"id":79618,"alias":"a2Ag4","short_url":"https://lix.li/a2Ag4","url":"https://example.com","is_public":true,"title":"Promo","created_datetime":"2026-05-21T23:35:02+03:00","active_before_datetime":"2029-05-21T21:25:40+03:00","deleted_datetime":null,"group":{"id":1005,"alias":"2222","url":"https://lix.li/g/2222","name":"Test","is_rotate":false,"description":"df","created_datetime":"2026-05-18T01:55:50+03:00","deactivated_datetime":null},"tags":["promo","sale"],"meta":{"title":"Promo"}},{"id":79615,"alias":"oSCZ0mP","short_url":"https://lix.li/oSCZ0mP","url":"https://console.cloud.google.com","is_public":true,"title":null,"created_datetime":"2026-05-18T03:31:12+03:00","active_before_datetime":null,"deleted_datetime":null,"group":null,"tags":[],"meta":{}}],"meta":{"total":5,"limit":2,"next_url":"https://lix.li/api/1.0/links?from_id=79615&limit=2"}}'


@pytest.fixture
def mock():
    return MockSession()


def test_list_links_maps_dto(mock):
    mock.add_response(200, LINKS_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    result = client.links().list()

    assert len(result.links) == 2
    assert result.links[0].short_url == 'https://lix.li/a2Ag4'
    assert result.links[1].short_url == 'https://lix.li/oSCZ0mP'
    assert result.links[0].group is not None
    assert result.links[1].group is None
    assert result.meta.total == 5
    assert result.meta.limit == 2
    assert result.meta.next_url == 'https://lix.li/api/1.0/links?from_id=79615&limit=2'


def test_list_links_request_no_pagination(mock):
    mock.add_response(200, LINKS_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.links().list()

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/links'
    assert requests[0]['method'] == 'GET'
    assert requests[0]['json'] is None


def test_list_links_request_with_pagination(mock):
    mock.add_response(200, LINKS_RESPONSE)
    client = Client('lix_test_some_key1', mock)

    client.links().list(limit=100, from_id=500)

    requests = mock.get_requests()
    assert requests[0]['url'] == 'https://lix.li/api/1.0/links?limit=100&from_id=500'
