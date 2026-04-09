from django import forms
from django.core.exceptions import ValidationError

from mainha import models as MainhaModels


class AccountAdminCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nome da organização"
        })
        self.fields["cnpj"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "CNPJ da organização"
        })
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "E-mail da organização"
        })
        self.fields["phone"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Telefone da organização"
        })
        self.fields["subscription"].widget.attrs.update({
            "class": "form-select",
            "placeholder": "Assinatura"
        })

    class Meta:
        model = MainhaModels.Account
        fields = ["name", "cnpj", "email", "phone", "subscription"]
        labels = {
            "name": "Nome",
            "cnpj": "CNPJ",
            "email": "E-mail",
            "phone": "Telefone",
            "subscription": "Assinatura",
        }


class AccountRegularUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nome da organização"
        })
        self.fields["cnpj"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "CNPJ da organização"
        })
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "E-mail da organização"
        })
        self.fields["phone"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Telefone da organização"
        })

    class Meta:
        model = MainhaModels.Account
        fields = ["name", "cnpj", "email", "phone"]
        labels = {
            "name": "Nome",
            "cnpj": "CNPJ",
            "email": "E-mail",
            "phone": "Telefone"
        }


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


class ValidationForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=MainhaModels.Project.objects.none(),
        empty_label="--- Selecione um projeto ---",
        label="Projeto"
    )

    standard = forms.ModelChoiceField(
        queryset=MainhaModels.Standard.objects.all(),
        required=True,
        empty_label="--- Selecione uma norma ---",
        label="Norma"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('initial').get('user')
        project_id = kwargs.get('initial').get('project')

        if project_id is None:
            projects = MainhaModels.Project.objects.filter(user=user).all()
        else:
            projects = MainhaModels.Project.objects.filter(pk=project_id, user=user).all()

        self.fields["project"].queryset = projects
        self.fields["project"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Projeto"
        })
        self.fields["standard"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Norma"
        })

    class Meta:
        model = MainhaModels.Validation
        fields = ["project", "standard"]


class ValidationRuleForm(forms.ModelForm):
    validation = forms.ModelChoiceField(
        queryset=MainhaModels.Validation.objects.all(),
        widget=forms.HiddenInput(),
        label="Análise de projeto"
    )

    standard_rule = forms.ModelChoiceField(
        queryset=MainhaModels.StandardRule.objects.all(),
        widget=forms.HiddenInput(),
        required=True,
        label="Critério da norma"
    )

    fulfilled = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
        label="Cumprido?"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fulfilled"].widget.attrs.update({
            "class": "form-check-input",
            "role": "switch",
            "placeholder": "Cumprido?"
        })
        self.fields["note"].widget.attrs.update({
            "class": "form-control",
            "rows": 2,
            "placeholder": "Observações..."
        })

    class Meta:
        model = MainhaModels.ValidationRule
        fields = ["validation", "standard_rule", "fulfilled", "note"]
        labels = {
            "fulfilled": "Cumprido?",
            "note": "Observação",
        }
