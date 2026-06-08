from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class UsageItem:
    limit: Optional[int]
    used: int
    remaining: Optional[int]


@dataclass
class Usages:
    links: UsageItem
    api_links: UsageItem
    mass_links: UsageItem


@dataclass
class ResponseMeta:
    total: int
    limit: int
    next_url: Optional[str]


@dataclass
class ClientDto:
    id: int
    name: str
    email: str
    created_datetime: str


@dataclass
class User:
    name: str
    email: str
    created_datetime: str


@dataclass
class Plan:
    id: int
    name: str
    start_datetime: str
    end_datetime: str


@dataclass
class Profile:
    client: ClientDto
    user: User
    plan: Plan
    usages: Usages


@dataclass
class Group:
    id: int
    alias: str
    url: str
    name: str
    is_rotate: bool
    description: Optional[str]
    created_datetime: str
    deactivated_datetime: Optional[str]


@dataclass
class Groups:
    groups: List[Group]
    meta: ResponseMeta


@dataclass
class Link:
    id: int
    alias: str
    url: str
    short_url: str
    title: Optional[str]
    group: Optional[Group]
    tags: List[str]
    meta: Any
    is_public: bool
    created_datetime: str
    active_before_datetime: Optional[str]
    deleted_datetime: Optional[str]


@dataclass
class Links:
    links: List[Link]
    meta: ResponseMeta


@dataclass
class LinkShortenResult:
    link: Link
    usage: UsageItem


class MetaEnum:
    META_TITLE = 'title'
    META_OG_TITLE = 'og:title'
    META_DESCRIPTION = 'description'
    META_OG_DESCRIPTION = 'og:description'
    META_KEYWORDS = 'keywords'
    META_OG_IMAGE = 'og:image'
