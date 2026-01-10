from django import forms
from mainha import models

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Nome do projeto"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "placeholder": "Descrição do projeto"})

    class Meta:
        model = models.Project
        fields = ["name", "description"]
        labels = {
            "name": "Nome",
            "description": "Descrição",
        }

class StandardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Nome da norma"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "placeholder": "Descrição da norma"})

    class Meta:
        model = models.Standard
        fields = ["name", "description"]
        labels = {
            "name": "Nome",
            "description": "Descrição",
        }

class StandardRuleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Nome da norma"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "placeholder": "Descrição da norma"})
        self.fields["group"].widget.attrs.update({"class": "form-control", "placeholder": "Hierarquia de organização"})
        self.fields["standard"].widget.attrs.update({"class": "form-control", "placeholder": "Norma"})
        
    class Meta:
        model = models.StandardRule
        fields = ["name", "description", "group", "standard"]
        labels = {
            "name": "Nome",
            "description": "Descrição",
            "group": "Hierarquia de organização",
            "standard": "Norma",
        }