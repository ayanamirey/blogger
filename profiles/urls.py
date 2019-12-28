from django.urls import path, re_path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile_detail, name='profile-details'),
    path('edit', views.update_profile, name='profile-update')
]
