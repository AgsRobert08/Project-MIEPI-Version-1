from django import forms
from .models import Cursos, Inscrito


class CoursesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'type': 'text',
            'autocomplete': 'off',
        })
        self.fields['description'].widget.attrs.update({
            'type': 'text',
            'autocomplete': 'off',
        })
        self.fields['start_date'].widget.attrs.update({
            'type': 'date',
        })

    class Meta:
        model = Cursos
        fields = '__all__'


class InscritoForm(forms.ModelForm):
    class Meta:
        model = Inscrito
        fields = [
            'nombre', 'genero', 'zona', 'subzona', 'otra_denominacion',
            'denominacion', 'telefono', 'grado', 'periodo', 'monto',
            'correo_electronico'
        ]


    def clean(self):
        cleaned_data = super().clean()

        otra = cleaned_data.get('otra_denominacion')
        zona = cleaned_data.get('zona')
        subzona = cleaned_data.get('subzona')
        denominacion = cleaned_data.get('denominacion')

        # 🔹 SI ES DE OTRA DENOMINACIÓN
        if otra == 'Sí':
            # Zona y subzona NO son requeridas
            cleaned_data['zona'] = None
            cleaned_data['subzona'] = None

            if not denominacion:
                self.add_error(
                    'denominacion',
                    'Este campo es obligatorio si es de otra denominación.'
                )

        # 🔹 SI NO ES DE OTRA DENOMINACIÓN
        else:
            if not zona:
                self.add_error(
                    'zona',
                    'Este campo es obligatorio.'
                )
            if not subzona:
                self.add_error(
                    'subzona',
                    'Este campo es obligatorio.'
                )

            # Denominación no aplica
            cleaned_data['denominacion'] = None

        return cleaned_data


class InscritoFormEdit(forms.ModelForm):
    class Meta:
        model = Inscrito
        fields = [
            'nombre',
            'genero',
            'otra_denominacion',
            'denominacion',
            'zona',
            'subzona',
            'telefono',
            'correo_electronico',
            'grado',
            'monto'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input'}),
            'zona': forms.TextInput(attrs={'class': 'input'}),
            'subzona': forms.TextInput(attrs={'class': 'input'}),
            'denominacion': forms.TextInput(attrs={'class': 'input'}),
            'telefono': forms.TextInput(attrs={'class': 'input'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'input'}),
            'grado': forms.TextInput(attrs={'class': 'input'}),
            'monto': forms.NumberInput(attrs={'class': 'input'}),
        }
