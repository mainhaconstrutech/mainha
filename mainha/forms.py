from django import forms
from mainha.models import Project

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Nome do projeto"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "placeholder": "Descrição do projeto"})

    class Meta:
        model = Project
        fields = ["name", "description"]
        labels = {
            "name": "Nome",
            "description": "Descrição",
        }