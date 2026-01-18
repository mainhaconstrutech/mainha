from django import forms
from django.core.exceptions import ValidationError

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

    class Meta:
        model = MainhaModels.StandardRule
        fields = ["name", "description", "group", "standard"]
        labels = {
            "name": "Nome",
            "description": "Descrição",
            "group": "Hierarquia de organização",
        }


class StandardRuleBulkForm(forms.Form):
    standard = forms.ModelChoiceField(
        queryset=MainhaModels.Standard.objects.all(),
        widget=forms.HiddenInput(),
        label="Norma"
    )
    standard_rules = forms.JSONField(label="Critérios da norma")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["standard_rules"].widget.attrs.update({
            "class": "form-control",
        })
        self.fields["standard"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Norma"
        })

    def clean_standard_rules(self):
        standard_rules_data = self.cleaned_data["standard_rules"]
        if not type(standard_rules_data) is list:
            raise ValidationError("Enter a valid JSON.")
        else:
            for standard_rule in standard_rules_data:
                if not "name" in standard_rule:
                    raise ValidationError("Enter a valid JSON.")
        return standard_rules_data
