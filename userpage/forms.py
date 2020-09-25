from django import forms


class AccountSetForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "github-account-input",
                "placeholder": "GitHuub Username",
            }
        ),
    )
