from datetime import datetime
from django.shortcuts import render
from django.views import View
import os
from typing import List, Dict, Any

from userpage.forms import AccountSetForm
from userpage.github_api import GitHubAPI


class Index(View):
    def __init__(self, *args, **kwargs):
        super(Index, self).__init__(*args, **kwargs)

        self.api = GitHubAPI(
            os.environ.get("API_USERNAME"), os.environ.get("API_TOKEN")
        )
        self.default_context = {
            "form": AccountSetForm(),
            "star_score": 50.00,
            "star_score_posi": 40,
            "issue_score": 50.00,
            "issue_score_posi": 40,
        }

    def get(self, request, *args, **kwargs):
        """ Inherit method from View """
        return render(request, "userpage/index.html", self.default_context)

    def post(self, request, *args, **kwargs):
        """ Inherit method from View """
        data = request.POST
        form = AccountSetForm(data)

        if form.is_valid():
            username = data["username"]

            # TODO: リクエストの並列化
            elapsed_days = self._calc_elapsed_days(username)
            repo_infos = self.get_repositories(username)
            star_score = self.calc_star_score(username, elapsed_days)
            issue_score = self.calc_issue_score(username, elapsed_days)

            context = {
                "form": form,
                "username": username,
                "repo_infos": repo_infos,
                "star_score": star_score,
                "star_score_posi": star_score - 10.00,
                "issue_score": issue_score,
                "issue_score_posi": issue_score - 10.00,
            }

            return render(request, "userpage/index.html", context)

        return render(request, "userpage/index.html", self.default_context)

    def get_repositories(self, username: str) -> List[Dict[str, Any]]:
        data = self.api.get_rest(f"users/{username}/repos?per_page=500")

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
        user_info = self.api.get_rest(f"users/{username}")

        account_created_at = datetime.strptime(
            user_info["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        )
        last_updated_at = datetime.strptime(
            user_info["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
        )

        elapsed_days = (last_updated_at - account_created_at).days

        return elapsed_days

    def _calc_star_count(self, username: str) -> int:
        query = (
            "{ user(login:"
            + f'"{username}"'
            + ") { starredRepositories { totalCount } } }"
        )
        star_count = self.api.post_graphql(query)["data"]["user"][
            "starredRepositories"
        ]["totalCount"]

        return star_count

    def _fetch_issue_count(self, username: str) -> int:
        query = '{ user(login: "' + username + '") { issues(first:10) { totalCount }}}'
        response = self.api.post_graphql(query)

        return response["data"]["user"]["issues"]["totalCount"]

    def calc_deviation_value(self, val: float, mean: float, stdev: float) -> float:
        dev_val = (val - mean) / stdev * 10 + 50
        dev_val = int(dev_val * 100) / 100

        return min(dev_val, 100)

    def calc_biased_deviation_value(
        self, count: int, mean: float, stdev: float, elapsed_days: int
    ) -> float:
        bias = 1000 if elapsed_days < 1000 else 0
        star_per_day_biased = count / (elapsed_days + bias)

        return self.calc_deviation_value(star_per_day_biased, mean=mean, stdev=stdev)

    def calc_star_score(self, username: str, elapsed_days: int) -> float:
        """
        Calculate Deviation value
        """
        star_count = self._calc_star_count(username)

        return self.calc_biased_deviation_value(
            star_count, mean=0.02862, stdev=0.1257, elapsed_days=elapsed_days
        )

    def calc_issue_score(self, username: str, elapsed_days: int) -> float:
        """
        Calculate Deviation value
        """
        issue_count = self._fetch_issue_count(username)

        return self.calc_biased_deviation_value(
            issue_count, mean=0.01043, stdev=0.04264, elapsed_days=elapsed_days
        )
