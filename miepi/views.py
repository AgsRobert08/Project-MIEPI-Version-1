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
'''
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
                "Usuario registrado correctamente. QR generado."
            )
            return redirect('miepi:inscritos_list')

        # === ERRORES DEL FORM ===
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")

        return redirect(request.META.get('HTTP_REFERER'))
'''
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('miepi:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'miepi/login.html')


@login_required(login_url='miepi:login')
def dashboard(request):
    return render(request, 'miepi/dashboard.html')


from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files import File
from io import BytesIO
import qrcode
import logging

logger = logging.getLogger(__name__)


class InscritoCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = InscritoForm()
        return render(request, 'miepi/dashboard.html', {
            'form': form
        })

    def post(self, request):
        form = InscritoForm(request.POST)

        # ❌ FORMULARIO INVÁLIDO
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect(request.META.get('HTTP_REFERER'))

        # ✅ FORMULARIO VÁLIDO
        inscrito = form.save(commit=False)
        inscrito.genero = form.cleaned_data['genero'].strip()
        inscrito.save()

        # === GENERAR QR ===
        qr = qrcode.make(str(inscrito.codigo))
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)

        inscrito.qr_image.save(
            f"{inscrito.codigo}.png",
            File(buffer),
            save=True
        )

        # === ENVÍO DE CORREO (PROTEGIDO) ===
        correo = (inscrito.correo_electronico or "").strip()

        if correo:
            try:
                asunto = "Confirmación de registro y código QR"

                denominacion_linea = (
                    f"Denominación: {inscrito.denominacion}\n"
                    if inscrito.denominacion else ""
                )

                mensaje = f"""
Hola {inscrito.nombre},

Tu registro ha sido realizado correctamente.
A continuación te compartimos tus datos:

DATOS DEL REGISTRO
--------------------
Nombre: {inscrito.nombre}
Teléfono: {inscrito.telefono}
Correo: {correo}
Zona: {inscrito.zona}
Subzona: {inscrito.subzona}
Grado Eclesiástico: {inscrito.grado}
{denominacion_linea}Monto: ${inscrito.monto}

Adjuntamos tu código QR en este correo.
Preséntalo el día del evento para el pase de lista.

Saludos cordiales.
"""

                email = EmailMessage(
                    subject=asunto,
                    body=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[correo]
                )

                # 🔒 Adjuntar SOLO si el archivo existe
                if inscrito.qr_image and inscrito.qr_image.path:
                    email.attach_file(inscrito.qr_image.path)

                email.send(fail_silently=False)

            except Exception as e:
                logger.error(f"Error enviando correo: {e}")
                # No romper el flujo del usuario

        messages.success(
            request,
            "Usuario registrado correctamente. QR generado."
        )

        return redirect('miepi:inscritos_list')

from django.shortcuts import render, get_object_or_404
class InscritoQRView(LoginRequiredMixin, View):
    template_name = "miepi/inscritos/qr.html"

    def get(self, request, id):
        inscrito = get_object_or_404(Inscrito, id=id)
        return render(request, self.template_name, {'inscrito': inscrito})

'''
class InscritosListView(LoginRequiredMixin, View):
    template_name = "miepi/inscripciones/inscritos.html"

    def get(self, request):
        genero = request.GET.get('genero', '').strip()  # limpiar espacios de la URL

        if genero:
                    inscritos = Inscrito.objects.filter(genero__iexact=genero).order_by('-fecha_registro')
        else:
                inscritos = Inscrito.objects.all().order_by('-fecha_registro')

        return render(request, self.template_name, {
            'inscritos': inscritos
        })

'''

def get_inscritos_filtrados(request):
    genero = request.GET.get('genero', '').strip()

    qs = Inscrito.objects.all().order_by('nombre')

    if genero:
        qs = qs.filter(genero__iexact=genero)

    return qs.order_by('nombre')

