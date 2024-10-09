from django.urls import path

from .views import login_view, logout_view, profile_dashboard

urlpatterns = [
    path('', profile_dashboard, name='profile_dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
