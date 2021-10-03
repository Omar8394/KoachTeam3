from django import forms  
from .models import CompetenciasAdq, Perfil, CompetenciasReq
from ..app.models import Publico, TablasConfiguracion, Programascap

class perfilForm(forms.ModelForm):

    deescripcion = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add a name",                
                "class": "form-control", 
                'autofocus': True,
                'id':'id_username',
                'maxlength':15
            }
        ))

    desc_corta = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add a description",                
                "class": "form-control",
                'maxlength':100
            }
        ))

    fk_rama = forms.ModelChoiceField(queryset=TablasConfiguracion.obtenerHijos("Rama"), empty_label="Which branch it belongs?",
        widget=forms.Select(
            attrs={        
                "placeholder" : "Select a branch",        
                "class": "form-control",
            }
        )) 

    def __init__(self, property_id = None, *args, **kwargs):

        self.property_id = property_id
        super(perfilForm, self).__init__(*args, **kwargs)

    class Meta:  

        model = Perfil  
        fields = "__all__" 

    def clean(self):
 
        super(perfilForm, self).clean()
         
        deescripcion = self.cleaned_data.get('deescripcion')
 
        if(Perfil.filtering(deescripcion, self.property_id)):

            self._errors['deescripcion'] = self.error_class(["There is a Profile named %s" %(deescripcion)])

        return self.cleaned_data
      

class competenciaForm(forms.ModelForm):
    desc_competencia = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add a description",                
                "class": "form-control", 
                'autofocus': True,
                'id':'id_username',
                'maxlength':30
            }
        ))

    fk_perfil = forms.ModelChoiceField(queryset=Perfil.objects.all(), empty_label="Which profile it belongs?",
        widget=forms.Select(
            attrs={                
                "class": "form-control",
            }
        ))

    fk_tipo_competencia = forms.ModelChoiceField(queryset=TablasConfiguracion.obtenerHijos("Tipo Competencia"), empty_label="Select its type",
        widget=forms.Select(
            attrs={                
                "class": "form-control",
            }
        ))

    fk_nivel = forms.ModelChoiceField(queryset=TablasConfiguracion.obtenerHijos("NivelComp"), empty_label="Select a minimun level to aprove",
        widget=forms.Select(
            attrs={                
                "class": "form-control",
            }
        ))

    def __init__(self, property_id = None, *args, **kwargs):

        self.property_id = property_id
        super(competenciaForm, self).__init__(*args, **kwargs)

    class Meta:  

        model = CompetenciasReq  
        fields = "__all__"  

    def clean(self):
 
        super(competenciaForm, self).clean()
         
        desc_competencia = self.cleaned_data.get('desc_competencia')
 
        if(CompetenciasReq.filtering(desc_competencia, self.property_id)):

            self._errors['desc_competencia'] = self.error_class(["There is a Competence named %s" %(desc_competencia)])

        return self.cleaned_data

class competenciaAdqForm(forms.ModelForm):

    fk_competencia = forms.ModelChoiceField(queryset=CompetenciasReq.objects.all(), empty_label="Select a competence",
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
            }
        ))

    fk_nivel = forms.ModelChoiceField(queryset=TablasConfiguracion.obtenerHijos("NivelComp"), empty_label="Skill level",
        widget=forms.Select(
            attrs={        
                "class": "form-control form-control",
            }
        ))

    periodo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Since when did you learn it?",                
                "class": "form-control", 
                "data-toggle":"tooltip",
                "data-placement":"bottom", 
                "title":"e.g. 2000-2001, since 2010 to now, 2020...",
            }
        ))

    experiencia = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "placeholder" : "Accumulated experience",                
                "class": "form-control", 
                "data-toggle":"tooltip",
                "data-placement":"bottom", 
                "title":"e.g. 1 year, 5 months, 1 week...",
            }
        ))

    fk_tipo_duracion = forms.ModelChoiceField(queryset=TablasConfiguracion.obtenerHijos("Duracion"), empty_label="Duration's type",
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
            }
        ))

    fk_publico = forms.ModelChoiceField(queryset=Publico.objects.all(), empty_label="Which public it belongs?",
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
                'autofocus': True,
            }
        ))

    def __init__(self, public_id = None, *args, **kwargs):

        self.public_id = public_id
        super(competenciaAdqForm, self).__init__(*args, **kwargs)
        
    class Meta:  
        model = CompetenciasAdq  
        # fields = "__all__"  
        fields = ["fk_publico", "fk_competencia", "fk_nivel", "periodo", "experiencia", "fk_tipo_duracion", ] 

        
class programForm(forms.ModelForm):
    desc_programas = forms.CharField(
        widget=forms.TextInput(
            attrs={
                 
                "placeholder" : "Description",             
                "class": "form-control", 
            }
        ))
    objetivo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                            
                "placeholder" : "Objective",  
                "class": "form-control", 
            }
        ))
    alcance = forms.CharField(
        widget=forms.TextInput(
            attrs={
                             
                "placeholder" : "Reach", 
                "class": "form-control", 
            }
        ))
    fecha_apertura = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={
                             
                "class": "form-control", 
            }
        ))

    class Meta:  
        model = Programascap  
        fields = "__all__"  