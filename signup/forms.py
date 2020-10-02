from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["required"] = "required"

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
