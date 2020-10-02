from django.test import Client
import pytest
from typing import Dict, Any

from userpage.forms import AccountSetForm
from userpage.views import Index
from userpage.github_api import GitHubAPI


# Form tests
def test_valid_username():
    testcase = "Hayashi-Yudai"
    form = AccountSetForm({"username": testcase})

    assert form.is_valid()


def test_space_is_invalid():
    testcase = "Hayashi Yudai"
    form = AccountSetForm({"username": testcase})

    assert not form.is_valid()
    assert form.errors["username"][0] == "Do NOT contain any spaces"


# View test
def test_view_get():
    c = Client()
    response = c.get("/userpage/")

    assert response.status_code == 200
    assert type(response.context["form"]) == AccountSetForm
    assert "username" not in response.context.keys()


def test_view_post():
    c = Client()
    response = c.post("/userpage/", {"username": "user"})

    assert response.status_code == 200

    assert "username" in response.context.keys()
    assert "repo_infos" in response.context.keys()
    assert response.context["username"] == "user"
    assert type(response.context["form"]) == AccountSetForm


# REST API test
def test_get_repositories(monkeypatch):
    def mock_get_rest(self, endpoint):
        return [
            {
                "fork": False,
                "name": "test-repository",
                "stargazers_count": 5,
                "forks_count": 4,
                "description": "test repository",
            },
            {
                "fork": True,
                "name": "test-repository",
                "stargazers_count": 5,
                "forks_count": 4,
                "description": "test repository",
            },
        ]

    monkeypatch.setattr(GitHubAPI, "get_rest", mock_get_rest)

    view = Index()
    view.get_repositories("test-user")

    # Test exclude the forked repository
    assert len(view.user_infos["repo_infos"]) == 1

    user_infos: Dict[str, Any] = view.user_infos["repo_infos"][0]

    assert user_infos["name"] == "test-repository"
    assert user_infos["star_cnt"] == 5
    assert user_infos["fork_cnt"] == 4
    assert user_infos["description"] == "test repository"


def test_calc_elapsed_days(monkeypatch):
    def mock_get_rest(self, endpoint):
        return {
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2020-01-03T00:00:00Z",
        }

    monkeypatch.setattr(GitHubAPI, "get_rest", mock_get_rest)

    view = Index()
    view._calc_elapsed_days("test-user")

    user_infos: Dict[str, Any] = view.user_infos

    assert user_infos["elapsed_days"] == 2


@pytest.mark.parametrize(
    "star_cnt,elapsed_days,expected",
    [
        (0, 1000, 0),  # has no stars
        (5000, 1000, 100),  # has a lot of stars
        (30, 100, 72.16),  # non-zero bias due to elapsed_days < 1000
        (30, 1000, 72.16),  # elapsed_days < 4100
        (30, 5000, 46.95),  # elapsed_days >= 4100
    ],
)
def test_calc_star_score(monkeypatch, star_cnt, expected, elapsed_days):
    def mock_post_graphql(self, query):
        return {"user": {"starredRepositories": {"totalCount": star_cnt}}}

    monkeypatch.setattr(GitHubAPI, "post_graphql", mock_post_graphql)

    view = Index()
    view.calc_star_score("test-user", elapsed_days)

    assert view.user_infos["star_score"] == expected


@pytest.mark.parametrize(
    "issue_cnt,elapsed_days,expected",
    [
        (0, 1000, 0),  # has no issues
        (5000, 1000, 100),  # has a lot of issues
        (10, 100, 54.86),  # non-zero bias due to elapsed_days < 1000
        (10, 1000, 54.86),  # zero bias
    ],
)
def test_calc_issue_score(monkeypatch, issue_cnt, expected, elapsed_days):
    def mock_post_graphql(self, query):
        return {"user": {"issues": {"totalCount": issue_cnt}}}

    monkeypatch.setattr(GitHubAPI, "post_graphql", mock_post_graphql)

    view = Index()
    view.calc_issue_score("test-user", elapsed_days)

    assert view.user_infos["issue_score"] == expected


def test_calc_pull_request_score_with_low_own_merge_ratio(monkeypatch):
    def mock_post_graphql(self, query):
        return {
            "user": {
                "pullRequests": {
                    "totalCount": 3,
                    "nodes": [
                        {
                            "merged": True,
                            "mergedBy": {"login": "test-user"},
                            "author": {"login": "test-user"},
                        },
                        {
                            "merged": False,
                            "mergedBy": {"login": "test-user"},
                            "author": {"login": "test-user"},
                        },
                        {
                            "merged": True,
                            "mergedBy": {"login": "test-user"},
                            "author": {"login": "test-user-2"},
                        },
                    ],
                }
            }
        }

    monkeypatch.setattr(GitHubAPI, "post_graphql", mock_post_graphql)

    view = Index()
    view.calc_pull_request_score("test-user")

    assert view.user_infos["pull_request_score"] == 36.96


def test_calc_pull_request_score_with_high_own_merge_ratio(monkeypatch):
    def mock_post_graphql(self, query):
        return {
            "user": {
                "pullRequests": {
                    "totalCount": 5,
                    "nodes": [
                        {
                            "merged": True,
                            "mergedBy": {"login": "test-user"},
                            "author": {"login": "test-user"},
                        },
                        {
                            "merged": False,
                            "mergedBy": {"login": "test-user-2"},
                            "author": {"login": "test-user"},
                        },
                        {
                            "merged": True,
                            "mergedBy": {"login": "test-user"},
                            "author": {"login": "test-user"},
                        },
                        {
                            "merged": True,
                            "mergedBy": {"login": "test-user"},
                            "author": {"login": "test-user"},
                        },
                        {
                            "merged": True,
                            "mergedBy": {"login": "test-user"},
                            "author": {"login": "test-user"},
                        },
                    ],
                }
            }
        }

    monkeypatch.setattr(GitHubAPI, "post_graphql", mock_post_graphql)

    view = Index()
    view.calc_pull_request_score("test-user")

    assert view.user_infos["pull_request_score"] == 30.54


# API test
def test_github_api_attributes():
    api = GitHubAPI()
    with pytest.raises(PermissionError):
        _ = api.username

    with pytest.raises(PermissionError):
        _ = api.token

    with pytest.raises(TypeError):
        api.username = ""

    with pytest.raises(TypeError):
        api.token = ""