class InscritosListView(LoginRequiredMixin, View):
    template_name = "miepi/inscripciones/inscritos.html"

    def get(self, request):
        inscritos = get_inscritos_filtrados(request)

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
'''
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

'''
from django.utils import timezone

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
                defaults={
                    "asistio": True,
                    "hora": timezone.now().time()
                }
            )

            if creada:
                return JsonResponse({
                    "ok": True,
                    "msg": f" Asistencia registrada: {inscrito.nombre}",
                    "fecha": asistencia.fecha.strftime("%Y-%m-%d"),
                    "hora": asistencia.hora.strftime("%H:%M")
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

from django.views import View
from django.shortcuts import render
from .models import Asistencia

class AsistenciasListView(View):
    template_name = 'miepi/pase_lista/lista_asistencias.html'

    def get(self, request):
        asistencias = Asistencia.objects.select_related('inscrito').order_by('-fecha', '-hora')
        
        # FILTRAR POR GÉNERO SI EXISTE EN GET
        genero = request.GET.get('genero')
        if genero:
            asistencias = asistencias.filter(inscrito__genero=genero)

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

from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Inscrito
from .forms import InscritoForm
from django.contrib.messages.views import SuccessMessageMixin

class InscritoUpdateView(SuccessMessageMixin, UpdateView):
    model = Inscrito
    form_class = InscritoFormEdit
    template_name = 'miepi/inscripciones/editar_inscrito.html'
    success_url = reverse_lazy('miepi:inscritos_list')
    success_message = "Registro actualizado correctamente"

from django.http import JsonResponse
from django.db.models import Q

def buscar_inscrito(request):
    q = request.GET.get('q', '').strip()

    if not q:
        return JsonResponse([], safe=False)

    inscritos = Inscrito.objects.filter(
        Q(nombre__icontains=q) |
        Q(telefono__icontains=q)
    )[:10]

    data = []
    for i in inscritos:
        data.append({
            "id": i.id,
            "nombre": i.nombre,
            "telefono": i.telefono,
            "codigo": i.codigo
        })

    return JsonResponse(data, safe=False)


from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.formats import date_format

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


from django.views import View
from django.http import HttpResponse
from django.utils.formats import date_format
from django.contrib.auth.mixins import LoginRequiredMixin

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from .models import Asistencia


class AsistenciaPDFView(LoginRequiredMixin, View):

    def get(self, request):

        # =========================
        # FILTRO (MISMO QUE HTML)
        # =========================
        genero = request.GET.get('genero')

        asistencias = (
            Asistencia.objects
            .select_related('inscrito')
            .order_by('-fecha', '-hora')
        )

        if genero:
            asistencias = asistencias.filter(inscrito__genero=genero)

        # =========================
        # RESPUESTA PDF
        # =========================
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="lista_asistencias.pdf"'

        doc = SimpleDocTemplate(
            response,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=30,
            bottomMargin=20
        )

        styles = getSampleStyleSheet()

        # 🔹 Estilo para salto de línea automático
        cell_style = ParagraphStyle(
            'cell',
            parent=styles['Normal'],
            fontSize=8,
            leading=10,
            alignment=1  # CENTER
        )

        elementos = []

        # =========================
        # TÍTULO
        # =========================
        elementos.append(
            Paragraph("LISTA DE ASISTENCIAS", styles['Title'])
        )
        elementos.append(Paragraph("<br/>", styles['Normal']))

        # =========================
        # ENCABEZADOS
        # =========================
        data = [[
            "Día",
            "Fecha",
            "Nombre",
            "Correo",
            "Teléfono",
            "Zona",
            "Subzona",
            "Asistió"
        ]]

        # =========================
        # REGISTROS
        # =========================
        for a in asistencias:
            data.append([
                Paragraph(date_format(a.fecha, "l"), cell_style),
                Paragraph(a.fecha.strftime('%d/%m/%Y'), cell_style),
                Paragraph(a.inscrito.nombre, cell_style),
                Paragraph(a.inscrito.correo_electronico or "-", cell_style),
                Paragraph(a.inscrito.telefono or "-", cell_style),
                Paragraph(a.inscrito.zona or "-", cell_style),
                Paragraph(a.inscrito.subzona or "-", cell_style),
                Paragraph("Sí" if a.asistio else "No", cell_style),
            ])

        # =========================
        # TABLA
        # =========================
        tabla = Table(
            data,
            repeatRows=1,
            colWidths=[
                60,   # Día
                70,   # Fecha
                140,  # Nombre
                180,  # Correo
                90,   # Teléfono
                90,   # Zona
                90,   # Subzona
                60    # Asistió
            ]
        )

        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#52658c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),

            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        elementos.append(tabla)
        doc.build(elementos)

        return response

from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from .models import Inscrito


class RegistrosPDFView(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Lista_Inscritos.pdf"'

        doc = SimpleDocTemplate(
            response,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=30,
            bottomMargin=20
        )

        styles = getSampleStyleSheet()

        cell_style = styles['Normal']
        cell_style.fontSize = 8
        cell_style.leading = 10

        # === ENCABEZADOS ===
        data = [[
            "Nombre",
            "Zona",
            "Subzona",
            "¿Otra denominación?",
            "Denominación",
            "Teléfono",
            "Correo Electrónico",
            "Grado Eclesiástico",
            "Monto",
        ]]

        registros = get_inscritos_filtrados(request)

        for a in registros:
            data.append([
                Paragraph(a.nombre or "", cell_style),
                Paragraph(a.zona or "", cell_style),
                Paragraph(a.subzona or "", cell_style),
                Paragraph("Sí" if a.otra_denominacion else "No", cell_style),
                Paragraph(a.denominacion or "", cell_style),
                Paragraph(a.telefono or "", cell_style),
                Paragraph(a.correo_electronico or "", cell_style),
                Paragraph(a.grado or "", cell_style),
                Paragraph(f"${a.monto}" if a.monto else "", cell_style),
            ])

        tabla = Table(
            data,
            colWidths=[95, 55, 65, 80, 95, 75, 160, 100, 50],
            repeatRows=1
        )

        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#52658c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))

        doc.build([tabla])
        return response
