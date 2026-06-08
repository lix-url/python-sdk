from lix_sdk.dto import ClientDto, Plan, Profile as ProfileDto, UsageItem, Usages, User
from lix_sdk.http.api_client import ApiClient


class Profile:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client

    def me(self) -> ProfileDto:
        data = self._api_client.get_profile_me()
        return ProfileDto(
            client=ClientDto(
                id=data['client']['id'],
                name=data['client']['name'],
                email=data['client']['email'],
                created_datetime=data['client']['created_datetime'],
            ),
            user=User(
                name=data['user']['name'],
                email=data['user']['email'],
                created_datetime=data['user']['created_datetime'],
            ),
            plan=Plan(
                id=data['plan']['id'],
                name=data['plan']['name'],
                start_datetime=data['plan']['start_datetime'],
                end_datetime=data['plan']['end_datetime'],
            ),
            usages=Usages(
                links=UsageItem(data['usage']['links']['limit'], data['usage']['links']['used'], data['usage']['links']['remaining']),
                api_links=UsageItem(data['usage']['api_links']['limit'], data['usage']['api_links']['used'], data['usage']['api_links']['remaining']),
                mass_links=UsageItem(data['usage']['mass_links']['limit'], data['usage']['mass_links']['used'], data['usage']['mass_links']['remaining']),
            ),
        )
