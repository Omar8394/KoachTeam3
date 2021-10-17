from django import forms 
from ..app.models import TablasConfiguracion,PreguntasFrecuentes

class preguntasfrecuentes(forms.ModelForm):
    texto_pregunta = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add a Question",                
                "class": "form-control", 
            }
        ))
    texto_respuesta = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Enter Answer",                
                "class": "form-control"
            }
        ))
    fk_tipo_pregunta_frecuente = forms.ModelChoiceField(queryset=TablasConfiguracion.obtenerHijos("Frecuente"),
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
            }
        ))

    class Meta:  
        model = PreguntasFrecuentes
        fields = "__all__" 
    