from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
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
    path('inscritos/eliminar/<int:id>/',views.eliminar_registros,name='eliminar_registros'),

    path('asistencia/registrar/', views.registrar_asistencia, name='registrar_asistencia'),
    
    #path('asistencia/escanear/', TemplateView.as_view(template_name='miepi/pase_lista/escanear.html'), name='escanear_asistencia')
    path('asistencia/escanear/',views.escanear_asistencia,name='escanear_asistencia'),
    path('asistencia/lista/',views.AsistenciasListView.as_view(),name='lista_asistencias'),
    path('asistencia/eliminar/<int:id>/',views.eliminar_asistencia,name='eliminar_asistencia'),
# urls.py
    path('asistencia/registrar-manual/',views.registrar_asistencia_manual,name='registrar_asistencia_manual'),


]