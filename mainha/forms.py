from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from mainha import models as MainhaModels
from mainha import scopes as MainhaScopes
from mainha import services as MainhaServices


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class CreateAccountAdminUserForm(forms.Form):
    account_name = forms.CharField(
        max_length=512,
        label='Nome da organização',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    account_cnpj = forms.CharField(
        max_length=512,
        required=False,
        label='CNPJ da organização',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0000-00'})
    )
    account_email = forms.EmailField(
        max_length=512,
        label='E-mail da organização',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'business@email.com'})
    )
    account_phone = forms.CharField(
        max_length=512,
        label='Telefone da organização',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '(00) 0 0000-0000'})
    )
    account_subscription = forms.ChoiceField(
        label='Assinatura da conta',
        choices=MainhaModels.Account.SUBSCRIPTION_CHOICES,
        initial='trial',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    user_email = forms.EmailField(
        max_length=254,
        label='E-mail do administrador',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'personal@email.com'})
    )
    user_password = forms.CharField(
        label='Senha do administradors',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class AccountAdminUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome da organização'
        })
        self.fields['cnpj'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'CNPJ da organização'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'E-mail da organização'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Telefone da organização'
        })
        self.fields['subscription'].widget.attrs.update({
            'class': 'form-select',
            'placeholder': 'Assinatura'
        })

    class Meta:
        model = MainhaModels.Account
        fields = ['name', 'cnpj', 'email', 'phone', 'subscription']
        labels = {
            'name': 'Nome',
            'cnpj': 'CNPJ',
            'email': 'E-mail',
            'phone': 'Telefone',
            'subscription': 'Assinatura',
        }


class AccountRegularUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome da organização'
        })
        self.fields['cnpj'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'CNPJ da organização'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'E-mail da organização'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Telefone da organização'
        })

    class Meta:
        model = MainhaModels.Account
        fields = ['name', 'cnpj', 'email', 'phone']
        labels = {
            'name': 'Nome',
            'cnpj': 'CNPJ',
            'email': 'E-mail',
            'phone': 'Telefone'
        }


class CreateUserAccountForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'personal@email.com'})
    )
    role = forms.ChoiceField(
        label='Função',
        choices=MainhaModels.UserAccount.ROLE_CHOICES,
        initial='employee',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class UpdateUserAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['active'].widget.attrs.update({
            'class': 'form-check-input',
            'role': 'switch',
        })
        self.fields['role'].widget.attrs.update({
            'class': 'form-select'
        })

    class Meta:
        model = MainhaModels.UserAccount
        fields = ['active', 'role']
        labels = {
            'active': 'Ativo',
            'role': 'Função',
        }


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome do projeto'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Descrição do projeto'
        })

    class Meta:
        model = MainhaModels.Project
        fields = ['name', 'description']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
        }


class UserProjectForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=MainhaModels.Project.objects.all(),
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        projects = MainhaScopes.Scopes.list_projects(self.user).filter(id=kwargs.get('initial').get('project'))
        project = projects.first()

        self.fields['project'].widget.attrs.update({'class': 'form-select'})
        self.fields['project'].queryset = projects
        self.fields['project'].empty_label = None

        project_user_ids = MainhaServices.ProjectService.list_user_project_in_project(
            project
        ).values_list('user__id', flat=True)

        account_user_ids_availables = MainhaServices.AccountService.list_user_account_in_account(
            project.account
        ).filter(
            role__in=['guest', 'employee']
        ).exclude(
            user__id__in=project_user_ids
        ).values_list('user__id', flat=True)

        self.fields['user'].widget.attrs.update({'class': 'form-select'})
        self.fields['user'].queryset = User.objects.filter(id__in=account_user_ids_availables)

    def clean(self):
        cleaned_data = super().clean()
        user = self.cleaned_data.get('user')
        project = self.cleaned_data.get('project')

        if not MainhaServices.AccountService.list_user_account_in_account(project.account).filter(user_id=user.id).exists():
            raise forms.ValidationError('User not allowed to be added to the project.')
        return cleaned_data

    class Meta:
        model = MainhaModels.UserProject
        fields = ['project', 'user']
        labels = {
            'project': 'Projeto',
            'user': 'Usuário',
        }


class StandardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome da norma'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Descrição da norma'
        })

    class Meta:
        model = MainhaModels.Standard
        fields = ['name', 'description']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
        }


class StandardRuleForm(forms.ModelForm):
    standard = forms.ModelChoiceField(
        queryset=MainhaModels.Standard.objects.all(),
        widget=forms.HiddenInput(),
        label='Norma'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome do Critério da Norma'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Descrição do Critério da Norma'
        })
        self.fields['group'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Hierarquia de organização'
        })
        self.fields['standard'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Norma'
        })

    class Meta:
        model = MainhaModels.StandardRule
        fields = ['name', 'description', 'group', 'standard']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'group': 'Hierarquia de organização',
        }


class StandardRuleBulkForm(forms.Form):
    standard = forms.ModelChoiceField(
        queryset=MainhaModels.Standard.objects.all(),
        widget=forms.HiddenInput(),
        label='Norma'
    )
    standard_rules = forms.JSONField(label='Critérios da norma')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['standard_rules'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['standard'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Norma'
        })

    def clean_standard_rules(self):
        standard_rules_data = self.cleaned_data['standard_rules']
        if not type(standard_rules_data) is list:
            raise ValidationError('Enter a valid JSON.')
        else:
            for standard_rule in standard_rules_data:
                if not 'name' in standard_rule:
                    raise ValidationError('Enter a valid JSON.')
        return standard_rules_data


class ValidationForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=MainhaModels.Project.objects.none(),
        empty_label='--- Selecione um projeto ---',
        label='Projeto'
    )

    standard = forms.ModelChoiceField(
        queryset=MainhaModels.Standard.objects.all(),
        required=True,
        empty_label='--- Selecione uma norma ---',
        label='Norma'
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        project_id = kwargs.get('initial').get('project')
        projects = MainhaScopes.Scopes.list_projects(self.user)

        if project_id:
            projects = projects.filter(pk=project_id).all()

        self.fields['project'].queryset = projects
        self.fields['project'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Projeto'
        })
        self.fields['standard'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Norma'
        })

    def clean(self):
        cleaned_data = super().clean()
        project = self.cleaned_data.get('project')

        if not MainhaScopes.Scopes.list_projects(self.user).filter(pk=project.pk).exists():
            raise forms.ValidationError('Cannot send this project to analysis.')
        return cleaned_data

    class Meta:
        model = MainhaModels.Validation
        fields = ['project', 'standard']


class ValidationRuleForm(forms.ModelForm):
    validation = forms.ModelChoiceField(
        queryset=MainhaModels.Validation.objects.all(),
        widget=forms.HiddenInput(),
        label='Análise de projeto'
    )

    standard_rule = forms.ModelChoiceField(
        queryset=MainhaModels.StandardRule.objects.all(),
        widget=forms.HiddenInput(),
        required=True,
        label='Critério da norma'
    )

    fulfilled = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
        label='Cumprido?'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fulfilled'].widget.attrs.update({
            'class': 'form-check-input',
            'role': 'switch',
            'placeholder': 'Cumprido?'
        })
        self.fields['note'].widget.attrs.update({
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Observações...'
        })

    class Meta:
        model = MainhaModels.ValidationRule
        fields = ['validation', 'standard_rule', 'fulfilled', 'note']
        labels = {
            'fulfilled': 'Cumprido?',
            'note': 'Observação',
        }
