from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UserForms
from django.views import View

class RegisterView(View):
    def get(self, request):
        create_form = UserForms()
        context = {'form': create_form}
        return render(request, "register.html", context)

    def post(self, request):
        create_form = UserForms(data=request.POST)
        if not create_form.is_valid():
            context = {
                'form': create_form
            }
            return render(request, 'register.html', context)
        create_form.save()
        return redirect('users:login')


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'login.html', context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        context = {
            'login_form': login_form
        }
        if not login_form.is_valid():
            return render(request, 'login.html', context)
        user = login_form.get_user()
        login(request, user)
        return redirect('landing_page')


class ProfileView(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect("users:login")
        return render(request, 'profile.html', {'user': user})

