from typing import Dict, Any
from requests.auth import HTTPBasicAuth
import requests


class GitHubAPI:
    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token
        self.rest_base = "https://api.github.com/"
        self.graphql_url = "https://api.github.com/graphql"

    def get_rest(self, endpoint: str):
        auth = HTTPBasicAuth(username=self.username, password=self.token)
        response = requests.get(self.rest_base + endpoint, auth=auth)

        if response.status_code != 200:
            return []

        return response.json()

    def post_graphql(self, query: str) -> Dict[str, Any]:
        header = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(
            self.graphql_url, json={"query": query}, headers=header
        )

        if response.status_code != 200:
            return dict()

        return response.json()
