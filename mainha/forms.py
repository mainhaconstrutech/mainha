from django import forms
from mainha import models as MainhaModels


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nome do projeto"
        })
        self.fields["description"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Descrição do projeto"
        })

    class Meta:
        model = MainhaModels.Project
        fields = ["name", "description"]
        labels = {
            "name": "Nome",
            "description": "Descrição",
        }


class StandardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nome da norma"
        })
        self.fields["description"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Descrição da norma"
        })

    class Meta:
        model = MainhaModels.Standard
        fields = ["name", "description"]
        labels = {
            "name": "Nome",
            "description": "Descrição",
        }


class StandardRuleForm(forms.ModelForm):
    standard = forms.ModelChoiceField(
        queryset=MainhaModels.Standard.objects.all(),
        widget=forms.HiddenInput(),
        label="Norma"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nome do Critério da Norma"
        })
        self.fields["description"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Descrição do Critério da Norma"
        })
        self.fields["group"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Hierarquia de organização"
        })
        self.fields["standard"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Norma"
        })
        if kwargs["initial"] and kwargs["initial"]["standard_id"]:
            self.fields["standard"].widget.attrs.update({
                "value": kwargs["initial"]["standard_id"]
            })

    class Meta:
        model = MainhaModels.StandardRule
        fields = ["name", "description", "group", "standard"]
        labels = {
            "name": "Nome",
            "description": "Descrição",
            "group": "Hierarquia de organização",
        }
