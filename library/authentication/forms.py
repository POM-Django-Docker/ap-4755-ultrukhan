from django import forms
from authentication.models import CustomUser


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
    )
    role = forms.ChoiceField(
        choices=[(0, 'User'), (1, 'Admin')],
        label='Role'
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'middle_name', 'last_name']


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'}),
        label='Password'
    )