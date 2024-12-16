from django.urls import path
from users.apps import UsersConfig
from users.views import user_generate_new_password, UserRegisterView, \
    UserLoginView, UserProfileView, UserUpdateView, UserChangePasswordView, UserLogoutView, UserListView, UserProfileListView

app_name = UsersConfig.name

urlpatterns = [
    # работа с аккаунтом пользователя
    path('', UserLoginView.as_view(), name='login_user'),
    path('logout/', UserLogoutView.as_view(), name='logout_user'),
    path('register/', UserRegisterView.as_view(), name='register_user'),
    path('profile/', UserProfileView.as_view(), name='profile_user'),
    path('update/', UserUpdateView.as_view(), name='update_user'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password_user'),
    path('profile/genpassword/', user_generate_new_password, name='user_generate_new_password'),

    # Просмотр списка пользователей
    path('all_users/', UserListView.as_view(), name='users_list'),
    path('profile/<int:pk>/', UserProfileListView.as_view(), name='profile_user_view'),
]
