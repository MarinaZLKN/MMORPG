from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import BaseRegisterView, IndexView

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='main_sign.html'),
         name='signup'),
    path('signout/', IndexView.as_view(), name='sign-out'),
]
