from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView,View
import qrcode
from io import BytesIO
from django.core.files import File

# vista del login
def login_view(request):
    # Si el usuario ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('miepi:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('miepi:dashboard')  # Cambié esto de index a dashboard
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'miepi/login.html')


@login_required(login_url='miepi:login')
def dashboard(request):  # Cambié el nombre de index a dashboard
    return render(request, 'miepi/dashboard.html')


# Lista de cursos 
class CoursesView(LoginRequiredMixin,View):
    template_name = "miepi/cursos/cursos.html"
    
    def get(self, request):
        courses = Cursos.objects.all().order_by("start_date")
        data = {
            'course': courses,
        }
        
class CursosCreateView(LoginRequiredMixin,CreateView):
    model = Cursos
    form_class = CoursesForm
    template_name = "miepi/cursos/create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            form = CoursesForm(request.POST or None, request.FILES or None)
            
            if form.is_valid():
                form.save()
                messages.success(request, "¡Curso creado correctamente!")
            else:
                print(form.errors)
                
        except Exception as e:
            print(e)
            messages.error(request, e)
            
        return redirect(request.META.get('HTTP_REFERER','miepi:courses_list'))
    
class CursosUpdateView(LoginRequiredMixin,UpdateView):
    model = Cursos
    form_class = CoursesForm
    template_name = "miepi/courses/update.html"
    
    def post(self, request, *args, **kwargs):
        form = CoursesForm(request.POST or None, request.FILES or None, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, "¡Curso editado correctamente!")
        else:
            messages.error(request, form.errors)
        
        return redirect(request.META.get('HTTP_REFERER','miepi:courses_list'))
    
@login_required
def CoursesDelete(request, id):
    course = Cursos.objects.get(id=id)
    course.delete()
    messages.success(request, "¡Curso eliminado correctamente!")
        
    return redirect(request.META.get('HTTP_REFERER','miepi:courses_list'))


import qrcode
from io import BytesIO
from django.core.files import File
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class InscritoCreateView(LoginRequiredMixin, View):

    def post(self, request):
        form = InscritoForm(request.POST)

        if form.is_valid():
            inscrito = form.save(commit=False)
            inscrito.save()  # ya tenemos ID y UUID

            # === GENERAR QR ===
            qr = qrcode.make(str(inscrito.codigo))
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            buffer.seek(0)  # 🔥 MUY IMPORTANTE

            inscrito.qr_image.save(
                f"{inscrito.codigo}.png",
                File(buffer),
                save=True
            )

            messages.success(
                request,
                "✅ Usuario registrado correctamente. QR generado."
            )
            return redirect('miepi:inscritos_list')

        # === ERRORES DEL FORM ===
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")

        return redirect(request.META.get('HTTP_REFERER'))

from django.shortcuts import render, get_object_or_404
class InscritoQRView(LoginRequiredMixin, View):
    template_name = "miepi/inscritos/qr.html"

    def get(self, request, id):
        inscrito = get_object_or_404(Inscrito, id=id)
        return render(request, self.template_name, {'inscrito': inscrito})


class InscritosListView(LoginRequiredMixin, View):
    template_name = "miepi/inscripciones/inscritos.html"

    def get(self, request):
        inscritos = Inscrito.objects.all().order_by('-fecha_registro')
        return render(request, self.template_name, {
            'inscritos': inscritos
        })
