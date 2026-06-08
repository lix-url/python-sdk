from typing import Any, Dict, Optional

import requests

from lix_sdk.exceptions import (
    NotFoundException,
    RateLimitException,
    ServerException,
    UnauthorizedException,
    ValidationException,
)

API_URL = 'https://lix.li/api/1.0'
USER_AGENT = 'lix-python-sdk/0.1.0'


class ApiClient:
    def __init__(self, api_key: str, session: Optional[requests.Session] = None):
        self.api_key = api_key
        self.session = session or requests.Session()

    def _send_request(self, method: str, endpoint: str, body: Optional[Dict] = None) -> Any:
        url = f'{API_URL}/{endpoint}'
        headers = {
            'X-Api-Key': self.api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT,
        }

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=body,
        )

        try:
            data = response.json()
        except Exception:
            data = {}

        if response.status_code == 400:
            raise ValidationException(data.get('parameter_errors'))
        if response.status_code == 401:
            raise UnauthorizedException()
        if response.status_code == 404:
            raise NotFoundException()
        if response.status_code == 429:
            raise RateLimitException()
        if response.status_code == 500:
            raise ServerException()

        return data

    def _get(self, endpoint: str) -> Any:
        return self._send_request('GET', endpoint)

    def _delete(self, endpoint: str) -> Any:
        return self._send_request('DELETE', endpoint)

    def _patch(self, endpoint: str, data: Dict) -> Any:
        return self._send_request('PATCH', endpoint, data)

    def _post(self, endpoint: str, data: Dict) -> Any:
        return self._send_request('POST', endpoint, data)

    def get_profile_me(self) -> Any:
        return self._get('me')

    def get_group(self, id: int) -> Any:
        return self._get(f'groups/{id}')

    def get_groups(self, limit: Optional[int] = None, from_id: Optional[int] = None) -> Any:
        params: Dict[str, Any] = {}
        if limit is not None:
            params['limit'] = limit
        if from_id is not None:
            params['from_id'] = from_id
        qs = '&'.join(f'{k}={v}' for k, v in params.items())
        return self._get(f'groups?{qs}' if qs else 'groups')

    def delete_group(self, id: int) -> Any:
        return self._delete(f'groups/{id}')

    def update_group(self, id: int, data: Dict) -> Any:
        return self._patch(f'groups/{id}', data)

    def create_group(self, data: Dict) -> Any:
        return self._post('groups', data)

    def get_link(self, id: int) -> Any:
        return self._get(f'links/{id}')

    def get_links(self, limit: Optional[int] = None, from_id: Optional[int] = None) -> Any:
        params: Dict[str, Any] = {}
        if limit is not None:
            params['limit'] = limit
        if from_id is not None:
            params['from_id'] = from_id
        qs = '&'.join(f'{k}={v}' for k, v in params.items())
        return self._get(f'links?{qs}' if qs else 'links')

    def delete_link(self, id: int) -> Any:
        return self._delete(f'links/{id}')

    def update_link(self, id: int, data: Dict) -> Any:
        return self._patch(f'links/{id}', data)

    def create_link(self, data: Dict) -> Any:
        return self._post('links', data)
