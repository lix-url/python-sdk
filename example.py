from lix_sdk import Client, ValidationException, NotFoundException

# Insert your API key here
API_KEY = 'YOUR_API_KEY_HERE'

client = Client(API_KEY)


def main():
    # --- Profile ------------------------------------------------------------------
    print('=== Profile ===')
    profile = client.profile().me()
    print(f'Client: {profile.client.name} | {profile.client.email}')
    print(f'User:   {profile.user.name} | {profile.user.email}')
    print(f'Plan:   {profile.plan.name} (until {profile.plan.end_datetime})')
    print(f'API links remaining: {profile.usages.api_links.remaining} / {profile.usages.api_links.limit}')
    print()

    # --- Create a short link -------------------------------------------------------
    print('=== Create link ===')
    created = client.links().create(
        'https://example.com',  # url
        alias=None,             # alias — None = auto-generated
        title='My test link',   # title
    )
    print(f'Created: {created.link.short_url} → {created.link.url}')
    print(f'ID: {created.link.id} | Alias: {created.link.alias}')
    print(f'API links used: {created.usage.used} / {created.usage.limit}')
    print()

    link_id = created.link.id

    # --- Get link by ID -----------------------------------------------------------
    print('=== Get link by ID ===')
    link = client.links().get(link_id)
    print(f'Link: {link.short_url} | Title: {link.title}')
    print()

    # --- Update link --------------------------------------------------------------
    print('=== Update link ===')
    updated = client.links().update(link_id, title='Updated title')
    print(f'Updated: {updated.link.short_url} | Title: {updated.link.title}')
    print()

    # --- List links ---------------------------------------------------------------
    print('=== List links (first 3) ===')
    links_page = client.links().list(limit=3)
    for l in links_page.links:
        print(f'  - {l.short_url} → {l.url}')
    print(f'Total links: {links_page.meta.total}')
    print()

    # --- Create a group -----------------------------------------------------------
    print('=== Create group ===')
    group = client.groups().create('Test group', 'Created via Python SDK')
    print(f'Group created: {group.name} | ID: {group.id} | URL: {group.url}')
    print()

    # --- List groups --------------------------------------------------------------
    print('=== List groups ===')
    groups_page = client.groups().list(limit=5)
    for g in groups_page.groups:
        print(f'  - {g.name} | {g.url}')
    print(f'Total groups: {groups_page.meta.total}')
    print()

    # --- Delete the test link -----------------------------------------------------
    print('=== Delete test link ===')
    client.links().delete(link_id)
    print(f'Link {link_id} deleted.')


if __name__ == '__main__':
    try:
        main()
    except ValidationException as e:
        print(f'Validation error: {e.data}')
    except NotFoundException as e:
        print(f'Not found: {e}')
    except Exception as e:
        print(f'Error: {e}')
        raise
