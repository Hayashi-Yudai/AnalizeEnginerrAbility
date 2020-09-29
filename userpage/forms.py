from django import forms
from django.core.exceptions import ValidationError
from typing import Optional


def not_has_space(value: str) -> Optional[Exception]:
    if " " in value:
        raise ValidationError("Do NOT contain any spaces")

    return None


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
