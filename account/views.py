from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm


class Registration(FormView):
    template_name = "registration/register.html"
    form_class = UserRegistrationForm
    success_url = "/login/"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return super().form_valid(form)


class Login(LoginView):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().get(request, *args, **kwargs)
