import pytest
from lix_sdk.client import Client
from tests.mock_session import MockSession

RESPONSE_WITH_GROUP = '{"data":{"id":79697,"alias":"demo","short_url":"https://lix.li/demo","url":"https://example.com/very/long/page","is_public":true,"title":"Some Title","created_datetime":"2026-05-27T22:16:22+03:00","active_before_datetime":null,"deleted_datetime":null,"group":{"id":1503,"alias":"demo","url":"https://lix.li/g/demo","name":"Seller group","is_rotate":false,"description":"Marketing group","created_datetime":"2026-05-21T22:08:37+03:00","deactivated_datetime":null},"tags":["sale","promo"],"meta":{"title":"Awesome sale!","og:title":"Awesome sale!!!!","description":"Woooooo, its wonderful!","og:description":"Woooowww, its wonderful!","keywords":"sale, promo"}},"usage":{"limit":500,"used":3,"remaining":497}}'
RESPONSE_NO_GROUP = '{"data":{"id":79697,"alias":"demo2","short_url":"https://lix.li/demo2","url":"https://example.com","is_public":true,"title":null,"created_datetime":"2026-05-27T22:16:22+03:00","active_before_datetime":null,"deleted_datetime":null,"group":null,"tags":[],"meta":[]},"usage":{"limit":500,"used":3,"remaining":497}}'


@pytest.fixture
def mock():
    return MockSession()


def test_create_link_maps_dto(mock):
    mock.add_response(201, RESPONSE_WITH_GROUP)
    client = Client('lix_test_123', mock)

    result = client.links().create('https://example.com/very/long/page')
    link = result.link

    assert link.id == 79697
    assert link.title == 'Some Title'
    assert link.alias == 'demo'
    assert link.short_url == 'https://lix.li/demo'
    assert link.url == 'https://example.com/very/long/page'
    assert link.is_public is True
    assert link.active_before_datetime is None
    assert link.deleted_datetime is None
    assert link.created_datetime == '2026-05-27T22:16:22+03:00'
    assert link.tags == ['sale', 'promo']
    assert link.meta == {
        'title': 'Awesome sale!',
        'og:title': 'Awesome sale!!!!',
        'description': 'Woooooo, its wonderful!',
        'og:description': 'Woooowww, its wonderful!',
        'keywords': 'sale, promo',
    }
    assert link.group.id == 1503
    assert link.group.alias == 'demo'
    assert link.group.url == 'https://lix.li/g/demo'
    assert link.group.is_rotate is False
    assert link.group.deactivated_datetime is None
    assert link.group.created_datetime == '2026-05-21T22:08:37+03:00'
    assert result.usage.limit == 500
    assert result.usage.used == 3
    assert result.usage.remaining == 497


def test_create_link_null_group(mock):
    mock.add_response(201, RESPONSE_NO_GROUP)
    client = Client('lix_test_123', mock)

    result = client.links().create('https://example.com')

    assert result.link.group is None
    assert result.link.title is None


def test_create_link_request(mock):
    mock.add_response(201, RESPONSE_NO_GROUP)
    client = Client('lix_test_some_key1', mock)

    client.links().create(
        'https://example.com/very/long/page',
        alias='demo',
        title='Some Title',
        group_id=1000,
        tags=['sale', 'promo'],
        meta={'title': 'Awesome sale!', 'og:title': 'Awesome sale!!!!', 'description': 'Woooooo, its wonderful!', 'og:description': 'Woooowww, its wonderful!', 'keywords': 'sale, promp'},
        utm={'utm_source': 'google ads', 'utm_medium': 'email', 'utm_campaign': 'sale', 'utm_content': 'buy', 'utm_term': 'banner'},
        tracking_pixel_ids=[1110, 1023],
        active_before_datetime='2029-05-21T21:25:40+03:00',
        password='12345',
        is_public=True,
    )

    requests = mock.get_requests()
    assert len(requests) == 1
    assert requests[0]['url'] == 'https://lix.li/api/1.0/links'
    assert requests[0]['method'] == 'POST'
    assert requests[0]['headers']['X-Api-Key'] == 'lix_test_some_key1'
    assert requests[0]['headers']['User-Agent'] == 'lix-python-sdk/0.1.0'
    body = requests[0]['json']
    assert body['url'] == 'https://example.com/very/long/page'
    assert body['alias'] == 'demo'
    assert body['title'] == 'Some Title'
    assert body['group_id'] == 1000
    assert body['tags'] == ['sale', 'promo']
    assert body['tracking_pixel_ids'] == [1110, 1023]
    assert body['active_before_datetime'] == '2029-05-21T21:25:40+03:00'
    assert body['password'] == '12345'
    assert body['is_public'] is True
