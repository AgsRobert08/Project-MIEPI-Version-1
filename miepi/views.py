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
    #if request.user.is_authenticated:
     #   return redirect('miepi:dashboard')
    
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
    
# views.py
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from .models import Inscrito, Asistencia
import uuid
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Inscrito, Asistencia

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Inscrito, Asistencia

@csrf_exempt
def registrar_asistencia(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")

        if not codigo:
            return JsonResponse({
                "ok": False,
                "msg": "❌ Código vacío"
            })

        try:
            inscrito = Inscrito.objects.get(codigo=codigo)

            asistencia, creada = Asistencia.objects.get_or_create(
                inscrito=inscrito,
                fecha=timezone.now().date(),
                defaults={"asistio": True}
            )

            if creada:
                return JsonResponse({
                    "ok": True,
                    "msg": f"✅ Asistencia registrada: {inscrito.nombre}"
                })
            else:
                return JsonResponse({
                    "ok": False,
                    "msg": f"⚠️ {inscrito.nombre} ya pasó lista hoy"
                })

        except Inscrito.DoesNotExist:
            return JsonResponse({
                "ok": False,
                "msg": "❌ QR no válido"
            })

    return JsonResponse({
        "ok": False,
        "msg": "Método no permitido"
    })


#def escanear_asistencia(request):
 #   return render(request, 'miepi/pase_lista/escanear.html')

def escanear_asistencia(request):
    inscritos = Inscrito.objects.order_by('nombre')
    return render(request, 'miepi/pase_lista/escanear.html', {
        'inscritos': inscritos
    })

from django.views import View
from django.shortcuts import render
from .models import Asistencia

class AsistenciasListView(View):
    template_name = 'miepi/pase_lista/lista_asistencias.html'

    def get(self, request):
        asistencias = Asistencia.objects.select_related('inscrito').order_by('-fecha', '-hora')

        return render(request, self.template_name, {
            'asistencias': asistencias
        })

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Asistencia

@login_required
def eliminar_asistencia(request, id):
    asistencia = get_object_or_404(Asistencia, id=id)

    asistencia.delete()
    messages.success(request, "✅ Asistencia eliminada correctamente")

    return redirect('miepi:lista_asistencias')

# Eliminar los registros de inscritos en el evento
def eliminar_registros(request, id):
    registro = get_object_or_404(Inscrito, id=id)
    registro.delete()
    messages.success(request, "Registro eliminado correctamente")
    return redirect('miepi:inscritos_list')



from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Inscrito, Asistencia

@login_required
@require_POST
def registrar_asistencia_manual(request):
    inscrito_id = request.POST.get("inscrito_id")

    inscrito = get_object_or_404(Inscrito, id=inscrito_id)

    asistencia, creada = Asistencia.objects.get_or_create(
        inscrito=inscrito,
        fecha=timezone.now().date()
    )

    if creada:
        return JsonResponse({
            "ok": True,
            "msg": f"✅ Asistencia registrada: {inscrito.nombre}"
        })
    else:
        return JsonResponse({
            "ok": False,
            "msg": f"⚠️ {inscrito.nombre} ya estaba registrado hoy"
        })
