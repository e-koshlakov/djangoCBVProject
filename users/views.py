from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm
from users.models import User
from users.services import send_new_password_email, send_registration_email


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register_user.html'
    success_url = reverse_lazy('users:login_user')

    def form_valid(self, form):
        self.object = form.save()
        send_registration_email(self.object.email)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'users/login_user.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('users:profile_user')

    def get_success_url(self):
        return reverse('users:profile_user')


class UserProfileView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_profile_read_only.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users:profile_user')

    def get_object(self, queryset=None):
        return self.request.user


class UserChangePasswordView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/change_password_user.html'
    success_url = reverse_lazy('users:profile_user')


class UserLogoutView(LogoutView):
    pass
    template_name = 'users/logout_user.html'


@login_required
def user_generate_new_password(request):
    new_password = User.objects.make_random_password()
    request.user.set_password(new_password)
    request.user.save()
    send_new_password_email(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
