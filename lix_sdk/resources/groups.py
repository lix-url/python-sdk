from typing import Optional

from lix_sdk.dto import Group, Groups as GroupsDto, ResponseMeta
from lix_sdk.http.api_client import ApiClient


class Groups:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client

    def create(self, name: str, description: Optional[str] = None, is_rotate: bool = False) -> Group:
        data = self._api_client.create_group({
            'name': name,
            'description': description,
            'is_rotate': is_rotate,
        })
        return self.group_from_response_data(data['data'])

    def update(
        self,
        group_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_rotate: bool = False,
    ) -> Group:
        data = self._api_client.update_group(group_id, {
            'name': name,
            'description': description,
            'is_rotate': is_rotate,
        })
        return self.group_from_response_data(data['data'])

    def get(self, id: int) -> Group:
        data = self._api_client.get_group(id)
        return self.group_from_response_data(data['data'])

    def delete(self, id: int) -> None:
        self._api_client.delete_group(id)

    def list(self, limit: Optional[int] = None, from_id: Optional[int] = None) -> GroupsDto:
        data = self._api_client.get_groups(limit, from_id)
        groups = [self.group_from_response_data(g) for g in data['data']]
        meta = ResponseMeta(data['meta']['total'], data['meta']['limit'], data['meta']['next_url'])
        return GroupsDto(groups=groups, meta=meta)

    @staticmethod
    def group_from_response_data(group_data: Optional[dict]) -> Optional[Group]:
        if not group_data:
            return None
        return Group(
            id=group_data['id'],
            alias=group_data['alias'],
            url=group_data['url'],
            name=group_data['name'],
            is_rotate=group_data['is_rotate'],
            description=group_data['description'],
            created_datetime=group_data['created_datetime'],
            deactivated_datetime=group_data['deactivated_datetime'],
        )
