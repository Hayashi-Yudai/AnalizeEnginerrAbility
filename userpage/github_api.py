from typing import Dict, Any, Optional
from requests.auth import HTTPBasicAuth
import requests
import os


class GitHubAPI:
    def __init__(self):
        self._username = os.environ.get("API_USERNAME")
        self._token = os.environ.get("API_TOKEN")
        self.rest_base = "https://api.github.com/"
        self.graphql_url = "https://api.github.com/graphql"

    @property
    def username(self) -> PermissionError:
        raise PermissionError("cannot access to the username")

    @property
    def token(self) -> PermissionError:
        raise PermissionError("cannot access to the API token")

    @username.setter
    def username(self, username) -> Optional[TypeError]:
        if type(username) != str or username == "":
            raise TypeError("Invalid username")
        self._username = username

        return

    @token.setter
    def token(self, token) -> Optional[TypeError]:
        if type(token) != str or token == "":
            raise TypeError("Invalid API token")
        self._token = token

        return

    def get_rest(self, endpoint: str):
        auth = HTTPBasicAuth(username=self._username, password=self._token)
        response = requests.get(self.rest_base + endpoint, auth=auth)

        if response.status_code != 200:
            return []

        return response.json()

    def post_graphql(self, query: str) -> Dict[str, Any]:
        header = {"Authorization": f"Bearer {self._token}"}
        response = requests.post(
            self.graphql_url, json={"query": query}, headers=header
        )

        if response.status_code != 200:
            return dict()

        return response.json()
