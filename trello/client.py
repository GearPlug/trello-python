from urllib.parse import urlencode

import requests

from trello.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://api.trello.com/1/"
    AUTH_URL = "https://trello.com/1/authorize?"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, api_key=None, token=None):
        self.key = api_key
        self.token = token

    def authorization_url(self, return_url=None, state=None):
        if state and return_url:
            return_url = f"{return_url}?state={state}"
        params = {
            "expiration": "never",
            "return_url": return_url,
            "name": "NewToken",
            "scope": "read,write,account",
            "response_type": "token",
            "key": self.key,
        }
        return self.AUTH_URL + urlencode(params)

    def set_token(self, token):
        self.token = token
        return True

    def get_current_user(self):
        """
        Use this function to get user's id, you will need it to access some other endpoints.
        """
        return self.get("members/me/")

    def get_workspaces(self, member_id):
        return self.get(f"members/{member_id}/organizations")

    def get_boards(self, workspace_id):
        return self.get(f"organizations/{workspace_id}/boards")

    def get_cards(self, board_id):
        return self.get(f"boards/{board_id}/cards")

    def get_card_actions(self, card_id, action_type):
        params = {"filter": action_type}
        return self.get(f"cards/{card_id}/actions", params=params)

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def put(self, endpoint, **kwargs):
        response = self.request("PUT", endpoint, **kwargs)
        return self.parse(response)

    def patch(self, endpoint, **kwargs):
        response = self.request("PATCH", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, headers=None, params=None, **kwargs):
        if headers:
            self.headers.update(headers)
        self.params = {"key": self.key, "token": self.token}
        if params:
            self.params.update(params)
        return requests.request(method, self.URL + endpoint, headers=self.headers, params=self.params, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
