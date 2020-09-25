from django.shortcuts import render
from django.views import View
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

            context = {"form": form, "username": username}

            return render(request, "userpage/index.html", context)

        return render(request, "userpage/index.html", {"form": form})

    def get_repositories(self, username: str) -> List[Dict[str, Any]]:
        pass
