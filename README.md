# Lix.li Python SDK

Official Python SDK for the [Lix.li](https://lix.li) URL shortening and link analytics API.

## Requirements

- Python 3.8+

## Installation

```bash
pip install lix-sdk
```

## Quick Start

```python
from lix_sdk import Client

client = Client('your_api_key')

result = client.links().create('https://example.com')
print(result.link.short_url)  # https://lix.li/xxxxx
```

---

## Links

### Create a short link

```python
result = client.links().create('https://example.com')
print(result.link.short_url)
print(result.usage.remaining)
```

### Create a link with a custom alias

```python
result = client.links().create(
    'https://example.com',
    alias='my-link',
)
print(result.link.short_url)  # https://lix.li/my-link
```

### Create a link with all options

```python
result = client.links().create(
    'https://example.com',
    alias='my-alias',
    title='My Page Title',
    group_id=42,
    tags=['sale', 'promo'],
    meta={'title': 'Sale!', 'description': '...'},
    utm={'utm_source': 'google', 'utm_medium': 'email', 'utm_campaign': 'summer'},
    tracking_pixel_ids=[1001, 1002],
    active_before_datetime='2029-12-31T23:59:59+00:00',
    password='secret123',
    is_public=True,
)
```

### Update a link

```python
result = client.links().update(79697, title='New Title')
print(result.link.title)
```

### Get a link by ID

```python
link = client.links().get(79697)
print(link.short_url)
print(link.url)
print(link.group.name if link.group else None)
```

### List links

```python
response = client.links().list()
# With pagination:
page = client.links().list(limit=20, from_id=79500)

for link in response.links:
    print(link.short_url, link.url)

print(response.meta.total)
print(response.meta.next_url)
```

### Delete a link

```python
client.links().delete(79697)
```

---

## Groups

### Create a group

```python
group = client.groups().create('Marketing')
# With options:
group = client.groups().create(
    'Landing Pages',
    description='Rotating landing pages',
    is_rotate=True,
)
```

### Update a group

```python
group = client.groups().update(
    10,
    description='Updated description',
)
```

### Get a group by ID

```python
group = client.groups().get(10)
print(group.name)
print(group.alias)
print(group.url)
```

### List groups

```python
response = client.groups().list()
# With pagination:
page = client.groups().list(limit=10, from_id=1000)

for group in response.groups:
    print(group.name)

print(response.meta.total)
```

### Delete a group

```python
client.groups().delete(10)
```

---

## Profile

```python
profile = client.profile().me()

print(profile.client.name)
print(profile.user.email)
print(profile.plan.name)
print(profile.usages.api_links.remaining)
print(profile.usages.links.used)
print(profile.usages.mass_links.limit)
```

---

## Error Handling

```python
from lix_sdk import (
    ValidationException,
    UnauthorizedException,
    NotFoundException,
    RateLimitException,
    ServerException,
)

try:
    result = client.links().create('https://example.com')
except ValidationException as e:
    print('Validation errors:', e.data)
except UnauthorizedException:
    print('Invalid API key')
except NotFoundException:
    print('Resource not found')
except RateLimitException:
    print('Rate limit exceeded')
except ServerException:
    print('Server error')
```

---

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## Project Structure

```
lix_sdk/
  __init__.py          — public API exports
  client.py            — main entry point
  exceptions.py        — typed exception classes
  dto.py               — dataclass DTOs
  http/
    api_client.py      — requests-based HTTP wrapper
  resources/
    links.py           — links resource
    groups.py          — groups resource
    profile.py         — profile resource
tests/                 — pytest test suite
example.py             — runnable usage example
```
