from django import forms
from django.core.exceptions import ValidationError


def not_has_space(value: str) -> Exception:
    if " " in value:
        raise ValidationError("Do NOT contain any spaces")


class AccountSetForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        validators=[not_has_space],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "github-account-input",
                "placeholder": "GitHuub Username",
            }
        ),
    )
