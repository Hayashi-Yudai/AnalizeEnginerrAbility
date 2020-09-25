from django.shortcuts import render
from userpage.forms import AccountSetForm


def index(request):
    context = {"form": AccountSetForm()}
    return render(request, "userpage/index.html", context)
