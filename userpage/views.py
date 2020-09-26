from django.shortcuts import render
from django.views import View
import os
import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Any

from userpage.forms import AccountSetForm


class Index(View):
    def get(self, request, *args, **kwargs):
        context = {"form": AccountSetForm()}
        return render(request, "userpage/index.html", context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = AccountSetForm(data)

        if form.is_valid():
            username = data["username"]
            repo_infos = self.get_repositories(username)

            context = {"form": form, "username": username, "repo_infos": repo_infos}

            return render(request, "userpage/index.html", context)

        return render(request, "userpage/index.html", {"form": form})

    def get_repositories(self, username: str) -> List[Dict[str, Any]]:
        auth = HTTPBasicAuth(
            os.environ.get("API_USERNAME"), os.environ.get("API_TOKEN")
        )

        data = requests.get(
            f"https://api.github.com/users/{username}/repos?per_page=500", auth=auth
        ).json()

        repo_infos = []

        for repo in data:
            if not repo["fork"]:
                name = repo["name"]
                star_cnt = repo["stargazers_count"]
                fork_cnt = repo["forks_count"]
                description = repo["description"]

                repo_infos.append(
                    {
                        "name": name,
                        "star_cnt": star_cnt,
                        "fork_cnt": fork_cnt,
                        "description": description,
                    }
                )

        return repo_infos
