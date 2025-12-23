from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'miepi'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='miepi:login'), name='logout'),
]