from django.urls import path
from .views import signup_view, login_view, CustomLogoutView, profile_view

app_name = 'accounts_app'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
]
