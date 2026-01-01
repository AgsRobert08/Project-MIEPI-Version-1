from django import forms
from .models import *

class CoursesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'type': 'text',
            'autocomplete':'off',
        })
        self.fields['description'].widget.attrs.update({
            'type': 'text',
            'autocomplete':'off',
        })
        self.fields['start_date'].widget.attrs.update({
            'type': 'date',
        })

    class Meta:
        model= Cursos 
        fields = '__all__'


class InscritoForm(forms.ModelForm):
    class Meta:
        model = Inscrito
        fields = [
            'nombre',
            'subzona',
            'telefono',
            'grado',
            'periodo',
            'monto',
        ]