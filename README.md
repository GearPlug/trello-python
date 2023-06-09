
# trello-python
![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*trello-python* is an API wrapper for Trello, written in Python.  
This library uses Oauth2 for authentication and notifications using webhooks.
## Installing
```
pip install trello-python
```
## Usage
```python
from trello.client import Client
client = Client(api_key, token=None)
```
If you don't have a token, follow this instructions:
1. **Get authorization URL to obtain token**
```python
url = client.authorization_url(return_url)
```
2. **Set access token**
```python
client.set_token(access_token)
```
Check more information about Trello Oauth: https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/
#### Get current user
```python
user = client.get_current_user()
```
### Workspaces
#### - List Workspaces
```python
# filter = One of: all, members, none, public (Note: members filters to only private Workspaces)
# fields = all or a comma-separated list of organization fields
# paid_accounts = Whether or not to include paid account information in the returned workspace object  
workspace = client.get_workspaces(member_id, filter=None, fields=None, paid_accounts=None)
```
#### - List Workspace Members
```python
members = client.get_members(workspace_id)
```
#### - List Workspace boards
```python
# filter = One of: all, members, none, public (Note: members filters to only private Workspaces) \n
# fields = all or a comma-separated list of organization fields \n
boards = client.get_boards(workspace_id, filter=None, fields=None)
```
### Boards
#### Get board
```python
board = client.get_board(board_id)
```
#### - List board cards
```python
# limit = maximum: 1000
cards = client.get_cards(board_id, limit=None)
```
#### - List board lists
```python
# cards = Valid values: all, closed, none, open  
# filter = Valid values: all, closed, none, open  
# fields = all or a comma-separated list of list fields
lists = client.get_board_lists(board_id, cards=None, filter=None, fields=None)
```
#### - List board labels
```python
# limit = default: 50, maximum: 1000
labels = client.get_board_labels(board_id, limit=None)
```
#### - Create label
```python
# color = Valid values: yellow, purple, blue, red, green, orange, black, sky, pink, lime
label = client.create_label(board_id, name, color=None)
```
### Cards
#### - Create Card
```python
# pos: The position of the new card. top, bottom, or a positive float
# due, start: these params accept only isoformat dates.
# idMembers, idLabels: string with a list of ids separated by commas.
card = client.create_card(
    idList,
    name=None, 
    desc=None, 
    pos=None, 
    due=None, 
    start=None, 
    dueComplete=None, 
    idMembers=None, 
    idLabels=None, 
    urlSource=None
)
```
#### - Add label to card
```python
label = client.add_label_to_card(card_id, label_id)
```
#### - Add comment to card
```python
comment = client.add_comment_to_card(card_id, comment_text)
```
#### - List card actions
```python
# action_type = A comma-separated list of action types. Default: commentCard
actions = client.get_card_actions(card_id, action_type=None, page=None)
```
A list of action types here: https://developer.atlassian.com/cloud/trello/guides/rest-api/action-types/
#### - List card checklists
```python
# fields = all or a comma-separated list of: idBoard,idCard,name,pos
checklists = client.get_card_checklists(card_id, fields=None)
```
#### - List card custom fields
```python
custom_fields = client.get_card_customfields(card_id)
```
#### - Get custom field
```python
custom_field = client.get_customfield(customfield_id)
```
### Checklists
#### - Add item to checklist
```python
# pos = The position of the check item in the checklist. One of: top, bottom, or a positive number.
# due, dueReminder: these params accept only isoformat dates.
item = client.add_item_to_checklist(checklist_id, name, pos=None, checked=None, due=None, dueReminder=None, idMember=None)
```
### Webhooks
#### - List token webhooks
```python
webhooks = client.get_token_webhooks()
```
#### - Create webhook
```python
webhook = client.create_webhook(idModel, callbackURL, description=None, active=True)
```
#### Delete webhook
```python
client.delete_webhook(webhook_id)
```
### Search
```python
# modelTypes = all or a comma-separated list of: actions, boards, cards, members, organizations. Default all.
# partial = true means that it will look for content that starts with any of the words in your query
search = client.search(query, modelTypes=None, partial=None)
```
