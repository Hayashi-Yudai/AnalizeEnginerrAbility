from collections import defaultdict
from datetime import datetime
from django.shortcuts import render
from django.views import View
import numpy as np
import threading
from typing import List, Dict, Any

from userpage.forms import AccountSetForm
from userpage.github_api import GitHubAPI


class Index(View):
    def __init__(self, *args, **kwargs):
        super(Index, self).__init__(*args, **kwargs)

        self.api = GitHubAPI()
        self.default_context = {
            "form": AccountSetForm(),
            "star_score": 50.0,
            "star_score_pos": 40,
            "issue_score": 50.0,
            "issue_score_pos": 40,
            "pr_score": 50.0,
            "pr_score_pos": 40,
            "star_scores": [50 for _ in range(12)],
            "issue_scores": [50 for _ in range(12)],
            "pull_request_scores": [50 for _ in range(12)],
            "profile_img": "../../static/userpage/media/default_profile_img.png",
        }
        self.user_infos = defaultdict(float)

    def get(self, request, *args, **kwargs):
        """ Inherit method from View """
        return render(request, "userpage/index.html", self.default_context)

    def post(self, request, *args, **kwargs):
        """ Inherit method from View """
        data = request.POST
        form = AccountSetForm(data)

        if form.is_valid():
            username = data["username"]
            self.run_request_threads(username)

            # Mock data
            star_scores = [65, 70, 70, 70, 70, 72, 70, 70, 70, 70, 70, 71]
            issue_scores = [35, 35, 40, 46, 52, 54, 60, 70, 70, 70, 70, 71]
            pull_request_scores = [25, 32, 32, 36, 44, 44, 46, 45, 56, 59, 60, 71]
            star_scores[-1] = self.user_infos["star_score"]
            issue_scores[-1] = self.user_infos["issue_score"]
            pull_request_scores[-1] = self.user_infos["pull_request_score"]

            context = {
                "form": form,
                "username": username,
                "repo_infos": self.user_infos["repo_infos"],
                "star_score": self.user_infos["star_score"],
                "star_score_pos": max(self.user_infos["star_score"] - 13.00, 1),
                "issue_score": self.user_infos["issue_score"],
                "issue_score_pos": max(self.user_infos["issue_score"] - 13.00, 1),
                "pr_score": self.user_infos["pull_request_score"],
                "pr_score_pos": max(self.user_infos["pull_request_score"] - 13.00, 1),
                "star_scores": star_scores,
                "issue_scores": issue_scores,
                "pull_request_scores": pull_request_scores,
                "profile_img": self.user_infos["profile_img"],
            }

            return render(request, "userpage/index.html", context)

        return render(request, "userpage/index.html", self.default_context)

    def run_request_threads(self, username):
        profile_img_thread = threading.Thread(
            target=self.fetch_profile_img, args=(username,)
        )
        elapsed_days_thread = threading.Thread(
            target=self._calc_elapsed_days, args=(username,)
        )
        repo_infos_thread = threading.Thread(
            target=self.get_repositories, args=(username,)
        )
        star_score_thread = threading.Thread(
            target=self.calc_star_score,
            args=(username, self.user_infos["elapsed_days"]),
        )
        issue_score_thread = threading.Thread(
            target=self.calc_issue_score,
            args=(username, self.user_infos["elapsed_days"]),
        )
        pull_request_score_thread = threading.Thread(
            target=self.calc_pull_request_score, args=(username,)
        )

        elapsed_days_thread.start()
        profile_img_thread.start()
        repo_infos_thread.start()
        pull_request_score_thread.start()

        # elapsed_day is necessary to run star_score_thread and issue_score_thread
        elapsed_days_thread.join()

        star_score_thread.start()
        issue_score_thread.start()

        profile_img_thread.join()
        repo_infos_thread.join()
        star_score_thread.join()
        issue_score_thread.join()
        pull_request_score_thread.join()

    def fetch_profile_img(self, username):
        avatar_url = self.api.fetch_avatar_url(username)["user"]["avatarUrl"]

        self.user_infos["profile_img"] = avatar_url

    def get_repositories(self, username: str):
        data: List[Dict[str, Any]] = self.api.get_rest(
            f"users/{username}/repos?per_page=500"
        )

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

        self.user_infos["repo_infos"] = repo_infos

    def _calc_elapsed_days(self, username: str):
        user_info: Dict[str, Any] = self.api.get_rest(f"users/{username}")

        account_created_at = datetime.strptime(
            user_info["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        )
        last_updated_at = datetime.strptime(
            user_info["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
        )

        elapsed_days = (last_updated_at - account_created_at).days
        self.user_infos["elapsed_days"] = elapsed_days

    def _fetch_star_count(self, username: str) -> int:
        star_count = self.api.fetch_star_count(username)["user"]["starredRepositories"][
            "totalCount"
        ]

        return star_count

    def _fetch_issue_count(self, username: str) -> int:
        response = self.api.fetch_issue_count(username)

        return response["user"]["issues"]["totalCount"]

    @staticmethod
    def calc_deviation_value(val: float, mean: float, stdev: float) -> float:
        dev_val = (val - mean) / stdev * 10 + 50
        dev_val = int(dev_val * 100) / 100

        return min(dev_val, 100)

    def calc_star_score(self, username: str, elapsed_days: int):
        """
        Calculate deviation value as score
        """
        star_count = self._fetch_star_count(username)

        if star_count == 0:
            self.user_infos["star_score"] = 0.0
            return None

        bias = 1000 if elapsed_days < 1000 else 1000 - elapsed_days
        star_per_day_norm = star_count / (elapsed_days + bias) / 3.0
        if star_per_day_norm >= 1:
            self.user_infos["star_score"] = 100.0
            return None

        logit = np.log10(star_per_day_norm / (1 - star_per_day_norm))

        if elapsed_days > 4100:
            self.user_infos["star_score"] = self.calc_deviation_value(
                logit,
                mean=-2.447,
                stdev=0.8237,
            )
        else:
            self.user_infos["star_score"] = self.calc_deviation_value(
                logit,
                mean=-3.405,
                stdev=0.6361,
            )

    def calc_issue_score(self, username: str, elapsed_days: int):
        """
        Calculate deviation value as score
        """
        issue_count = self._fetch_issue_count(username)
        bias = 1000 if elapsed_days < 1000 else 1000 - elapsed_days
        issue_per_day = issue_count / (elapsed_days + bias)

        if issue_per_day >= 1:
            self.user_infos["issue_score"] = 100.0
            return None
        if issue_per_day == 0:
            self.user_infos["issue_score"] = 0.0
            return None

        logit = np.log10(issue_per_day / (1 - issue_per_day))

        self.user_infos["issue_score"] = self.calc_deviation_value(
            logit,
            mean=-2.377,
            stdev=0.7849,
        )

    def calc_pull_request_score(self, username: str):
        response: Dict[str, Any] = self.api.fetch_pull_request_infos(username)["user"]
        if response is None:
            return 0

        pull_request_num: int = response["pullRequests"]["totalCount"]
        pull_requests: List[Dict[str, Any]] = response["pullRequests"]["nodes"]

        merged_pr_num = 0
        own_pr_num = 0

        for pr in pull_requests:
            if pr["merged"]:
                merged_pr_num += 1

            if (
                pr["mergedBy"] is not None
                and pr["author"]["login"] == pr["mergedBy"]["login"]
            ):
                own_pr_num += 1

        own_pr_ratio = own_pr_num / (merged_pr_num + 1)
        merged_ratio = merged_pr_num / (pull_request_num + 1)
        if own_pr_ratio < 0.8:
            score = self.calc_deviation_value(merged_ratio, mean=0.719, stdev=0.168)
        else:
            score = self.calc_deviation_value(merged_ratio, mean=0.869, stdev=0.104)

        self.user_infos["pull_request_score"] = score
