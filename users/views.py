from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserForm, UserUpdateForm, UserPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from users.services import send_registration_email, send_new_password_email


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register_user.html'
    success_url = reverse_lazy('users:login_user')


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:profile_user'))
                else:
                    return HttpResponse('Disabled account')

    form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login_user.html', context)


@login_required
def user_profile_view(request):
    user_object = request.user
    context = {
        # 'user_object': user_object,
        'title': f'Профиль пользователя {user_object.first_name}',
        # 'form': UserForm(instance=user_object),
    }

    return render(request, 'users/user_profile_read_only.html', context)


@login_required
def user_udate_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return redirect('users:profile_user')
    user_name = user_object.first_name
    context = {
        'user_object': user_object,
        'title': f' Изменить профиль пользователя {user_name}',
        'form': UserUpdateForm(instance=user_object),
    }
    return render(request, 'users/update_user.html', context)


@login_required
def user_change_password_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserPasswordChangeForm(user_object, request.POST)
        if form.is_valid():
            user_object = form.save()
            update_session_auth_hash(request, user_object)
            messages.success(request, 'Ваш пароль успешно обновлен!')

            return HttpResponseRedirect(reverse('users:profile_user'))
        else:
            messages.error(request, 'Не удалось изменить пароль.')
    form = UserPasswordChangeForm(user_object)
    context = {
        'form': form
    }
    return render(request, 'users/change_password_user.html', context)


def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')


@login_required
def user_generate_new_password(request):
    new_password = User.objects.make_random_password()
    request.user.set_password(new_password)
    request.user.save()
    send_new_password_email(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
