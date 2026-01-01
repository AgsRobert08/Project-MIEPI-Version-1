from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'miepi'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='miepi:login'), name='logout'),

    #Cursos
    path('courses/', views.CoursesView.as_view(), name='courses_list'),
    path('inscrito/create/', views.InscritoCreateView.as_view(), name='inscrito_create'),
    path('inscrito/qr/<int:id>/', views.InscritoQRView.as_view(), name='inscrito_qr'),
    path('inscritos/', views.InscritosListView.as_view(), name='inscritos_list'),


]