from datetime import datetime
from django.shortcuts import render
from django.views import View
import os
import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Any

from userpage.forms import AccountSetForm


class Index(View):
    def get(self, request, *args, **kwargs):
        context = {"form": AccountSetForm(), "star_score": 50}
        return render(request, "userpage/index.html", context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = AccountSetForm(data)

        if form.is_valid():
            username = data["username"]
            repo_infos = self.get_repositories(username)
            star_score = self.calc_star_score(username)

            context = {
                "form": form,
                "username": username,
                "repo_infos": repo_infos,
                "star_score": star_score,
            }

            return render(request, "userpage/index.html", context)

        return render(request, "userpage/index.html", {"form": form, "total_score": 50})

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

    def calc_star_score(self, username: str) -> float:
        auth = HTTPBasicAuth(
            os.environ.get("API_USERNAME"), os.environ.get("API_TOKEN")
        )

        user_info = requests.get(
            f"https://api.github.com/users/{username}", auth=auth
        ).json()

        account_created_at = datetime.strptime(
            user_info["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        )
        last_updated_at = datetime.strptime(
            user_info["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
        )

        elapsed_days = (last_updated_at - account_created_at).days

        star_count = 0
        page = 1

        while True:
            star_repositories = requests.get(
                f"https://api.github.com/users/{username}/starred?per_page=100&page={page}",
                auth=auth,
            ).json()

            if len(star_repositories) == 0:
                break

            page += 1
            star_count += len(star_repositories)

        bias = 1000 if elapsed_days < 1000 else 0
        star_per_day_biased = star_count / (elapsed_days + bias)

        deviation_val = (star_per_day_biased - 0.02862) / 0.1257 * 10 + 50
        deviation_val = int(deviation_val * 100) / 100

        return min(deviation_val, 100)
