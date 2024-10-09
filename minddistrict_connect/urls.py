from django.urls import re_path

from .views import connect_redirect

urlpatterns = [
    re_path('connect/(?P<path>.*)/', connect_redirect, name='dlo'),
]
