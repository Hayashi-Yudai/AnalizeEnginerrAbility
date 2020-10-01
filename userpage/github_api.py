from typing import Dict, Any, Optional
from requests.auth import HTTPBasicAuth
import requests
import os


class GitHubAPI:
    """Request to the GitHub API"""

    def __init__(self):
        self.__username = os.environ.get("API_USERNAME")
        self.__token = os.environ.get("API_TOKEN")
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
        self.__username = username

        return

    @token.setter
    def token(self, token) -> Optional[TypeError]:
        if type(token) != str or token == "":
            raise TypeError("Invalid API token")
        self.__token = token

        return

    def get_rest(self, endpoint: str):
        """
        Send GET request to the REST API

        Parameter
        ---------
        endpoint : str
            the endpoint of the API. https://api.github.com/$ENDPOINT

        Returns
        -------
        dict or list
            the type of return value is different in each endpoint
            user/ -> dict
            user/$USERNAME/repos -> list
        """
        auth = HTTPBasicAuth(username=self.__username, password=self.__token)
        response = requests.get(self.rest_base + endpoint, auth=auth)

        if response.status_code != 200:
            return []

        return response.json()

    def post_graphql(self, query: str) -> Dict[str, Any]:
        """
        Send POST request to the GraphQL API

        Parameters
        ----------
        query : str
            the GraphQL query. For the query format, see
            https://developer.github.com/v4/

        Returns
        -------
        dict
            returned dict has one key "data" and contains all in its value
        """
        header = {"Authorization": f"Bearer {self.__token}"}
        response = requests.post(
            self.graphql_url, json={"query": query}, headers=header
        )

        if response.status_code != 200:
            return dict()

        return response.json()["data"]

    def fetch_avatar_url(self, username: str) -> Dict[str, Any]:
        query = "{ user(login:" + f'"{username}"' + ") { avatarUrl }}"

        return self.post_graphql(query)

    def fetch_star_count(self, username: str) -> Dict[str, Any]:
        query = (
            "{ user(login:"
            + f'"{username}"'
            + ") { starredRepositories { totalCount } } }"
        )
        return self.post_graphql(query)

    def fetch_issue_count(self, username: str) -> Dict[str, Any]:
        query = '{ user(login: "' + username + '") { issues(first:10) { totalCount }}}'

        return self.post_graphql(query)

    def fetch_pull_request_infos(self, username) -> Dict[str, Any]:
        query = (
            '{ user(login: "'
            + username
            + '") {'
            + """
                pullRequests(last: 100, orderBy:{direction: DESC, field:CREATED_AT}) {
                    totalCount
                    nodes {
                        merged
                        author {
                            login
                        }
                        mergedBy {
                            login
                        }
                    }
                }
            }
        }
                """
        )

        return self.post_graphql(query)
