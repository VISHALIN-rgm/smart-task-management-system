from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class BaseUserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2', None)  # Remove confirm password field

        # Clean up field labels and help text
        for field in self.fields.values():
            field.help_text = ''
            field.widget.attrs.update({'class': 'form-control'})

class AdminRegisterForm(BaseUserRegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'admin'
        if commit:
            user.save()
        return user

class ManagerRegisterForm(BaseUserRegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'manager'
        if commit:
            user.save()
        return user

class HRRegisterForm(BaseUserRegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'hr'
        if commit:
            user.save()
        return user

class EmployeeRegisterForm(BaseUserRegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employee'
        if commit:
            user.save()
        return user



from django import forms
from .models import CustomUser

class ManagerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']  # REMOVED professional_background

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'Manager'  # Automatically assign Manager role
        if commit:
            user.save()
        return user
