from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts_app'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
