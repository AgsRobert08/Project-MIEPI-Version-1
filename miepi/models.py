from django.db import models
import uuid


class Inscripciones(models.Model):
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

    OPCIONES_CURSO = [
        ('Curso de Abril 2026', 'Curso de Abril 2026'),
    ]

    nombre_completo = models.CharField(max_length=200)
    subzona = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    grado_eclesiastico = models.CharField(max_length=100)

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


def qr_upload_path(instance, filename):
    return f"qr/inscritos/{instance.codigo}.png"


class Inscrito(models.Model):
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre = models.CharField(max_length=150)

    # 🔹 Campo género agregado
    genero = models.CharField(
        max_length=10,
        choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')],
    )

    # para comentar algo usamos el #
    #y entonces vamos a usar  un choices aqui y comentar este o dejarlo asi, igual no se usara.
    #  lo dejare ahi y are el nuevo campo, primero el choices
    ZONAS = [
        ('CENTRAL', 'CENTRAL'),
        ('CDMX', 'CD. DE MEX.'),
        ('PUEBLA', 'PUEBLA, PUE.'),
        ('XALAPA', 'XALAPA, VER.'),
        ('MISANTLA', 'MISANTLA, VER.'),
        ('ALTOTONGA', 'ALTOTONGA, VER.'),
        ('JUCHIQUE', 'JUCHIQUE DE FERRER, VER.'),
        ('POZA_RICA', 'POZA RICA, VER.'),
        ('CUERNAVACA', 'CUERNAVACA, MOR.'),
        ('URUAPAN', 'URUAPAN, MICH.'),
        ('CARDENAS', 'CARDENAS, TAB.'),
        ('GUADALAJARA', 'GUADALAJARA, JAL.'),
        ('SILAO', 'SILAO, GTO.'),
        ('PACHUCA', 'PACHUCA, HGO.'),
        ('CANCUN', 'CANCÚN, Q. R.'),
        ('JUAREZ', 'CIUDAD JUÁREZ, CHIH.'),
        ('MATIAS_ROMERO', 'MATÍAS ROMERO, OAX.'),
        ('CHILPANCINGO', 'CHILPANCINGO, GRO.'),
        ('TIJUANA', 'TIJUANA, B.C.'),
        ('REYNOSA', 'REYNOSA, TAMPS.'),
        ('TOLUCA', 'TOLUCA, EDO. DE MEX.'),
        ('OAXACA', 'OAXACA, OAX.'),
        ('ELGIN', 'ELGIN ILLINOIS, EUA'),
        ('TAPACHULA', 'TAPACHULA, CHIS.'),
        ('CABO', 'CABO SAN LUCAS, B.C.S.'),
        ('TEZIUTLAN', 'TEZIUTLÁN, PUE.'),
        ('TAMPICO', 'TAMPICO, TAMPS.'),
        ('VERACRUZ', 'VERACRUZ, VER.'),
        ('TOPILEJO', 'TOPILEJO, CD. MEX.'),
        ('NEZA', 'CIUDAD NEZAHUALCÓYOTL, EDOMEX'),
        ('MIRAFLORES', 'MIRAFLORES, EDOMEX'),
        ('CALPULALPAN', 'CALPULALPAN, TLAX.'),
        ('COYOTEPEC', 'COYOTEPEC, EDOMEX'),
        ('CENTRO_SUR', 'CENTRO Y SUDAMÉRICA'),
    ]
    zona = models.CharField(max_length=100,choices=ZONAS, blank=True, null=True) # aqui es texto, asi que lo vamos a cmabiar a seleccionable


    subzona = models.CharField(max_length=100, blank=True, null=True)

    otra_denominacion = models.CharField(
        max_length=2,
        choices=[('Sí', 'Sí'), ('No', 'No')],
        default='No'
    )
    denominacion = models.CharField(max_length=150, blank=True, null=True)

    telefono = models.CharField(max_length=20, unique=True)
    GRADOS = [
        ('MINISTRO', 'MINISTRO / DIACONISA'),
        ('EG_ITE_ESC', 'EGRESADO DEL I.T.E. (Sistema Escolarizado)'),
        ('EG_ITE_AB', 'EGRESADO DEL I.T.E. (Sistema Abierto)'),
        ('EST_1_ESC', 'ESTUDIANTE (PRIMER AÑO) S.E.'),
        ('EST_2_ESC', 'ESTUDIANTE (SEGUNDO AÑO) S.E.'),
        ('EST_3_ESC', 'ESTUDIANTE (TERCER AÑO) S.E.'),
        ('EST_1_AB', 'ESTUDIANTE (PRIMER AÑO) S. ABIERTO'),
        ('EST_2_AB', 'ESTUDIANTE (SEGUNDO AÑO) S. ABIERTO'),
        ('EST_3_AB', 'ESTUDIANTE (TERCER AÑO) S. ABIERTO'),
        ('EST_4_AB', 'ESTUDIANTE (CUARTO AÑO) S. ABIERTO'),
        ('OBRERO', 'OBRERO LAICO'),
        ('ANCIANO', 'ANCIANO DE IGLESIA'),
        ('OTRO', 'OTRO (ESPECIFICAR)'),
        ('REP_ZONA', 'REPRESENTANTE DE ZONA'),
        ('REP_SUBZONA', 'REPRESENTANTE DE SUB ZONA'),
        ('EG_XAL_ESC', 'EGRESADO ITE CAMPUS XALAPA S. ESCOLARIZADO'),
        ('EG_XAL_AB', 'EGRESADO ITE CAMPUS XALAPA S. ABIERTO'),
        ('EG_SUR_ESC', 'EGRESADO ITE CAMPUS SURESTE S. ESCOLARIZADO'),
        ('EG_ELGIN', 'EGRESADO ITE CAMPUS ELGIN, IL'),
        ('SIN_RANGO', 'SIN RANGO'),
    ]
    grado = models.CharField(max_length=100, choices=GRADOS)

    periodo = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=8, decimal_places=2)

    qr_image = models.ImageField(upload_to=qr_upload_path, blank=True, null=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    correo_electronico = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Asistencia(models.Model):
    inscrito = models.ForeignKey(Inscrito, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField(auto_now_add=True)
    asistio = models.BooleanField(default=True)

    class Meta:
        unique_together = ('inscrito', 'fecha')

    def __str__(self):
        return f"{self.inscrito.nombre} - {self.fecha}"
