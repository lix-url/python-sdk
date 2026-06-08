from typing import Optional

import requests

from lix_sdk.http.api_client import ApiClient
from lix_sdk.resources.groups import Groups
from lix_sdk.resources.links import Links
from lix_sdk.resources.profile import Profile


class Client:
    def __init__(self, api_key: str, session: Optional[requests.Session] = None):
        api_client = ApiClient(api_key, session)
        self._profile = Profile(api_client)
        self._groups = Groups(api_client)
        self._links = Links(api_client)

    def profile(self) -> Profile:
        return self._profile

    def groups(self) -> Groups:
        return self._groups

    def links(self) -> Links:
        return self._links
