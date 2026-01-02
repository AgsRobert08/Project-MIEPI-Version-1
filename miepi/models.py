from django.db import models

class Inscripciones(models.Model):
    # Opciones para el campo de pago y periodo
    OPCIONES_PAGO = [
        ('Sí', 'Sí'),
        ('No', 'No'),
    ]

    OPCIONES_PERIODO = [
        ('', 'Seleccione'),
        ('Primer periodo|1500', '07 Ene - 21 Feb | $1,500'),
        ('Segundo periodo|1700', '22 Feb - 31 Mar | $1,700'),
        ('Tercer periodo|1900', '31 Mar - 26 Abr | $1,900'),
    ]

    # Opciones para el curso (Solo una opción como pediste)
    OPCIONES_CURSO = [
        ('Curso de Abril 2026', 'Curso de Abril 2026'),
    ]

    nombre_completo = models.CharField(max_length=200)
    subzona = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    grado_eclesiastico = models.CharField(max_length=100)
    
    # Campo con opción única y valor por defecto
    curso = models.CharField(
        max_length=100, 
        choices=OPCIONES_CURSO, 
        default='Curso de Abril 2026'
    )
    
    pago = models.CharField(max_length=2, choices=OPCIONES_PAGO)
    periodo_pago = models.CharField(max_length=50, choices=OPCIONES_PERIODO, blank=True, null=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.curso}"

    # Método auxiliar para obtener el monto limpio (opcional)
    def obtener_monto(self):
        if self.periodo_pago and '|' in self.periodo_pago:
            return self.periodo_pago.split('|')[1]
        return "-"

    def obtener_periodo_texto(self):
        if self.periodo_pago and '|' in self.periodo_pago:
            return self.periodo_pago.split('|')[0]
        return "No pagó"
    
class Cursos(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

import uuid
from django.db import models

def qr_upload_path(instance, filename):
    return f"qr/inscritos/{instance.codigo}.png"

class Inscrito(models.Model):
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    nombre = models.CharField(max_length=150)
    subzona = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, unique=True)
    grado = models.CharField(max_length=100)

    periodo = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=8, decimal_places=2)

    qr_image = models.ImageField(upload_to=qr_upload_path, blank=True, null=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    correo_electronico = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.nombre
    
    # models.py
# models.py
class Asistencia(models.Model):
    inscrito = models.ForeignKey(Inscrito, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField(auto_now_add=True)
    asistio = models.BooleanField(default=True)

    class Meta:
        unique_together = ('inscrito', 'fecha')

    def __str__(self):
        return f"{self.inscrito.nombre} - {self.fecha}"
