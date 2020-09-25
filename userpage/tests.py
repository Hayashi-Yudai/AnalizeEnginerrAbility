from userpage.forms import AccountSetForm


def test_valid_username():
    testcase = "Hayashi-Yudai"
    form = AccountSetForm({"username": testcase})

    assert form.is_valid()


def test_space_is_invalid():
    testcase = "Hayashi Yudai"
    form = AccountSetForm({"username": testcase})

    assert not form.is_valid()
    assert form.errors["username"][0] == "Do NOT contain any spaces"
