from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from signup.forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "signup/index.html"
    success_url = reverse_lazy("userpage")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        self.object = user

        return HttpResponseRedirect(self.get_success_url())
