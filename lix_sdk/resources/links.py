from typing import Any, Dict, List, Optional

from lix_sdk.dto import Link, Links as LinksDto, LinkShortenResult, ResponseMeta, UsageItem
from lix_sdk.http.api_client import ApiClient
from lix_sdk.resources.groups import Groups


class Links:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client

    def create(
        self,
        url: str,
        alias: Optional[str] = None,
        title: Optional[str] = None,
        group_id: Optional[int] = None,
        tags: Optional[List[str]] = None,
        meta: Optional[Any] = None,
        utm: Optional[Any] = None,
        tracking_pixel_ids: Optional[List[int]] = None,
        active_before_datetime: Optional[str] = None,
        password: Optional[str] = None,
        is_public: bool = True,
    ) -> LinkShortenResult:
        data = self._api_client.create_link({
            'group_id': group_id,
            'url': url,
            'alias': alias,
            'password': password,
            'title': title,
            'tags': tags or [],
            'is_public': is_public,
            'tracking_pixel_ids': tracking_pixel_ids or [],
            'meta': meta or [],
            'utm': utm or [],
            'active_before_datetime': active_before_datetime,
        })
        return LinkShortenResult(
            link=self.link_from_response_data(data['data']),
            usage=UsageItem(data['usage']['limit'], data['usage']['used'], data['usage']['remaining']),
        )

    def update(
        self,
        id: int,
        url: Optional[str] = None,
        title: Optional[str] = None,
        group_id: Optional[int] = None,
        tags: Optional[List[str]] = None,
        meta: Optional[Any] = None,
        utm: Optional[Any] = None,
        tracking_pixel_ids: Optional[List[int]] = None,
        active_before_datetime: Optional[str] = None,
        password: Optional[str] = None,
        is_public: bool = True,
    ) -> LinkShortenResult:
        data = self._api_client.update_link(id, {
            'group_id': group_id,
            'url': url,
            'password': password,
            'title': title,
            'tags': tags or [],
            'is_public': is_public,
            'tracking_pixel_ids': tracking_pixel_ids or [],
            'meta': meta or [],
            'utm': utm or [],
            'active_before_datetime': active_before_datetime,
        })
        return LinkShortenResult(
            link=self.link_from_response_data(data['data']),
            usage=UsageItem(data['usage']['limit'], data['usage']['used'], data['usage']['remaining']),
        )

    def get(self, id: int) -> Link:
        data = self._api_client.get_link(id)
        return self.link_from_response_data(data['data'])

    def delete(self, id: int) -> None:
        self._api_client.delete_link(id)

    def list(self, limit: Optional[int] = None, from_id: Optional[int] = None) -> LinksDto:
        data = self._api_client.get_links(limit, from_id)
        links = [self.link_from_response_data(l) for l in data['data']]
        meta = ResponseMeta(data['meta']['total'], data['meta']['limit'], data['meta']['next_url'])
        return LinksDto(links=links, meta=meta)

    @staticmethod
    def link_from_response_data(link_data: dict) -> Link:
        return Link(
            id=link_data['id'],
            alias=link_data['alias'],
            url=link_data['url'],
            short_url=link_data['short_url'],
            title=link_data['title'],
            group=Groups.group_from_response_data(link_data['group']),
            tags=link_data['tags'],
            meta=link_data['meta'],
            is_public=link_data['is_public'],
            created_datetime=link_data['created_datetime'],
            active_before_datetime=link_data['active_before_datetime'],
            deleted_datetime=link_data['deleted_datetime'],
        )
