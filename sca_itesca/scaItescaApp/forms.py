from django import forms  
from .models import File


class TrainingPlanForm(forms.Form):
    nombre_del_evento = forms.CharField(max_length=255, required=True)

    
class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']