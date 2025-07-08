from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginUserForm


def login_user(request: HttpRequest):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponsePermanentRedirect(reverse('home'))
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request: HttpRequest):
    logout(request)
    return HttpResponsePermanentRedirect(reverse('users:login'))
