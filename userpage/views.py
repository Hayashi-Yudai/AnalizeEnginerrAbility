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
        context = {"form": AccountSetForm(), "star_score": 50.00, "star_score_posi": 40}
        return render(request, "userpage/index.html", context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = AccountSetForm(data)

        if form.is_valid():
            username = data["username"]

            # TODO: リクエストの並列化
            repo_infos = self.get_repositories(username)
            star_score = self.calc_star_score(username)

            context = {
                "form": form,
                "username": username,
                "repo_infos": repo_infos,
                "star_score": star_score,
                "star_score_posi": star_score - 10.00,
            }

            return render(request, "userpage/index.html", context)

        return render(
            request,
            "userpage/index.html",
            {"form": form, "star_score": 50.00, "star_score_posi": 40},
        )

    def _fetch_json_from_api(self, endpoint: str) -> Dict[str, Any]:
        auth = HTTPBasicAuth(
            os.environ.get("API_USERNAME"), os.environ.get("API_TOKEN")
        )
        base_url = "https://api.github.com/"

        return requests.get(base_url + endpoint, auth=auth).json()

    def get_repositories(self, username: str) -> List[Dict[str, Any]]:
        data = self._fetch_json_from_api(f"users/{username}/repos?per_page=500")

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

    def _calc_elapsed_days(self, username: str) -> int:
        user_info = self._fetch_json_from_api(f"users/{username}")

        account_created_at = datetime.strptime(
            user_info["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        )
        last_updated_at = datetime.strptime(
            user_info["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
        )

        elapsed_days = (last_updated_at - account_created_at).days

        return elapsed_days

    def _calc_star_count(self, username: str) -> int:
        star_count = 0
        page = 1

        # TODO: 二分探索したら効率的になる？
        while True:
            star_repositories = self._fetch_json_from_api(
                f"users/{username}/starred?per_page=100&page={page}"
            )

            if len(star_repositories) == 0:
                break

            page += 1
            star_count += len(star_repositories)

        return star_count

    def calc_star_score(self, username: str) -> float:
        elapsed_days = self._calc_elapsed_days(username)
        star_count = self._calc_star_count(username)

        bias = 1000 if elapsed_days < 1000 else 0
        star_per_day_biased = star_count / (elapsed_days + bias)

        deviation_val = (star_per_day_biased - 0.02862) / 0.1257 * 10 + 50
        deviation_val = int(deviation_val * 100) / 100

        return min(deviation_val, 100)
