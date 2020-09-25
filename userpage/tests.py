from django.test import Client

from userpage.forms import AccountSetForm

# from userpage.views import Index


def test_valid_username():
    testcase = "Hayashi-Yudai"
    form = AccountSetForm({"username": testcase})

    assert form.is_valid()


def test_space_is_invalid():
    testcase = "Hayashi Yudai"
    form = AccountSetForm({"username": testcase})

    assert not form.is_valid()
    assert form.errors["username"][0] == "Do NOT contain any spaces"


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
    assert response.context["username"] == "user"
    assert type(response.context["form"]) == AccountSetForm
