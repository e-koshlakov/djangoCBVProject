from django.urls import path
from users.apps import UsersConfig
from users.views import  user_profile_view, user_logout_view, user_udate_view, \
    user_change_password_view,  user_generate_new_password, UserRegisterView, UserLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='login_user'),
    path('logout/', user_logout_view, name='logout_user'),
    path('register/', UserRegisterView.as_view(), name='register_user'),
    path('profile/', user_profile_view, name='profile_user'),
    path('update/', user_udate_view, name='update_user'),
    path('change_password/', user_change_password_view, name='change_password_user'),
    path('profile/genpassword/', user_generate_new_password, name='user_generate_new_password'),
]
