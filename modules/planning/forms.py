from django import forms  
from .models import CompetenciasAdq, Perfil, CompetenciasReq
from ..app.models import Publico, TablasConfiguracion, Programascap




class perfilForm(forms.ModelForm):
    deescripcion = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add a name",                
                "class": "form-control", 
                'autofocus': True
            }
        ))
    desc_corta = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add a description",                
                "class": "form-control"
            }
        ))
    fk_rama = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.filter(id_tabla=TablasConfiguracion.objects.get(valor_elemento="Rama").id_tabla), empty_label="Which branch it belongs?",
    # fk_rama = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.all(),
        widget=forms.Select(
            attrs={        
                "placeholder" : "Select a branch",        
                "class": "form-control",
            }
        ))

    class Meta:  
        model = Perfil  
        fields = "__all__"  

class competenciaForm(forms.ModelForm):
    desc_competencia = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Add a description",                
                "class": "form-control", 
                'autofocus': True
            }
        ))
    fk_perfil = forms.ModelChoiceField(queryset=Perfil.objects.all(), empty_label="Which profile it belongs?",
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
            }
        ))
    # fk_tipo_competencia = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.exclude(fk_tabla_padre=1).filter(valor_elemento="Tipo Competencia"), empty_label="Select an option",
    fk_tipo_competencia = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.filter(valor_elemento="Tipo Competencia"), empty_label="Select its type",
    # fk_tipo_competencia = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.all(), empty_label="Select an option",
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
            }
        ))
    fk_nivel = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.filter(valor_elemento="NivelComp"), empty_label="Select a minimun level to aprove",
    # fk_nivel = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.all(), empty_label="Select an option",
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
            }
        ))

    class Meta:  
        model = CompetenciasReq  
        fields = "__all__"  

class competenciaAdqForm(forms.ModelForm):
    # fk_competencia = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.all(), empty_label="Select an option",
    fk_competencia = forms.ModelChoiceField(queryset=CompetenciasReq.objects.all(), empty_label="Select a competence",
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
                'autofocus': True
            }
        ))
    fk_nivel = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.filter(valor_elemento="NivelComp"), empty_label="Skill level",
    # fk_nivel = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.all(), empty_label="Select an option",
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
    fk_tipo_duracion = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.filter(valor_elemento="Duracion"), empty_label="Duration's type",
    # fk_nivel = forms.ModelChoiceField(queryset=TablasConfiguracion.objects.all(), empty_label="Select an option",
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
            }
        ))
    fk_publico = forms.ModelChoiceField(queryset=Publico.objects.all(), empty_label="Which public it belongs?",
        widget=forms.Select(
            attrs={                
                "class": "form-control form-control",
            }
        ))

    class Meta:  
        model = CompetenciasAdq  
        # fields = "__all__"  
        fields = ["fk_competencia", "fk_nivel", "periodo", "experiencia", "fk_tipo_duracion", "fk_publico"] 
        
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