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
