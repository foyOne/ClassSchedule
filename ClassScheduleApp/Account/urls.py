from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page, never_cache

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('refresh', views.refresh, name='refresh'),
    path('users', views.UserView.as_view(), name='users'),
    path('all-users', views.all_users, name='show'),
]